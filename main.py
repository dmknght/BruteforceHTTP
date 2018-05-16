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

pathDefaultUserlist = 'userlist.txt'
pathDefaultPasslist = 'passlist.txt'
optionTargetURL = ''

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
		optionUserlist = actions.actionGetFileData(pathDefaultUserlist)
		optionPasslist = actions.actionGetFileData(pathDefaultPasslist)

else:
	###########################################
	#	Get user options
	#	Replace default options
	#	**NEED IMPROVE**
	#
	###########################################

	optionUserlist = actions.actionGetFileData(pathDefaultUserlist)
	optionPasslist = actions.actionGetFileData(pathDefaultPasslist)
	try:
		index = 1
		while index < len(sys.argv):

			#	Choose custom username
			if sys.argv[index] == '-U':
				optionUserlist = actions.actionGetListData(sys.argv[index + 1])
				infoUserOptions = infoUserOptions.replace(
					"optionUserlist: DEFAULT", "optionUserlist: %s" %(optionUserlist)
				)
				index += 1

			#	Choose custom optionUserlist
			elif sys.argv[index] == '-u':
				optionUserlist = actions.actionGetFileData(sys.argv[index + 1])
				infoUserOptions = infoUserOptions.replace(
					"optionUserlist: DEFAULT", "optionUserlist: %s" %(sys.argv[index + 1])
				)
				index += 1

			#	Choose custom optionPasslist
			elif sys.argv[index] == '-p':
				infoUserOptions = infoUserOptions.replace(
					"optionPasslist: DEFAULT", "optionPasslist: %s" %(sys.argv[index + 1])
				)
				optionPasslist = actions.actionGetFileData(sys.argv[index + 1])
				index += 1

			#	Possible URL
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


###########################################
#	print option information before running
#
###########################################

print(infoUserOptions)

timeStarting = time.time()

try:
	#	create object
	processBruteForcing = httpbrute.BruteForcing(optionTargetURL, optionUserlist, optionPasslist)

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
		credentials = processBruteForcing.actGetResult()

		#	check result
		if len(credentials) == 0:
			utils.printf("Password not found!", "bad")
		else:
			utils.printf("")
			utils.print_table(("Username", "Password"), *credentials)
	except:
		#utils.printf("\nCan not get result.\n", "bad")
		pass

	utils.printf("\nCompleted. Run time: %0.5s [s]\n" %(time.time() - timeStarting), "good")

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