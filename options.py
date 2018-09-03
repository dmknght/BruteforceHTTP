import sys, data
from core import utils, actions

##############################################
#	Parse user's options
#	Create default options
#
############################################

"""
	Format: python main.py [--<mode>] [-<option> <value>] <url>
	mode and option are optinal
	Todo: add working modules (likes getproxy) to main		
"""


def checkOption(url, options, proxy):
	
	finalOption = {}
	
	# Modify URL value to correct format
	# Read password list
	# Read userlist
	# Convert to int(threads)
	
	
	try:
		finalOption["threads"] = int(options["-t"])
	except Exception as ConvertError:
		utils.die("Invalid threads", ConvertError)
		
	finalOption["passlist"] = data.getPass() if options["-p"] == "default" else actions.fread(options["-p"])
	
	if options["-U"]:
		finalOption["userlist"] = actions.lread(options["-U"])
	else:
		finalOption["userlist"] = data.getUser() if options["-u"] == "default" else actions.fread(options["-u"])
	
	finalOption["falsekey"] = options["-k"]
	
	if "http" not in url:
		url = "http://%s" %(url)
	if url[-1] != "/":
		url += "/"
		
	if proxy:
		proxy = actions.getProxyList()
	
	return url, finalOption, proxy


def getUserOptions():
	
	URL = None
	USERLIST = "default"
	PASSLIST = "default"
	THREADS = 3
	KEY_FALSE = None
	MODE = "--brute"
	PROXY = False
	
	# Default operation modes:
	#	--brute: brute force
	#	--sqli: sql injection bypass login
	#	--basic: http basic authentication
	#	--proxy: Using proxy while attacking
	
	DEF_MODE = ("--brute", "--sqli", "--basic", "--proxy")
	
	# Default options:
	#	-u: Read userlist from file
	#	-p: Read passlit from file
	#	-U: Read username / userlist directly from argument
	#	-t: Number of threads using #TODO Modify for new module
	#	-k: Set key for false condition (for special cases)
	
	DEF_OPS = ("-u", "-U", "-p", "-t", "-k")
	
	options = {
		"-u": USERLIST,
		"-p": PASSLIST,
		"-t": THREADS,
		"-k": KEY_FALSE,
		"-U": None,
	}
	
	
	if len(sys.argv) == 1:
		utils.print_help()
		sys.exit(0)
	
	idx = 1
	while idx < len(sys.argv):
		if sys.argv[idx] in ("-h", "--help", "help"):
			utils.print_help()
			
		else:
			if sys.argv[idx] in DEF_MODE:
				if sys.argv[idx] == "--proxy":
					PROXY = True
				else:
					MODE = sys.argv[idx + 1]
					idx += 1
				
			elif sys.argv[idx] in DEF_OPS:
				options[sys.argv[idx]] = sys.argv[idx + 1]
				idx += 1
				# TODO -u vs -U
				
			else:
				URL  = sys.argv[idx]
				
		idx += 1
	
	if not URL:
		utils.printf("An URL is required", "bad")
		sys.exit(1)
	else:
		utils.printf(craftbanner(URL, options, MODE, PROXY), "good")
		URL, options, PROXY = checkOption(URL, options, PROXY)
		return URL, options, MODE, PROXY


def craftbanner(url, options, mode, useproxy):
	usr = options["-U"] if options["-U"] else options["-u"]

	banner = """
	======================================================================
	| Target: %s
	|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	| Users: %s
	| Password: %s
	|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
	| Threads: %s
	| Attack mode: %s
	|---------------------------------------------------------------------
	| False keyword: %s
	|---------------------------------------------------------------------
	| Using Proxy: %s
	======================================================================
	""" %(url, usr, options["-p"], options["-t"], mode.replace("--", ""), options["-k"], useproxy)
	
	return banner.replace("\t", "  ")