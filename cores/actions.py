import random, sys, string
import utils


# def getRootDir(pathModuleLocation):
# 	##################################
# 	#	Get root folder of module file
# 	#	/foo/bar/module.py
# 	#	---> return "/foo/bar"
# 	#################################
# 
# 	pathModuleLocation = "/".join(pathModuleLocation.split("/")[:-1])
# 	return pathModuleLocation

def randomFromList(listData):
	return random.choice(listData)


def randomFromFile(pathFile):
	##########################################
	#	Return random User Agents from file
	#
	##########################################
	
	return randomFromList(fread(pathFile).split("\n"))


def lread(strUsername):
	#################################
	#	split input username to a list
	#	username -> [username]
	#	user1:user2 -> [user1, user2]
	#
	##################################
	
	return strUsername.split(":")


def fload(pathFile):
	###################################
	#	Read and return data file
	#	Return file object instead of list
	#
	###################################
	try:
		pFile = open(pathFile, 'r')
		return pFile
	except Exception as error:
		utils.die("[x] Error while loading file!", error)


def fread(pathFile):
	try:
		pFile = fload(pathFile)
		return pFile.read()
	except Exception as error:
		utils.die("[x] Error while reading data", error)
	finally:
		try:
			pFile.close()
		except:
			pass


def fwrite(pathFileLocation, writeData):
	try:
		objFileWrite = open(pathFileLocation, "w")
		objFileWrite.write(writeData)
	except Exception as error:
		utils.die("[x] Error while writing data", error)
	finally:
		try:
			objFileWrite.close()
		except:
			pass


def fwrite_c(pathFileLocation, writeData):
	try:
		fileWrite = open(pathFileLocation, "a")
		fileWrite.write(writeData)
	except Exception as error:
		utils.die("[x] Error while continuing write file", error)
	finally:
		fileWrite.close()


def srand(min = 2, max = 5, stype = "char"):
	# https://stackoverflow.com/a/2257449
	if stype == "char":
		charset = string.letters
	elif stype == "dig":
		charset = string.digits
	
	min, max = 0, random.randint(min, max)
	return ''.join(random.choice(charset) for _ in xrange(min, max))


if __name__ == "__main__":
	utils.die("Oops! Wrong place", "Find other place")
