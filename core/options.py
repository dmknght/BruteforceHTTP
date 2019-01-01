import sys
from core import helps, actions, utils

class ParseOptions(object):

	# Deny user choosing --httpget option
	# Program now automatic choose attack mode
	# --httpget is still useable in attack module
	
	ATTACK_MODES = (
		"--brute",
		#"--httpget",
		"--sqli",
	)
		
	run_options = {
		"--proxy": False,
		"--report": False,
		"--verbose": False,
	}

	extra_mode = (
		"--getproxy",
		"--reauth",
		"--social", # Similar reauth, no url
	)


	# TODO get dynamically using data.__init__
	WORDLISTS = (
		"default",
		"router",
		"unix",
		"tomcat",
		"cctv",
		"mirai",
		"http",
		"webshell"
	)

	options = {
		"-u": "default",
		"-p": "default",
		"-t": 16,
		"-U": None
	}

	HELP_OPTIONS = [
		"-h",
		"--help",
		"-help",
		"help"
	]

	def __init__(self):
		self.url = None
		self.login_url = None
		self.panel_url = None
		self.attack_mode = "--brute"
		self.extras = []
		self.help = False

		# options
		self.threads = 16
		self.username = None
		self.passwd = None

		# run_modes
		self.verbose = False
		self.proxy = None
		self.report = False

		self.get_options()

	def parse_options(self, szOptions):
		i = 1
		while i < szOptions:
			if sys.argv[i] in self.HELP_OPTIONS:
				self.help = True

			elif sys.argv[i].startswith("--"):
				
				if sys.argv[i] in self.run_options.keys():
					self.run_options[sys.argv[i]] = True
				elif sys.argv[i] in self.extra_mode:
					self.extras.append(sys.argv[i])
				elif sys.argv[i] in self.ATTACK_MODES:
					self.attack_mode = sys.argv[i]
			
				elif sys.argv[i] == "--list":

					if sys.argv[i + 1] in self.WORDLISTS:
						self.options["-u"] = sys.argv[i + 1]
						self.options["-p"] = sys.argv[i + 1]
						i += 1
					
					else:
						utils.die(
							"[x] Options: Arguments error",
							"Invalid wordlist %s" %(sys.argv[i + 1])
						)
				
				elif sys.argv[i] in self.HELP_OPTIONS:
					self.help = True
				
				else:
					utils.die(
						"[x] Options: Arguments error",
						"Unknow option %s" %(sys.argv[i])
					)
			
			elif sys.argv[i].startswith("-"):
				
				if sys.argv[i] in self.options.keys():
					self.options[sys.argv[i]] = sys.argv[i + 1]
					i += 1
				else:
					utils.die(
						"[x] Options: Arguments error",
						"Unknow option %s" %(sys.argv[i])
					)
			
			else:
				self.url = sys.argv[i]
			
			i += 1

	def get_options(self):
		szOptions = len(sys.argv)
		
		if szOptions == 1:
			# NO ARGUMENT
			helps.print_fast_help()

			utils.printf(
				"Use: %s for more infomation\n" %(self.HELP_OPTIONS)
			)
			sys.exit(0)

		else:
			try:
				self.parse_options(szOptions)
			except Exception as error:
				utils.die(
					"[x] Options: Parse options error",
					error
				)