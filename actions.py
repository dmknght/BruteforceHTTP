import random, sys, utils, re

def subaction_countListSize(lstListData):
	#	Return length of a list

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
			retTextField = re.findall(regTextField, str(idxSingleForm), re.MULTILINE)[0]
			retPassField = re.findall(regPassField, str(idxSingleForm), re.MULTILINE)[0]

			#objBrowserForm.close() #This is seems useless
			return retFormID, retTextField, retPassField
		except:
			retFormID += 1
	return None

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
	#	Return file object instead of list
	#
	###################################
	try:
		objOpenFileData = open(srcDataPath, 'r')
		return objOpenFileData
	except:
		sys.exit(utils.craft_msg("Can not read file %s" %(srcDataPath), 'bad'))
