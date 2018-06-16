import random, sys, utils, re

def getProjectRootDirectory(pathModuleLocation):
	##################################
	#	Get root folder of module file
	#	/foo/bar/module.py
	#	---> return "/foo/bar"
	#################################
	
	pathModuleLocation = "/".join(pathModuleLocation.split("/")[:-1])
	return pathModuleLocation

def getObjectSize(objInputData):
	#	Return length of a file object or list
	if type(objInputData) == file:

		retFileSize = len(objInputData.readlines())
		objInputData.seek(0)
		return retFileSize

	elif type(objInputData) == list:
		return len(objInputData)
	elif type(objInputData) == str:
		return len(objInputData.split('\n'))

def getUserAgent(path = "data/user_agents.txt"):
	##########################################
	#	Return random User Agents from file
	#
	##########################################

	objDataUserAgent = open(path, 'r')
	retUserAgent = random.choice(objDataUserAgent.read().split('\n'))
	objDataUserAgent.close()
	return retUserAgent

def createBrowserObject():
	import mechanize
	retObject = mechanize.Browser()
	retObject.set_handle_robots(False)
	retObject.set_handle_referer(True)
	retObject.set_handle_redirect(True)
	retObject.set_handle_equiv(True)
	return retObject


def getFormInformation(objBrowserForm):
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

def readDataFromList(optListUsername):
	#################################
	#	split input username to a list
	#	username -> [username]
	#	user1:user2 -> [user1, user2]
	#
	##################################

	return optListUsername.split(':')

def readDataFromFile(pathFileLocation):
	###################################
	#	Read and return data file
	#	Return file object instead of list
	#
	###################################
	try:
		objFileRead = open(pathFileLocation, 'r')
		return objFileRead
	except Exception as error:
		utils.die("Reading file error", error)

def writeDataToFile(pathFileLocation, writeData):
	try:
		objFileWrite = open(pathFileLocation, "w'")
		objFileWrite.write(writeData)
		objFileWrite.close()
	except Exception as error:
		utils.die("Error while writing data", error)