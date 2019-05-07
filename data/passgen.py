import string

def maskgen(min = 1, max = 4, charset = None):
	charset = string.letters if not charset else charset
	from itertools import product
	for i in xrange(min, max):
		for passwd in product(charset, repeat = i):
			yield "".join(passwd)

def maskprocessor(text):
	"""
		passw?drd -> passw0rd, passw1rd, ..
	"""
	pass # TODO create mask processor

def toggle_case(text):
	# https://stackoverflow.com/a/29184387
	# Generate dict; keys = lower characters and values = upper characters
	text, SUBSTITUTIONS = text.lower(), dict(zip(string.lowercase, string.uppercase))
	
	from itertools import product
	possibilities = [c + SUBSTITUTIONS.get(c, "") for c in text]
	for subbed in product(*possibilities):
		yield "".join(subbed)

def test_toggle_case(text):
	# https://stackoverflow.com/a/29184387
	# TODO create replacement table
	text = text.lower()
	SUBSTITUTIONS = {
		"a": "A4@",
		"b": "B",
		"c": "C",
		"d": "D",
		"e": "e3E",
		"f": "F",
		"g": "G",
		"h": "H",
		"i": "!1|I",
		"j": "J",
		"k": "K",
		"l": "L",
		"m": "M",
		"n": "N",
		"o": "0O",
		"p": "P",
		"q": "Q",
		"r": "R",
		"s": "$5S",
		"t": "T",
		"u": "U",
		"v": "V",
		"w": "W",
		"x": "X",
		"y": "Y",
		"z": "Z"
	}

	from itertools import product

	possibilities = [c + SUBSTITUTIONS.get(c, "") for c in text]
	for subbed in product(*possibilities):
		yield "".join(subbed)