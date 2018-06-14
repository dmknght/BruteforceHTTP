#!/usr/bin/python

import sys, threading, time#, itertools
	
try:
	import mechanize, re
except ImportError as error:
	print(error)
	_, missing_moudle, _ = str(error).split("'")
	sys.exit("Try: sudo apt install python-%s" %(missing_moudle))
	
try:
	import actions, utils, httpbrute, options
except ImportError as error:
	print(error)
	sys.exit("Missing core module!")

def main(setTargetURL, setUserlist, setPasslist, setNumberThreads):

	try:
		sizePasslist = actions.getObjectSize(setPasslist)

	except:
		#utils.printf("Can not get size of passlist", "bad")
		pass

	timeStarting = time.time()

	workers = []

	try:
		#lock = threading.Lock()
		#lock.acquire()
		#	Create thread list
		#usePasslist = list(itertools.islice(setPasslist, sizePasslist))
		usePasslist = setPasslist.readlines()

		for i in xrange(setNumberThreads):
			worker = threading.Thread(
				target = httpbrute.handle,
				args = (setTargetURL, setUserlist, usePasslist, sizePasslist)
			)
			# add threads to list
			workers.append(worker)
	except:
		utils.printf("Error while creating threads")

		#	Start all threads
	try:
		for worker in workers:
			worker.daemon = True
			worker.start()

	#except (KeyboardInterrupt, SystemExit):
	except KeyboardInterrupt:# as error:
		# for worker in workers:
		# 	worker.join()
		utils.die("Terminated by user!", KeyboardInterrupt)
		
	except SystemExit:# as error
		utils.die("Terminated by system!", SystemExit)

	except Exception as error:
		utils.die("Error while running", error)

	finally:
		try:
			for worker in workers:
				worker.join()
		except:
			pass
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
	setTargetURL, setUserlist, setPasslist, setNumberThreads = options.getUserOptions()
	main(setTargetURL, setUserlist, setPasslist, setNumberThreads)