import sys


def prints(mtext):
	#############################################
	#	print message and replace it after
	#	Use for status bar, brute forcing process
	#############################################
	mtext = mtext.replace('\n', '')
	#	Remove \n in text.
	print(mtext)

	sys.stdout.write("\033[F")
	sys.stdout.write("\033[K")

def printf(mtext, mtype = 'warn'):
	print(craft_msg(mtext, mtype))

def craft_msg(mtext, mtype = 'warn'):
	####################################################
	#	print text with color
	#	bad: red
	#	warn: yellow
	#	good: light green
	#	This functions is using for Linux terminal only
	####################################################

	mtext = {
		'bad': '\033[91m{}\033[00m'.format(mtext),
		'warn': '\033[93m{}\033[00m'.format(mtext),
		'good': '\033[92m{}\033[00m'.format(mtext)
	}
	return (mtext[mtype])

def print_table(headers, *args, **kwargs):
	################################################
	#	print beautiful table in terminal style
	#	author @routersploit project
	#	ALL input data must be string
	################################################

	extra_fill = kwargs.get("extra_fill", 5)
	header_separator = kwargs.get("header_separator", "-")
	if not all(map(lambda x: len(x) == len(headers), args)):
		printf("Error headers", 'bad')
		return
	def custom_len(x):
		try:
			return len(x)
		except TypeError:
			return 0
	fill = []
	headers_line = '   '
	headers_separator_line = '   '

	for idx, header in enumerate(headers):
		column = [custom_len(arg[idx]) for arg in args]
		column.append(len(header))
		current_line_fill = max(column) + extra_fill
		fill.append(current_line_fill)
		headers_line = "".join((headers_line, "{header:<{fill}}".format(header = header, fill = current_line_fill)))
		headers_separator_line = "".join((
			headers_separator_line,
			'{:<{}}'.format(header_separator * len(header), current_line_fill)
		))
	print(headers_line)
	print(headers_separator_line)
	for arg in args:
		content_line = '   '
		for idx, element in enumerate(arg):
			content_line = "".join((
				content_line,
				'{:{}}'.format(element, fill[idx])
			))
		print(content_line)

def print_help():

	#	Print project's help table

	print('Usage: %s [options] url\n\nOptions:\n' %(sys.argv[0]))
	title = ("Format", "Example")
	menu_options = [
		["-u <path_to_wordlist>", "-u /usr/share/wordlists/nmap.lst"],
		["-p <path_to_wordlist>", "-p /usr/share/wordlists/fasttrack.txt"],
		["-U <username>", "-U user | -U user1:user2:user3"]
	]
	print_table(title, *menu_options)