import random, sys, utils, re

'''
def subaction_getFileLineNumber(srcFilePath):
	############################################
	#	Return number of lines / wordlist count
	#	Need to be tested more
	#	Can not use File Object as Argv, return None Object
	#	Comparing len() and count() performance?
	#
	##################################################

	objFileRead = open(srcFilePath, 'r')
	#retNumberOfLines = len(objFileRead.read().split('\n'))
	retNumberOfLines = len(objFileRead.readlines())
	objFileRead.close()
	return retNumberOfLines
'''

def subaction_countListSize(lstListData):
	return len(lstListData)

def action_getUserAgent(path = "user_agents.txt"):
	##########################################
	#	Return random User Agents from file
	#
	##########################################

	objGetUserAgent = open(path, 'r')
	listUserAgent = objGetUserAgent.read().split('\n')
	objGetUserAgent.close()
	return random.choice(listUserAgent)


def action_getFormInformation(objBrowserForm):
	##########################################
	#	Get Login Form Information
	#	Need form ID for select_form(nr = ID)
	#	Username field's name for submiting
	#	Password field's name for submiting
	#
	###########################################

	# Using for loop for getting
	retFormID = 0

	regTextField = r"TextControl\W(.*)="
	regPassField = r"PasswordControl\W(.*)="
	# Start counting forms loop
	for idxSingleForm in objBrowserForm:
		try:
			retTextField = re.findall(regTextField, str(idxSingleForm), re.MULTILINE)[0]
			retPassField = re.findall(regPassField, str(idxSingleForm), re.MULTILINE)[0]
			objBrowserForm.close()
			return retFormID, retTextField, retPassField
		except:
			retFormID += 1
	return None

def action_testFormInformation(objBrowserForm):
	retData = action_getFormInformation(objBrowserForm)
	if not retData:
		sys.exit(utils.craft_msg("Can not find login form", "bad"))
	return retData

def actionGetListData(varUsername):
	#################################
	#	split input username to a list
	#	username -> [username]
	#	user1:user2 -> [user1, user2]
	#
	##################################

	return varUsername.split(':')

def actionGetFileData(srcDataPath):
	###################################
	#	Read and return data file
	#
	###################################
	try:
		objOpenFileData = open(srcDataPath, 'r')
		#retData = objOpenFileData.readlines()
		#objOpenFileData.close()
		return objOpenFileData
	except:
		sys.exit(utils.craft_msg("Can not read file %s" %(srcDataPath), 'bad'))
