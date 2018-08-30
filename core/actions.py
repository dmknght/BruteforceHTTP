import random, sys, utils, re, string

def getRootDir(pathModuleLocation):
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

def randomFromList(listData):
	return random.choice(listData)

def randomFromFile(path):
	##########################################
	#	Return random User Agents from file
	#
	##########################################

	loadData = fread(path).split("\n")
	retData = randomFromList(loadData)
	return retData
	
def getUserAgent():
	path = "data/user_agents.txt"
	return randomFromFile(path)
	
def getProxyAddr():
	path = "data/liveproxy.txt"
	return randomFromFile(path)

def startBrowser():
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

def lread(optListUsername):
	#################################
	#	split input username to a list
	#	username -> [username]
	#	user1:user2 -> [user1, user2]
	#
	##################################

	return optListUsername.split(':')

def fload(pathFileLocation):
	###################################
	#	Read and return data file
	#	Return file object instead of list
	#
	###################################
	try:
		objFileRead = open(pathFileLocation, 'r')
		return objFileRead
	except Exception as error:
		utils.die("Error while loading file!", error)
		
def fread(pathFileLocation):
	try:
		retObj = fload(pathFileLocation)
		return retObj.read()
	except Exception as error:
		utils.die("Error while reading data", error)
	finally:
		try:
			retObj.close()
		except:
			pass

def fwrite(pathFileLocation, writeData):
	try:
		objFileWrite = open(pathFileLocation, "w'")
		objFileWrite.write(writeData)
		objFileWrite.close()
	except Exception as error:
		utils.die("Error while writing data", error)

def randomString(min = 2, max = 5):
	#https://stackoverflow.com/a/2257449
	charset = string.lowercase + string.uppercase
	return ''.join(random.choice(charset) for _ in xrange(min, max))

	
if __name__ == "__main__":
	utils.die("Oops! Wrong place", "Find other place")
	