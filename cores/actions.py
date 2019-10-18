import random, sys
from utils import events


def list_choose_randomly(arg_list):
	"""
	Select element in list randomly
	:param arg_list: a list of values
	:return: Random element in arg_list
	"""
	return random.choice(arg_list)


def file_choose_randomly(file_location):
	"""
	Select a line in a file randomly
	:param file_location: string = file location
	:return: a line in the file
	"""
	return list_choose_randomly(file_read(file_location).split("\n"))


def to_list(username):
	"""
	Split input string by ':' value (use for username in options)
	:param username: string = option users give from keyboard
	:return: a list of username splitted by ':'
	"""
	return username.split(":")


def file_load(file_location):
	"""
	Try open a file and give user file object
	:param file_location: string = location of the file
	:return: file object = open(file)
	"""
	try:
		file_object = open(file_location, 'r')
		return file_object
	except Exception as error:
		events.error("%s" % (error))
		sys.exit(1)


def file_read(file_location):
	"""
	Try open file and read all data
	:param file_location: string = path to the file
	:return: string = text in the file
	"""
	try:
		file_object = open(file_location, 'r')
		return file_object.read()
	except Exception as error:
		events.error("%s" % (error))
		sys.exit(1)
	finally:
		try:
			file_object.close()
		except:
			pass


def file_write(file_location, data):
	"""
	Write text to file
	:param file_location: string = path to file
	:param data: string = text to write into file
	:return: None
	"""
	try:
		file_object = open(file_location, "w")
		file_object.write(data)
	except Exception as error:
		events.error("%s" % (error))
		sys.exit(1)
	finally:
		try:
			file_object.close()
		except:
			pass


def file_write_next(file_location, data):
	"""
	Write data to a file in next line
	:param file_location: string = file location
	:param data: string = text to write
	:return: True
	"""
	try:
		file_object = open(file_location, "a")
		file_object.write(data)
	except Exception as error:
		events.error("%s" % (error))
		sys.exit(1)
	finally:
		file_object.close()


def string_gen_randomly(len_min=2, len_max=5, select_type="char"):
	"""
	Generate a string randomly with random length
	:param len_min: int[default] = 2 Min value of int range to choose randomly for text len
	:param len_max: int[default] = 5 Max value of int range to choose randomly for text len
	:param select_type: string = [ "char" | "dig" ] choose charset type
	:return: random string
	refer: https://stackoverflow.com/a/2257449
	"""
	import string

	# Generate charset range from select_type
	if select_type == "char":
		charset = string.ascii_letters # string.letters in python 2. TODO fix here
	elif select_type == "dig":
		charset = string.digits

	# Generate length of string from len_min and len_max
	len_min, len_max = 0, random.randint(len_min, len_max)

	# return string value
	return ''.join(random.choice(charset) for _ in range(len_min, len_max))

def get_domain(url):
	return url.split("/")[2]
