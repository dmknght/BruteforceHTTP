def maskgen(min = 1, max = 4, charset = None):
	import string
	charset = string.letters if not charset else charset
	from itertools import product
	for i in xrange(min, max):
		for passwd in product(charset, repeat = i):
			yield "".join(passwd)