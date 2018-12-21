import random, sys, utils, string

# def getRootDir(pathModuleLocation):
# 	##################################
# 	#	Get root folder of module file
# 	#	/foo/bar/module.py
# 	#	---> return "/foo/bar"
# 	#################################
# 
# 	pathModuleLocation = "/".join(pathModuleLocation.split("/")[:-1])
# 	return pathModuleLocation

def size_o(objInputData):
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


def lread(strUsername):
	#################################
	#	split input username to a list
	#	username -> [username]
	#	user1:user2 -> [user1, user2]
	#
	##################################

	return strUsername.split(":")

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
		objFileWrite = open(pathFileLocation, "w")
		objFileWrite.write(writeData)
	except Exception as error:
		utils.die("Error while writing data", error)
	finally:
		objFileWrite.close()

		

def fwrite_c(pathFileLocation, writeData):
	try:
		fileWrite = open(pathFileLocation, "a")
		fileWrite.write(writeData)
	except Exception as error:
		utils.die("Error while continuing write file", error)
	finally:
		fileWrite.close()

def randomString(min = 2, max = 5):
	#https://stackoverflow.com/a/2257449
	charset = string.lowercase + string.uppercase
	return ''.join(random.choice(charset) for _ in xrange(min, max))


def verify_url(options):
	try:
		if not options.url.startswith("http://"):
			options.url = "http://%s" %(options.url)
	except:
		options.url = None

def verify_options(options):
	# Check url
	import data

	# CHECK threads option
	try:
		options.threads = int(options.options["-t"])
		if options.threads < 1:
			utils.die(
				"[x] Options: Invalid option \"threads\"",
				"Thread number must be larger than 1"
			)
	except Exception as error:
		utils.die(
			"[x] Options: Invalid option \"threads\"",
			error
		)
	
	# CHECK username list options
	if options.options["-U"]:
		options.username = lread(options.options["-U"])
	else:
		if options.options["-u"] in options.WORDLISTS:
			options.username = eval("data.%s_user()" %(options.options["-u"])).replace("\t", "").split("\n")
		else:
			options.username = fread(options.options["-u"])
	
	# CHECK passlist option
	if options.options["-p"] in options.WORDLISTS:
		options.passwd = eval("data.%s_pass()" %(options.options["-p"])).replace("\t", "").split("\n")
	else:
		options.passwd = fread(options.options["-p"])


	options.report = options.run_options["--report"]
	options.verbose = options.run_options["--verbose"]
	if options.run_options["--proxy"]:
		options.proxy = fread("%s/liveproxy.txt" %(data.__path__[0])).split("\n")


if __name__ == "__main__":
	utils.die("Oops! Wrong place", "Find other place")
	