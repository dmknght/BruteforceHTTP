import sys, utils, actions
##############################################
#	Parse user's options
#	Create default options
#	*MUSTDO* validate URL
#	*TODO* validate option
#
############################################

def getUserOptions():
	pathDefaultUserlist = 'userlist.txt'
	pathDefaultPasslist = 'passlist.txt'
	optionTargetURL = ''
	optionThreads = 3

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
			optionUserlist = actions.readDataFromFile(pathDefaultUserlist)
			optionPasslist = actions.readDataFromFile(pathDefaultPasslist)

	else:
		###########################################
		#	Get user options
		#	Replace default options
		#	**NEED IMPROVE**
		#
		###########################################

		optionUserlist = actions.readDataFromFile(pathDefaultUserlist)
		optionPasslist = actions.readDataFromFile(pathDefaultPasslist)
		try:
			index = 1
			while index < len(sys.argv):
				#	Choose custom username
				if sys.argv[index] == '-U':
					optionUserlist = actions.readDataFromList(sys.argv[index + 1])
					infoUserOptions = infoUserOptions.replace(
						"optionUserlist: DEFAULT", "optionUserlist: %s" %(optionUserlist)
					)
					index += 1

				#	Choose custom optionUserlist
				elif sys.argv[index] == '-u':
					optionUserlist = actions.readDataFromFile(sys.argv[index + 1])
					infoUserOptions = infoUserOptions.replace(
						"optionUserlist: DEFAULT", "optionUserlist: %s" %(sys.argv[index + 1])
					)
					index += 1

				#	Choose custom optionPasslist
				elif sys.argv[index] == '-p':
					infoUserOptions = infoUserOptions.replace(
						"optionPasslist: DEFAULT", "optionPasslist: %s" %(sys.argv[index + 1])
					)
					optionPasslist = actions.readDataFromFile(sys.argv[index + 1])
					index += 1

				#	Possible URL
				elif sys.argv[index] == '-t':
					optionThreads = sys.argv[index + 1]
					index += 1
				else:
					optionTargetURL = sys.argv[index]
				index += 1

		except:
			sys.exit(utils.craft_msg("Parsing arguments error", "bad"))

	##########################
	#	CHECK REQUIRED OPTIONS
	#
	##########################

	if not optionTargetURL:
		sys.exit(utils.craft_msg("An URL is required", "bad"))
	else:
		infoUserOptions = infoUserOptions.replace('TARGETURL', optionTargetURL)

	try:
		optionThreads = int(optionThreads)
		infoUserOptions += "Thread[s]: %s\n" %(optionThreads)
	except:
		utils.printf("Invalid number of threads", "bad")
		sys.exit(1)


	###########################################
	#	print option information before running
	#
	###########################################
	utils.printf(infoUserOptions, 'good')

	return optionTargetURL, optionUserlist, optionPasslist, optionThreads