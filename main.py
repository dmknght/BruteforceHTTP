#!/usr/bin/python

###############################################
#	Parse user's options from Argv
#	Create Brute forcing object
#	Start method
#	Clear object
#	Print result
#
##############################################

import sys, actions, httpbrute, utils, time


##############################################
#	Create default options
#
############################################

srcUsrList = 'userlist.txt'
srcPassList = 'passlist.txt'
varTargetURL = ''

infUserOptions = '''
Target: TARGETURL
userlist: DEFAULT
passlist: DEFAULT
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
		varTargetURL = sys.argv[1]
		#############################################
		#	open file here -> no delay for print help
		#############################################
		userlist = actions.actionGetFileData(srcUsrList)
		passlist = actions.actionGetFileData(srcPassList)

else:
	###########################################
	#	Get user options
	#	Replace default options
	#	**NEED IMPROVE**
	#
	###########################################

	userlist = actions.actionGetFileData(srcUsrList)
	passlist = actions.actionGetFileData(srcPassList)
	try:
		idxArgOpt = 1
		while idxArgOpt < len(sys.argv):

			#	Choose custom username
			if sys.argv[idxArgOpt] == '-U':
				userlist = actions.actionGetListData(sys.argv[idxArgOpt + 1])
				infUserOptions = infUserOptions.replace("userlist: DEFAULT", "userlist: %s" %(userlist))
				idxArgOpt += 1

			#	Choose custom userlist
			elif sys.argv[idxArgOpt] == '-u':
				userlist = actions.actionGetFileData(sys.argv[idxArgOpt + 1])
				infUserOptions = infUserOptions.replace("userlist: DEFAULT", "userlist: %s" %(sys.argv[idxArgOpt + 1]))
				idxArgOpt += 1

			#	Choose custom passlist
			elif sys.argv[idxArgOpt] == '-p':
				infUserOptions = infUserOptions.replace("passlist: DEFAULT", "passlist: %s" %(sys.argv[idxArgOpt + 1]))
				passlist = actions.actionGetFileData(sys.argv[idxArgOpt + 1])
				idxArgOpt += 1

			#	Possible URL
			else:
				varTargetURL = sys.argv[idxArgOpt]
			idxArgOpt += 1

	except:
		sys.exit(utils.craft_msg("Parsing arguments error", "bad"))

##########################
#	CHECK REQUIRED OPTIONS
#
##########################

if not varTargetURL:
	sys.exit(utils.craft_msg("An URL is required", "bad"))
else:
	infUserOptions = infUserOptions.replace('TARGETURL', varTargetURL)


###########################################
#	print option information before running
#
###########################################

print(infUserOptions)

timeStarting = time.time()

try:
	#	create object
	processBruteForcing = httpbrute.BruteForcing(varTargetURL, userlist, passlist)

	utils.printf("Starting...\n")

	# Calling method
	processBruteForcing.run()

except KeyboardInterrupt:
	utils.printf("Terminated!!!", "bad")

finally:
	############################################
	#	Get result
	#
	############################################

	try:
		creds = processBruteForcing.actGetResult()

		#	check result
		if len(creds) == 0:
			utils.printf("Password not found!", "bad")
		else:
			utils.printf("")
			utils.print_table(("Username", "Password"), *creds)
	except:
		#utils.printf("\nCan not get result.\n", "bad")
		pass

	utils.printf("\nCompleted. Run time: %0.5s [s]\n" %(time.time() - timeStarting), "good")

	########################################
	#	Clear resources
	#
	########################################

	try:
		passlist.close()
	except:
		pass
	try:
		userlist.close()
	except:
		pass

	sys.exit(0)