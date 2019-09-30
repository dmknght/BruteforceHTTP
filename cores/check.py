from cores.actions import to_list, file_read
from utils import events
import re, sys


# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

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
	try:
		# Try detect login form from all forms in response. Return form information
		reTextControl = r"text\((.*)\)"
		reMailControl = r"email\((.*)\)"
		rePasswdControl = r"password\((.*)\)"
		reSubmitControl = r"submit\((.*)\)"
		
		formData = None
		
		for uint_formID, form in enumerate(allFormControl):
			# if not form:
			# 	return False
			txtPasswdControl = re.findall(rePasswdControl, form)
			# Find password control. If has
			# 	1 password control -> login field
			# 	2 or more password control -> possibly register field
			if len(txtPasswdControl) == 1:
				txtTextControl = re.findall(reTextControl, form)
				txtMailControl = re.findall(reMailControl, form)
				txtTextControl = txtTextControl if txtTextControl else txtMailControl
				txtSubmitControl = re.findall(reSubmitControl, form)
				txtSubmitControl = ["None"] if not txtSubmitControl else txtSubmitControl
				if len(txtTextControl) == 1:
					# Regular login field. > 1 can be register specific field (maybe captcha)
					formData = ([uint_formID, txtSubmitControl[0]], [txtPasswdControl[0], txtTextControl[0]])
				elif len(txtTextControl) == 0:
					# Possibly password field login only
					formData = ([uint_formID, txtSubmitControl[0]], [txtPasswdControl[0]])
				return formData
		return False
	except AttributeError:
		return False


def check_login(options):
	try:
		from cores.browser import Browser
		
		proc = Browser()
		
		resp = proc.open_url(options.url)
		"""
			Check URL type. If Website directs to other URL,
			options.url is website's panel
			else: it is login url.
			Example: options.url = site.com/wp-admin/ -> panel
				site directs user to wp-login -> login URL
				options.url = site.com/wp-login.php -> login URL
		"""
		if proc.url() != options.url:
			events.info("Website moves to: ['%s']" % (proc.url()))
			options.panel_url, options.login_url = options.url, proc.url()
		else:
			options.login_url = options.url
		
		options.attack_mode = "--loginbrute"
		if options.run_options["--verbose"]:
			events.info("%s" % (proc.get_title()), "TITLE")
		if resp.status_code == 401:
			if "WWW-Authenticate" in resp.headers:
				loginID = checkHTTPGetLogin(resp.headers)
				loginInfo = (loginID, ["Password", "User Name"])
				if options.verbose:
					events.info("HTTP GET login")
				options.attack_mode = "--httpget"
			else:
				loginInfo = False
		else:
			loginInfo = parseLoginForm(proc.forms())
			options.txt = resp.content
		
		return loginInfo
	
	except Exception as error:
		loginInfo = False
		events.error("%s" % (error), "TARGET")
		sys.exit(1)
	
	except KeyboardInterrupt:
		loginInfo = False
	
	finally:
		try:
			proc.close()
		except:
			pass
	# try:
	# 	jscheck.close()
	# except:
	# 	pass
	# return loginInfo


def check_url(url):
	try:
		# Shorter startswith https://stackoverflow.com/a/20461857
		"""
			ftp://something.com
			https://something.com
		"""
		if "://" in url:
			if not url.startswith(("http://", "https://")):
				events.error("Invalid URL format")
				sys.exit(1)
		else:
			"Something.com"
			url = "http://%s" % (url)
		if len(url.split("/")) <= 3:
			url = "%s/" % (url) if url[-1] != "/" else url
	except:
		url = None
	return url


def check_options(options):
	"""
		This function checks main options before create tasks, ...
	"""
	# Read URL from list (file_path) or get URL from option
	options.report = options.run_options["--report"]
	options.verbose = options.run_options["--verbose"]
	try:
		options.target = file_read(options.options["-l"]).split("\n") if options.options["-l"] else [options.url]
		options.target = list(filter(None, options.target))
	except Exception as error:
		events.error("%s" % (error))
		sys.exit(1)
	# CHECK threads option
	try:
		options.threads = int(options.options["-t"])
		if options.threads < 1:
			events.error("Thread must be larger than 1")
	
	except Exception as error:
		events.error("%s" % (error))
		sys.exit(1)
	
	# CHECK timeout option
	# try:
	# 	options.timeout = int(options.options["-T"])
	# 	if options.timeout < 1:
	# 		utils.die("[x] Options: Invalid option \"timeout\"", "Thread number must be larger than 1")
	# except Exception as error:
	# 	utils.die("[x] Options: Invalid option \"timeout\"", error)
	
	if options.attack_mode == "--sqli":
		options.options["-u"], options.options["-p"] = "sqli", "sqli"


def check_tasks(options, loginInfo):
	"""
		This fucntion check options for each brute force task
	"""
	
	_, formField = loginInfo
	
	# CHECK username list options
	if len(formField) == 1:
		options.username = [""]
	elif options.options["-U"]:
		options.username = list(set(to_list(options.options["-U"])))
	else:
		import data
		if options.options["-u"] in options.WORDLISTS:
			if options.options["-u"] == "sqli":
				options.username = tuple(eval("data.%s_user()" % (options.options["-u"])))
			else:
				options.username = tuple(eval("data.%s_user()" % (options.options["-u"])).replace("\t", "").split("\n"))
		else:
			options.username = tuple(file_read(options.options["-u"]).split("\n"))
			options.username = tuple(filter(None, options.username))
	
	# CHECK passlist option
	if options.options["-p"] in options.WORDLISTS:
		import data
		options.passwd = tuple(eval("data.%s_pass()" % (options.options["-p"])).replace("\t", "").split("\n"))
	else:
		options.passwd = tuple(file_read(options.options["-p"]).split("\n"))
		options.passwd = tuple(filter(None, options.passwd))
	
	if "--replacement" in options.extras:
		from data.passgen import replacement
		final_passwd = ""
		for line in options.passwd:
			final_passwd += "\n".join(list(replacement(line)))
		options.passwd = final_passwd.split("\n")
	
	elif "--toggle_case" in options.extras:
		from data.passgen import toggle_case
		final_passwd = ""
		for line in options.passwd:
			final_passwd += "\n".join(list(toggle_case(line)))
		options.passwd = final_passwd.split("\n")
