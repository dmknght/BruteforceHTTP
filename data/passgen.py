import string


def maskgen(min_length = 1, max_length = 4, charset = None):
	"""
	Generate password using maskgen algth
	:param min_length: int = min length of text to generate
	:param max_length: int = max length of text to generate
	:param charset: text = all characters to generate
	:return: yield text
	"""
	charset = string.letters if not charset else charset
	from itertools import product
	for i in range(min_length, max_length):
		for password in product(charset, repeat = i):
			yield "".join(password)


def maskprocessor(text):
	"""
		passw?drd -> passw0rd, passw1rd, ..
	"""
	pass  # TODO create mask processor


def toggle_case(text):
	# https://stackoverflow.com/a/29184387
	# Generate dict; keys = lower characters and values = upper characters
	text, SUBSTITUTIONS = text.lower(), dict(zip(string.lowercase, string.uppercase))
	
	from itertools import product
	possibilities = [c + SUBSTITUTIONS.get(c, "") for c in text]
	for subbed in product(*possibilities):
		yield "".join(subbed)


def replacement(text):
	# TODO call this heavy replacement, light replacement will replace text with number and spec chars only
	# https://stackoverflow.com/a/29184387
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
		"z": "Z",
		" ": "_+-",
	}
	
	from itertools import product
	
	possibilities = [c + SUBSTITUTIONS.get(c, "") for c in text]
	for subbed in product(*possibilities):
		yield "".join(subbed)
