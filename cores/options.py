import sys
from utils import events


class ParseOptions(object):
	"""
	Object of user options
	Parse and save all flags
	"""

	ATTACK_MODES = (
		"--brute",
		# "--httpget",
		"--sqli",
	)

	run_options = {
		"--proxy": False,
		"--report": False,
		"--verbose": False,
	}

	extra_mode = (
		"--getproxy",
		"--upwd",
		"--reauth",
		"--social",  # Similar reauth, no url
	)

	WORDLISTS = (
		"default",
		"router",
		"unix",
		"tomcat",
		"cctv",
		"mirai",
		"http",
		"webshell",
		"sqli",
	)
	PASSWD_GEN = (
		"--toggle_case",  # TODO add mask* attack type, handle arguments
		"--replacement"
	)

	options = {
		"-u": "default",
		"-p": "default",
		"-t": 16,
		"-U": None,
		"-l": None,
		"-T": 25
	}

	HELP_OPTIONS = [
		"-h",
		"--help",
		"-help",
		"help"
	]

	def __init__(self):
		self.url = None
		self.target = None
		self.attack_mode = "--brute"
		self.extras = []
		self.txt = ""

		# options
		self.threads = 16
		# self.timeout = 25
		self.username = None
		self.passwd = None

		# run_modes
		self.verbose = False
		self.proxy = None
		self.report = False

		self.get_options()

	def parse_options(self, size_of_options):
		"""
		Parse all flags from sys arguments and save them
		:param size_of_options: int = size of arguments
		:return: list[dummy] of flag
		"""
		i = 1
		while i < size_of_options:
			# Check flag has format --X
			if sys.argv[i].startswith("--"):
				# Save flag values in each option type
				if sys.argv[i] in self.run_options.keys():
					self.run_options[sys.argv[i]] = True
				elif sys.argv[i] in self.extra_mode:
					self.extras.append(sys.argv[i])
				elif sys.argv[i] in self.ATTACK_MODES:
					self.attack_mode = sys.argv[i]
				elif sys.argv[i] in self.PASSWD_GEN:
					self.extras.append(sys.argv[i])

				# Check if flag is wordlist setting
				elif sys.argv[i] == "--list":
					if sys.argv[i + 1] in self.WORDLISTS:
						self.options["-u"] = sys.argv[i + 1]
						self.options["-p"] = sys.argv[i + 1]
						i += 1
					# Invalid name of wordlist
					else:
						events.error("Invalid wordlist", "ARGS")
						sys.exit(1)
				# Invalid flag X - Not defined
				else:
					events.error("Unknown option %s" % (sys.argv[i]), "ARGS")
					sys.exit(1)

			# Check flags with format -X
			elif sys.argv[i].startswith("-"):
				# Save value if it is in our dictionary
				if sys.argv[i] in self.options.keys():
					self.options[sys.argv[i]] = sys.argv[i + 1]
					i += 1
				# Invalid flag X - Not defined
				else:
					events.error("Unknown option %s" % (sys.argv[i], "ARGS"))
					sys.exit(1)

			# No - -> should be URL
			else:
				self.url = sys.argv[i]
			# Increase value if index
			i += 1

	def get_options(self):
		"""
		Analysis flags to print help or parse flag (Try to save performance)
		:return: list[dummy] flags with defined values
		"""

		# Get size of argv array (don't have to call len function multiple times)
		size_of_options = len(sys.argv)

		if size_of_options == 1:
			# If user gives no argument, print help banner [short] and exit
			from utils import helps
			helps.print_fast_help()
			events.info("Use: %s for more information" % (self.HELP_OPTIONS))
			sys.exit(0)

		else:
			# Check if options has help flag -> print help banner [full] and exit
			if [True if flag in sys.argv else False for flag in self.HELP_OPTIONS][0]: from utils import helps; helps.print_help()
			try:
				self.parse_options(size_of_options)
			except Exception as error:
				events.error("%s" % (error), "ARGS")

	def exceptions(self):
		"""
		List of extensions on web that we don't open to save time
		:return: a tuple (save a little memory) of common extensions
		"""
		return (
			".css", ".js", ".jpg", ".png", ".jpeg", ".doc", ".docx", ".xlsx", ".pdf", ".txt", ".rar", ".bak", ".zip",
			".7z")
