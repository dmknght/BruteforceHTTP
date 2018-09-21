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

def main(setTargetURL, setOptions, setMode, setRunOptions):
	
	"""
	if setUserlist and setPasslist is file (actions.fload())
	do httpbrute(setUserlist.readlines(), setPasslist.readlines(),) is very good for threading
	#BUG:
	setUserlist, setPasslist = setUserlist.readlines(), setPasslist.readlines() does not work
	#Testing with list
	"""
	# BUG
	"""
		Setting threading with big number
		split jobs for threading
		Memory management
	"""
	
	setUserlist, setThreads, setKeyFalse, setPasslist = setOptions.values()
	#setProxy, setVerbose, setLog = setRunOptions.values()

	# try:
	# 	sizePasslist = actions.size_o(setPasslist)
	# 	sizeUserlist = actions.size_o(setUserlist)
	# 	# TODO Check condition each case
	# 
	# except:
	# 	#utils.printf("Can not get size of passlist", "bad")
	# 	pass
		
	try:
		setUserlist = setUserlist.split("\n")
	except:
		#setUserlist = setUserlist.readlines()
		pass

	# TODO Must testing cases with list and file object
	try:
		setPasslist = setPasslist.split("\n")
	except:
		pass
	
	
	## End of testing
	
	# TODO: check network, form before creating tasks

	timeStarting = time.time()

	try:
		
		#TODO modify for sql injection mode
		if setMode == "--sqli":
			pass
			# for i in xrange(setThreads):
			# 	worker = threading.Thread(
			# 		target = sqltest.handle,
			# 		args = (setTargetURL, setUserlist, setPasslist, sizeUserlist * sizePasslist, setProxy, setKeyFalse)
			# 	)
			# 	# add threads to list
			# 	workers.append(worker)
		else:
			#httpbrute.handle(setTargetURL, setUserlist, setPasslist, sizePasslist, setProxy, setKeyFalse)
			httpbrute.handle(setTargetURL, setUserlist, setPasslist, setKeyFalse, setThreads, setRunOptions)

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
			setPasslist.close()
		except:
			pass
		try:
			setUserlist.close()
		except:
			pass

		sys.exit(0)

if __name__ == "__main__":
	current_dir = actions.getRootDir(sys.argv[0])
	if current_dir:
		os.chdir(current_dir)
	main(*options.getUserOptions())