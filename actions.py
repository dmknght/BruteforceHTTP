import random, sys, utils, re

def subaction_countListSize(objInputData):
	#	Return length of a file object or list
	if type(objInputData) == file:
		return len(objInputData.readlines())
	elif type(objInputData) == list:
		return len(objInputData)

def action_getUserAgent(path = "user_agents.txt"):
	##########################################
	#	Return random User Agents from file
	#
	##########################################

	objDataUserAgent = open(path, 'r')
	retUserAgent = random.choice(objDataUserAgent.read().split('\n'))
	objDataUserAgent.close()
	return retUserAgent


def action_getFormInformation(objBrowserForm):
	##########################################
	#	Get Login Form Information
	#	Need form ID for select_form(nr = ID)
	#	Username field's name for submiting
	#	Password field's name for submiting
	#
	#	*** NEED IMPROVE ***
	#
	###########################################

	# Using for loop for getting
	retFormID = 0

	regTextField = r"TextControl\W(.*)="
	regPassField = r"PasswordControl\W(.*)="

	# Find login form
	for idxSingleForm in objBrowserForm:
		try:
			#retTextField = re.findall(regTextField, str(idxSingleForm).encode('utf-8'), re.MULTILINE)[0]
			#retPassField = re.findall(regPassField, str(idxSingleForm).encode('utf-8'), re.MULTILINE)[0]
			retTextField = re.findall(regTextField, str(idxSingleForm), re.MULTILINE)[0]
			retPassField = re.findall(regPassField, str(idxSingleForm), re.MULTILINE)[0]
			#objBrowserForm.close() #This is seems useless
			return retFormID, retTextField, retPassField
		except:
			retFormID += 1
	return None

def actionGetListData(optListUsername):
	#################################
	#	split input username to a list
	#	username -> [username]
	#	user1:user2 -> [user1, user2]
	#
	##################################

	return optListUsername.split(':')

def actionGetFileData(pathFileLocation):
	###################################
	#	Read and return data file
	#	Return file object instead of list
	#
	###################################
	try:
		objFileRead = open(pathFileLocation, 'r')
		return objFileRead
	except:
		utils.printf("Can not read file %s" %(pathFileLocation), 'bad')
		sys.exit(1)
