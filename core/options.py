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
USERLIST = "default"
PASSLIST = "default"
THREADS = 16
KEY_FALSE = None
MODE = "--brute"

r_options = {
	"--proxy": False,
	"--result": False,
	"--verbose": False,
}

def checkOption(url, options, r_options):
	
	finalOption = {}
	global MODE
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
		
	if r_options["--proxy"]:
		r_options["--proxy"] = actions.getProxyList()
	
	return url, finalOption, r_options


def getUserOptions():
	
	global URL, USERLIST, PASSLIST, THREADS, KEY_FALSE, MODE, r_options
	
	# Default operation modes:
	#	--brute: brute force
	#	--sqli: sql injection bypass login (TODO)
	#	--basic: http basic authentication (TODO)
	
	DEF_A_MODE = ("--brute", "--sqli", "--basic")
	
	# Default running mode:
	#	--verbose: display informations (TODO)
	#	--result: creating log file (TODO)
	#	--proxy: Running using proxy
	
	DEF_R_MODE = ("--verbose", "--result", "--proxy")
	
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
			sys.exit(0)
			
		else:
			if sys.argv[idx][:2] == "--":
				if sys.argv[idx] in DEF_R_MODE:
					# --verbose", "--result", "--proxy"
					r_options[sys.argv[idx]] = True

				elif sys.argv[idx] in DEF_A_MODE:
					# "--brute", "--sqli", "--basic"
					MODE = sys.argv[idx]
				else:
					utils.die("Error while parsing option", "Invalid option %s" %(sys.argv[idx]))

			elif sys.argv[idx][:1] == "-":
				if sys.argv[idx] in DEF_OPS:
					# "-u", "-U", "-p", "-t", "-k"
					options[sys.argv[idx]] = sys.argv[idx + 1]
					idx += 1
				else:
					utils.die("Error while parsing option", "Invalid option %s" %(sys.argv[idx]))
				
			else:
				URL  = sys.argv[idx]
				
		idx += 1
	
	if not URL:
		utils.printf("An URL is required", "bad")
		sys.exit(1)
	else:
		utils.printf(craftbanner(URL, options, MODE, r_options), "good")
		URL, options, r_options = checkOption(URL, options, r_options)

		return URL, options, MODE, r_options


def craftbanner(url, options, mode, r_options):
	usr = options["-U"] if options["-U"] else options["-u"]

	banner = """
	  =================================================================
	/  Target: %-56s \\
	|++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|
	|  Users: %-58s |
	|  Password: %-55s |
	|++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|
	|                                                                    |
	|      Attack mode: %-6s |   Using Proxy: %-6s |   Threads: %-4s |
	|                                                                    |
	|--------------------------------------------------------------------|
	|          Verbose: %-13s  |          Save Log: %-12s |
	|--------------------------------------------------------------------|
	\\       False keyword: %-44s /
	  =================================================================
	""" %(url,
		usr,
		options["-p"],
		mode.replace("--", ""),
		r_options["--proxy"],
		options["-t"],
		r_options["--verbose"],
		r_options["--result"],
		options["-k"]
	)
	
	return banner.replace("\t", "  ")