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


def basic_http_request(response_header):
	"""
	Find basic HTTP LOGIN request from error 401 and response header
	:param response_header: string = header of http response from server
	:return: False or Request Realm (name)
	"""
	regex_http_get = r"WWW-Authenticate: Basic realm=\"(.*)\""
	try:
		return re.findall(regex_http_get, response_header, re.MULTILINE)[0]
	except:
		return False


def find_login_form(form_controls):
	"""
	Find login form in all form objects from response
	:param form_controls: list of string = form information
	:return: False or login form information (form_id, text_field, password_field)
	"""
	form_info = False
	try:
		# Try detect login form from all forms in response. Return form information
		regex_text_control = r"text\((.*)\)"
		regex_mail_control = r"email\((.*)\)"
		regex_password_control = r"password\((.*)\)"
		regex_submit_control = r"submit\((.*)\)"
		
		for form_id, form in enumerate(form_controls):
			password_control = re.findall(regex_password_control, form)
			# Find password control. If has
			# 	1 password control -> login field
			# 	2 or more password control -> possibly register field
			if len(password_control) == 1:
				text_control = re.findall(regex_text_control, form)
				mail_control = re.findall(regex_mail_control, form)
				text_control = text_control if text_control else mail_control
				submit_control = re.findall(regex_submit_control, form)
				submit_control = ["None"] if not submit_control else submit_control
				if len(text_control) == 1:
					# Regular login field. > 1 can be register specific field (maybe captcha)
					form_info = ([form_id, submit_control[0]], [password_control[0], text_control[0]])
				elif len(text_control) == 0:
					# Possibly password field login only
					form_info = ([form_id, submit_control[0]], [password_control[0]])
				return form_info
	except AttributeError:
		pass
	finally:
		return form_info


def find_login_request(options):
	"""
	Find and analysis login request from response
	:param options: object = options of user
	:return: False or list of string = login request information
	"""
	login_request = False
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
		if proc.get_url() != options.url:
			events.info("Website moves to: ['%s']" % (proc.get_url()))
			options.panel_url, options.login_url = options.url, proc.get_url()
		else:
			options.login_url = options.url
		
		options.attack_mode = "--loginbrute"
		if options.run_options["--verbose"]:
			events.info("%s" % (proc.get_title()), "TITLE")
		if resp.status_code == 401:
			if "WWW-Authenticate" in resp.headers:
				login_id = basic_http_request(resp.headers)
				login_request = (login_id, ["Password", "User Name"])
				if options.verbose:
					events.info("HTTP GET login")
				options.attack_mode = "--httpget"
		
		else:
			login_request = find_login_form(proc.forms())
			options.txt = resp.content
	
	except KeyboardInterrupt:
		pass
	
	except Exception as error:
		events.error("%s" % (error), "TARGET")
		sys.exit(1)
	
	finally:
		try:
			proc.close()
		except:
			pass
		return login_request


def check_url(url):
	"""
	Check if url has valid format or fix it
	:param url: string = url from option user gives
	:return: string = url with valid format or False
	"""
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
			url = "http://" + url
		if len(url.split("/")) <= 3:
			url = url + "/" if url[-1] != "/" else url
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
