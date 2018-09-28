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

	
URL = None
MODE = "--brute"
DEF_WORDLIST = ("default", "router", "unix", "tomcat", "cctv", "mirai", "http")


r_options = {
	"--proxy": False,
	"--report": False,
	"--verbose": False,
}

def checkURL(url):
	if "http" not in url:
		url = "http://%s" %(url)
	if url[-1] != "/":
		url += "/"
	return url
	
def checkOption(options, r_options):
	
	finalOption = {}
	global MODE, DEF_WORDLIST
	# Modify URL value to correct format
	# Read password list
	# Read userlist
	# Convert to int(threads)
	
	
	try:
		finalOption["threads"] = int(options["-t"])
		if finalOption["threads"] < 1:
			utils.die("Value error", "Threads must be > 1")
	except Exception as ConvertError:
		utils.die("Invalid threads", ConvertError)
		
	if MODE == "--sqli":
		finalOption["passlist"] = "MyP@ssW0rd"
		finalOption["userlist"] = data.getSQL()
		
	else:
		# WARNING eval() is called. It can be unsafe
		finalOption["passlist"] = eval("data.%s_pass()" %(options["-p"])) if options["-p"] in DEF_WORDLIST else actions.fread(options["-p"])
		
		if options["-U"]:
			finalOption["userlist"] = actions.lread(options["-U"])
		else:
			finalOption["userlist"] = eval("data.%s_user()" %(options["-u"])) if options["-u"] in DEF_WORDLIST else actions.fread(options["-u"])
	
	finalOption["falsekey"] = options["-k"]
		
	if r_options["--proxy"]:
		r_options["--proxy"] = actions.getProxyList()
	
	return finalOption, r_options


def getUserOptions():
		
	global URL, MODE, r_options, DEF_WORDLIST
	
	# Default operation modes:
	#	--brute: brute force
	#	--sqli: sql injection bypass login (TODO)
	#	--basic: http basic authentication (TODO)
	
	DEF_A_MODE = ("--brute", "--sqli", "--basic")
	
	# Default running mode:
	#	--verbose: display informations (TODO)
	#	--report: creating log file (TODO)
	#	--proxy: Running using proxy
	
	DEF_R_MODE = ("--verbose", "--report", "--proxy")
	
	# Default options:
	#	-u: Read userlist from file
	#	-p: Read passlit from file
	#	-U: Read username / userlist directly from argument
	#	-t: Number of threads using #TODO Modify for new module
	#	-k: Set key for false condition (for special cases)
	
	DEF_OPS = ("-u", "-U", "-p", "-t", "-k")
	
	# Default wordlist: default, router, unix, tomcat, cctv, mirai, http
		
	options = {
		"-u": "default",
		"-p": "default",
		"-t": 16,
		"-k": None,
		"-U": None,
	}
	
	
	if len(sys.argv) == 1:
		utils.print_help()
		sys.exit(0)
	
	idx = 1
	while idx < len(sys.argv):
		if sys.argv[idx] in ("-h", "--help", "help"):
			utils.print_help()
			sys.exit(0)
			
		else:
			if sys.argv[idx][:2] == "--":
				if sys.argv[idx] in DEF_R_MODE:
					# --verbose", "--report", "--proxy"
					r_options[sys.argv[idx]] = True

				elif sys.argv[idx] in DEF_A_MODE:
					# "--brute", "--sqli", "--basic"
					MODE = sys.argv[idx]
					
				elif sys.argv[idx] == "--list":
					# Wordlist provided
					if sys.argv[idx + 1] in DEF_WORDLIST:
						options["-u"], options["-p"], idx = sys.argv[idx + 1], sys.argv[idx + 1], idx + 1
					else:
						utils.die("Parsing option error", "Invalid wordlist %s" %(sys.argv[idx + 1]))

				else:
					utils.die("Error while parsing option", "Invalid option %s" %(sys.argv[idx]))

			elif sys.argv[idx][:1] == "-":
				if sys.argv[idx] in DEF_OPS:
					# "-u", "-U", "-p", "-t", "-k"
					options[sys.argv[idx]], idx = sys.argv[idx + 1], idx + 1
				else:
					utils.die("Error while parsing option", "Invalid option %s" %(sys.argv[idx]))
				
			else:
				URL  = sys.argv[idx]
				
		idx += 1
	
	if not URL:
		utils.printf("An URL is required", "bad")
		sys.exit(1)
		
	else:
		URL = checkURL(URL)
		utils.printf(utils.start_banner(URL, options, MODE, r_options), "good")
		options, r_options = checkOption(options, r_options)

		return URL, options, MODE, r_options
