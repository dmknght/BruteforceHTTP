import sys, actions


def prints(mtext):
	#############################################
	#	print message and replace it after
	#	Use for status bar, brute forcing process
	#	https://stackoverflow.com/a/5291044
	#
	#	Update code by this (Works better)
	#	https://stackoverflow.com/a/41511658
	#############################################

	print(mtext)
	sys.stdout.write("\033[F \033[K" * actions.getObjectSize(mtext))

def printp(username, index, total, bar_size = 50):
	completed = (index * bar_size) / total
	prints("%s\n |%s%s| %s/%s"%(
		username,
		completed * '#',
		(bar_size - completed) * '-',
		index,
		total)
	)


def printf(mtext, mtype = 'warn'):
	############################################
	#	Print text w/ color
	#
	###########################################

	print(craft_msg(mtext, mtype))

def craft_msg(mtext, mtype = 'warn'):
	####################################################
	#	create text message with color
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
	
def die(msg, error):
	printf(msg, "bad")
	printf(error, "bad")
	sys.exit(1)

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