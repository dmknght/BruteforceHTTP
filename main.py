###############################################
#	parse user's options from Argv
#	Argv information to Brute Forcing object
#	Best analysis options for using?
#	automatically something, optional options
#
#############################################3

import sys, actions, httpbrute, utils

srcUsrList = 'userlist.txt'
srcPassList = 'passlist.txt'
varTargetURL = ''
userlist = actions.actionGetDataFile(srcUsrList)
passlist = actions.actionGetDataFile(srcPassList)

infUserOptions = '''
Target: TARGETURL
userlist: DEFAULT
passlist: DEFAULT
'''

if len(sys.argv) == 1:
	utils.print_help()
	sys.exit(0)

elif len(sys.argv) == 2:
	if sys.argv[1] == '-h' or sys.argv[1] == '--help':
		utils.print_help()
		sys.exit(0)
	else:
		varTargetURL = sys.argv[1]
else:
	idxArgOpt = 1
	while idxArgOpt < len(sys.argv):
		if sys.argv[idxArgOpt] == '-U':
			userlist = actions.actionGetDataList(sys.argv[idxArgOpt + 1])
			infUserOptions = infUserOptions.replace("userlist: DEFAULT", "userlist: %s" %(userlist))
			idxArgOpt += 1
		elif sys.argv[idxArgOpt] == '-u':
			userlist = actions.actionGetDataFile(sys.argv[idxArgOpt + 1])
			infUserOptions = infUserOptions.replace("userlist: DEFAULT", "userlist: %s" %(sys.argv[idxArgOpt + 1]))
			idxArgOpt += 1
		elif sys.argv[idxArgOpt] == '-p':
			infUserOptions = infUserOptions.replace("passlist: DEFAULT", "userlist: %s" %(sys.argv[idxArgOpt + 1]))
			passlist = actions.actionGetDataFile(sys.argv[idxArgOpt + 1])
			idxArgOpt += 1
		else:
			varTargetURL = sys.argv[idxArgOpt]
		idxArgOpt += 1

infUserOptions = infUserOptions.replace('TARGETURL', varTargetURL)
print(infUserOptions)
processBruteForcing = httpbrute.BruteForcing(varTargetURL, userlist, passlist)
processBruteForcing.actBruteForce()