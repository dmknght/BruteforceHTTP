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
DEF_WORDLIST = ("default", "router", "unix", "tomcat", "cctv", "mirai", "http", "webshell")


r_options = {
	"--proxy": False,
	"--report": False,
	"--verbose": False,
}

def checkURL(url):
	try:
		if "http" not in url:
			url = "http://%s" %(url)
		# if url[-1] != "/":
		# 	url += "/"
		return url
		
	except:
		return None
	
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
			utils.die("Argument error", "Threads must be > 1")
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
		try:
			import data
			r_options["--proxy"] = actions.fread("%s/liveproxy.txt" %(data.__path__[0]))
		except Exception as err:
			utils.printf("Argument error", err)
	
	return finalOption, r_options


def getUserOptions():
		
	global URL, MODE, r_options, DEF_WORDLIST
	
	# Default operation modes:
	#	--brute: brute force
	#	--sqli: sql injection bypass login (TODO)
	#	--httpauth: http basic authentication
	
	DEF_R_MODE = ("--brute", "--sqli", "--httpauth")
	
	# Default running mode:
	#	--verbose: display informations
	#	--report: create task report
	#	--proxy: Running using proxy
		
	# Default options:
	#	-u: Read userlist from file
	#	-p: Read passlit from file
	#	-U: Read username / userlist directly from argument
	#	-t: Number of threads using
	#	-k: Set key for false condition (for special cases)
	
	# Default wordlist: default, router, unix, tomcat, cctv, mirai, http
		
	options = {
		"-u": "default",
		"-p": "default",
		"-t": 16,
		"-k": None,
		"-U": None,
	}
	
	GETPROXY = False
	
	########### STARTING ##################
	
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
				if sys.argv[idx] in r_options.keys():
					# --verbose", "--report", "--proxy"
					r_options[sys.argv[idx]] = True

				elif sys.argv[idx] in DEF_R_MODE:
					# "--brute", "--sqli", "--httpauth"
					MODE = sys.argv[idx]
					
				elif sys.argv[idx] == "--list":
					# Wordlist provided
					if sys.argv[idx + 1] in DEF_WORDLIST:
						options["-u"], options["-p"], idx = sys.argv[idx + 1], sys.argv[idx + 1], idx + 1
					else:
						utils.die("Error while parsing arguments", "Invalid wordlist %s" %(sys.argv[idx + 1]))
				
				elif sys.argv[idx] == "--getproxy":
					GETPROXY = True

				else:
					utils.die("Error while parsing arguments", "Invalid option %s" %(sys.argv[idx]))

			elif sys.argv[idx][:1] == "-":
				if sys.argv[idx] in options.keys():
					# "-u", "-U", "-p", "-t", "-k"
					options[sys.argv[idx]], idx = sys.argv[idx + 1], idx + 1
				else:
					utils.die("Error while parsing arguments", "Invalid option %s" %(sys.argv[idx]))
				
			else:
				URL  = sys.argv[idx]
				
		idx += 1
	
	
	URL = checkURL(URL)

	if GETPROXY:
		# TODO Auto brute using proxy after get new proxy
		# TODO New help banner
		
		from extras import getproxy

		try:
			threads = int(options["-t"])
		except Exception as err:
			utils.die("GetProxy: Error while parsing arguments", err)
			
		getproxy.main(URL, threads, r_options["--verbose"])
		
		
		# GET NEW PROXY LIST ONLY
		if not URL:
			sys.exit(0)
		# else: CHECK PROXY TO TARGET DONE, AUTO ATTACK?
		# 	r_options["--proxy"] == True		

	if not URL:
		utils.die("Error while parsing arguments", "Invalid URL")
	utils.printf(utils.start_banner(URL, options, MODE, r_options), "good")
	options, r_options = checkOption(options, r_options)

	return URL, options, MODE, r_options
