from cores.actions import lread, fread
from utils.utils import die, printf
import re, sys

reload(sys)
sys.setdefaultencoding('utf8')

# def check_import():
# 	try:
# 		import sys, threading, os, ssl, time
# 		import mechanize, re

# 	except ImportError as error:
# 		print(error)
# 		print("Please install libraries")
# 		return False

# 	try:
# 		from core import actions, utils, tbrowser, options
# 		from modules import loginbrute, httpget
# 		from extras import getproxy, reauth
# 		import data, reports
	
# 	except Exception as error:
# 		print("Can't find project's module")
# 		print(error)
# 		return False


def checkHTTPGetLogin(strHeader):
	reg = r"WWW-Authenticate: Basic realm=\"(.*)\""
	try:
		return re.findall(reg, strHeader, re.MULTILINE)[0]
	except:
		return False

def parseLoginForm(allFormControl):
	# Try detect login form from all forms in response. Return form information
	reTextControl = r"TextControl\W(.*)="
	rePasswdControl = r"PasswordControl\W(.*)="
	reSubmitControl = r"SubmitControl\W(.*)="

	for uint_formID, form in enumerate(allFormControl):
		txtPasswdControl = re.findall(rePasswdControl, str(form))
		# Find password control. If has
		# 	1 password control -> login field
		# 	2 or more password control -> possibly register field
		if len(txtPasswdControl) == 1:
			txtTextControl = re.findall(reTextControl, str(form))
			txtSubmitControl = re.findall(reSubmitControl, str(form))
			txtSubmitControl = ["None"] if not txtSubmitControl else txtSubmitControl
			if len(txtTextControl) == 1:
				# Regular login field. > 1 can be register specific field (maybe captcha)
				return ([uint_formID, txtSubmitControl[0]], [txtPasswdControl[0], txtTextControl[0]])
			elif len(txtTextControl) == 0:
				# Possibly password field login only
				return ([uint_formID, txtSubmitControl[0]], [txtPasswdControl[0]])
	return None

def check_sqlerror(response):
	# Parse html response to define SQL error
	# Copyright: SQLmap
	if re.search(r"SQL (warning|error|syntax)", response):
		return True
	return False
	# TODO improve condition

def check_login(options):
	try:
		from libs.mbrowser import mBrowser
		# from libs.sbrowser import sBrowser
		
		proc = mBrowser(options.timeout)
		
		resp = proc.open_url(options.url)
		"""
			Check URL type. If Website directs to other URL,
			options.url is website's panel
			else: it is login url.
			Example: options.url = site.com/wp-admin/ -> panel
				site directs user to wp-login -> login URL
				options.url = site.com/wp-login.php -> login URL
		"""
		if proc.geturl() != options.url:
			printf("[*] Website moves to: ['%s']" %(proc.geturl()), "norm")
			options.panel_url, options.login_url = options.url, proc.geturl()
		else:
			options.login_url = options.url

		# printf("[*] Connect success!", "good")
		options.attack_mode = "--loginbrute"
		if options.run_options["--verbose"]:
			printf("[*] %s" %(proc.get_title()), "norm")
		# printf("[+] Analyzing login form....")
		loginInfo = parseLoginForm(proc.forms())
		
		# Check target login page with selenium
		# jscheck = sBrowser()
		# jscheck.open_url(options.url)
		
		# # Convert data to mechanize to analysis form (easier)
		# r_jscheck = str(jscheck.get_resp())
		# resp.set_data(r_jscheck)
		# proc.set_response(resp)

		# # Get new info
		# js_loginInfo = parseLoginForm(proc.forms())
		# if not loginInfo and js_loginInfo:
		# 	options.engine = "selenium"
		# 	loginInfo = js_loginInfo

		return loginInfo
		
	except Exception as error:
		try:
			if error.code == 401:
				## GET INFORMATION
				resp_header = str(proc.response().info())
				if "WWW-Authenticate" in resp_header:
					loginID = checkHTTPGetLogin(resp_header)
					loginInfo = (loginID, ["Password", "User Name"])
					if options.verbose:
						printf("[+] Using HTTP GET Authentication mode", "norm")
					options.attack_mode = "--httpget"
				else:
					loginInfo = False
			else:
				loginInfo = False
				printf("[x] Target check: %s" %(error), "bad")

		# Error != http code
		except:
			loginInfo = False
			die("[x] Target check:", error)
	
	except KeyboardInterrupt:
		loginInfo = False
	
	finally:
		proc.close()
		# jscheck.close()
		return loginInfo

def check_url(url):
	try:
		# Shorter startswith https://stackoverflow.com/a/20461857
		"""
			ftp://something.com
			https://something.com
		"""
		if "://" in url:
			if not url.startswith(("http://", "https://")):
				die("[x] URL error", "Invalid protocol")
		else:
			"Something.com"
			url = "http://%s" %(url)
	except:
		url = None
	return url

def check_options(options):
	"""
		This function checks main options before create tasks, ...
	"""
	# Read URL from list (file_path) or get URL from option
	try:
		options.target = fread(options.options["-l"]).split("\n") if options.options["-l"] else [options.url]
		options.target = filter(None, options.target)
	except Exception as error:
		die("[x] Options: URL error", error)
		# CHECK threads option
	try:
		options.threads = int(options.options["-t"])
		if options.threads < 1:
			die(
				"[x] Options: Invalid option \"threads\"",
				"Thread number must be larger than 1"
			)
	except Exception as error:
		die(
			"[x] Options: Invalid option \"threads\"",
			error
		)

	# CHECK timeout option
	try:
		options.timeout = int(options.options["-T"])
		if options.timeout < 1:
			die(
				"[x] Options: Invalid option \"timeout\"",
				"Thread number must be larger than 1"
			)
	except Exception as error:
		die(
			"[x] Options: Invalid option \"timeout\"",
			error
		)
	if options.attack_mode == "--sqli":
		options.options["-u"], options.options["-p"] = "sqli", "sqli"

def check_tasks(options, loginInfo):

	"""
		This fucntion check options for each brute force task
	"""
	
	_, formField = loginInfo
	import data

	# CHECK username list options
	if len(formField) == 1:
		options.username = [""]
	elif options.options["-U"]:
		options.username = list(set(lread(options.options["-U"])))
	else:
		if options.options["-u"] in options.WORDLISTS:
			if options.options["-u"] == "sqli":
				options.username = tuple(eval("data.%s_user()" %(options.options["-u"])))
			else:
				options.username = tuple(eval("data.%s_user()" %(options.options["-u"])).replace("\t", "").split("\n"))
		else:
			options.username = tuple(fread(options.options["-u"]).split("\n"))
			options.username = filter(None, options.username)
	
	# CHECK passlist option
	if options.options["-p"] in options.WORDLISTS:
		options.passwd = tuple(eval("data.%s_pass()" %(options.options["-p"])).replace("\t", "").split("\n"))
	else:
		options.passwd = tuple(fread(options.options["-p"]).split("\n"))
		options.passwd = filter(None, options.passwd)


	options.report = options.run_options["--report"]
	options.verbose = options.run_options["--verbose"]