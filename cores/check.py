from cores.actions import lread, fread
from utils.utils import die

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

def check_url(url):
	try:
		# Shorter startswith https://stackoverflow.com/a/20461857
		if not url.startswith(("http://", "https://")):
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