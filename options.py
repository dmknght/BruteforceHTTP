import sys
from core import utils, actions
##############################################
#	Parse user's options
#	Create default options
#	*MUSTDO* validate URL
#	*TODO* validate option
#
############################################

def getUserOptions():
	pathDefaultUserlist = 'data/userlist.txt'
	pathDefaultPasslist = 'data/passlist.txt'
	optionTargetURL = ''
	optionKeyFalse = ''
	optionThreads = 3
	optionProxy = False

	infoUserOptions = '''
	Target: TARGETURL
	Userlist: DEFAULT
	Passlist: DEFAULT
	'''
	################################
	#	Get user's options
	#
	################################

	if len(sys.argv) == 1:
		##############################
		#	If there is no options:
		#	print help and show how to use this script
		##############################

		utils.print_help()
		sys.exit(0)

	elif len(sys.argv) == 2:
		############################################
		#	if 1 option only:
		#		calling help
		#	else:
		#		run process with default options
		#
		############################################

		if sys.argv[1] == '-h' or sys.argv[1] == '--help':
			utils.print_help()
			sys.exit(0)
		else:
			optionTargetURL = sys.argv[1]
			#############################################
			#	open file here -> no delay for print help
			#############################################
			optionUserlist = actions.loadDataFromFile(pathDefaultUserlist)
			optionPasslist = actions.loadDataFromFile(pathDefaultPasslist)

	else:
		###########################################
		#	Get user options
		#	Replace default options
		#	**NEED IMPROVE**
		#
		###########################################

		optionUserlist = actions.loadDataFromFile(pathDefaultUserlist)
		optionPasslist = actions.loadDataFromFile(pathDefaultPasslist)
		try:
			index = 1
			while index < len(sys.argv):
				#	Choose custom username
				if sys.argv[index] == '-U':
					optionUserlist = actions.readDataFromList(sys.argv[index + 1])
					infoUserOptions = infoUserOptions.replace(
						"Userlist: DEFAULT", "Userlist: %s" %(":".join(optionUserlist))
					)
					index += 1

				#	Choose custom optionUserlist
				elif sys.argv[index] == '-u':
					optionUserlist = actions.loadDataFromFile(sys.argv[index + 1])
					infoUserOptions = infoUserOptions.replace(
						"Userlist: DEFAULT", "Userlist: %s" %(sys.argv[index + 1])
					)
					index += 1

				#	Choose custom optionPasslist
				elif sys.argv[index] == '-p':
					infoUserOptions = infoUserOptions.replace(
						"Passlist: DEFAULT", "Passlist: %s" %(sys.argv[index + 1])
					)
					optionPasslist = actions.loadDataFromFile(sys.argv[index + 1])
					index += 1

				#	Set thread
				elif sys.argv[index] == '-t':
					optionThreads = sys.argv[index + 1]
					index += 1

				elif sys.argv[index] == '-c':
					optionKeyFalse = sys.argv[index + 1]
					index += 1

				# Set proxy
				elif sys.argv[index] == "--proxy":
					try:
						optionProxy = actions.readDataFromFile("data/liveproxy.txt").split("\n")
					except:
						utils.printf("Can not read proxy list file!", "bad")
						utils.printf("Downloading proxy list automatically")
						try:
							import getproxy
							getproxy.refresh()
							optionProxy = actions.readDataFromFile("data/liveproxy.txt").split("\n")
						except Exception as error:
							utils.die("Error while getting proxy list [automatic]", error)

					#finally:
					#	optionProxy = actions.readDataFromFile("data/liveproxy.txt").split("\n")

				else:
					optionTargetURL = sys.argv[index]
				index += 1

		except Exception as error:
			utils.die("Argument error", error)

	##########################
	#	CHECK REQUIRED OPTIONS
	#
	##########################

	if not optionTargetURL:
		utils.die("An URL is required!", "Missing argument")
	else:
		infoUserOptions = infoUserOptions.replace('TARGETURL', optionTargetURL)

	if optionProxy:
		infoUserOptions += "Proxy: %s\n" %("True")
	else:
		infoUserOptions += "Proxy: %s\n" %(optionProxy)

	try:
		optionThreads = int(optionThreads)
		infoUserOptions += "\tThread[s]: %s\n" %(optionThreads)

	except Exception as error:
		utils.die("Invalid number threads", error)

	if optionKeyFalse:
		infoUserOptions += "\tFalse keyword: %s\n" %(optionKeyFalse)


	###########################################
	#	print option information before running
	#
	###########################################
	utils.printf(infoUserOptions, 'good')

	return optionTargetURL, optionUserlist, optionPasslist, optionThreads, optionProxy, optionKeyFalse