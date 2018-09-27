import sys, actions

# TODO write stderr and stdout instead of print

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
	sys.stdout.write("\033[F \033[K" * actions.size_o(mtext))

def printp(index, total, bar_size = 50):
	completed = (index * bar_size) / total
	prints("|%s%s| %s/%s"%(
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
	# TODO move print to std write
	# if mtype == 'bad':
	# 	sys.stderr.write("%s\n" %(craft_msg(mtext, mtype)))
	# else:
	# 	sys.stdout.write("%s\n" %(craft_msg(mtext, mtype)))

def craft_msg(mtext, mtype = 'warn'):
	# https://misc.flogisoft.com/bash/tip_colors_and_formatting
	####################################################
	#	create text message with color
	#	bad: red
	#	warn: yellow
	#	good: light green
	#	This functions is using for Linux terminal only
	####################################################

	mtext = {
		'bad':  '\033[91m{}\033[00m'.format(mtext),
		'warn': '\033[93m{}\033[00m'.format(mtext),
		'good': '\033[92m{}\033[00m'.format(mtext),
		'norm': '\033[97m{}\033[00m'.format(mtext)
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

	print('\nUsage: %s [<option> <value>] [mode] URL\n\nOptions:\n' %(sys.argv[0]))
	title = ("Format", "Example")
	menu = [
		[ "%-25s"%("-u <path_to_wordlist>"), "-u /usr/share/wordlists/nmap.lst"],
		[ "%-25s"%("-p <path_to_wordlist>"), "-p /usr/share/wordlists/fasttrack.txt"],
		[ "%-25s"%("-U <username>"), "-U admin | -U admin:user1:user2:user3"],
		[ "%-25s"%("-t <threads>"), "-t 32"],
		[ "%-25s"%("-k <false_key>"), "-k 'Invalid username'"]
	]
	print_table(title, *menu)
	
	print("\nModes:\n")
	title = ("Attack Modes", "Ony ONE attack mode can be used")
	menu = [
		[ "%-25s"%("--brute [Default]"), "Brute Forcing credentials"],
		[ "%-25s"%("--sqli [Not Available]"), "SQL Injection bypass"],
		[ "%-25s"%("--basic [Not Available]"), "HTTP Basic Authentication"],
	]
	print_table(title, *menu)

	print("")
	title = ("Running Modes", "")
	menu = [
		[ "%-25s"%("--proxy"), "Use Proxy each connection"],
		[ "%-25s"%("--verbose"), "Display more information"],
		[ "%-25s"%("--report"), "Write result report"],
	]
	print_table(title, *menu)
	print("")

def fixLen(text, lim):
	# https://stackoverflow.com/a/37422973
	ret, text = " %.*s" %(lim, text[:lim]), text[lim:]
	lim = 70
	
	while text:
		
		if len(text) < lim:
			ret += " |\n  | %s" %(text) + " " * (71 - len(text))
			break
		ret, text = ret + " |\n  |  %.*s" %(71, text[:lim]), text[lim:]

	return ret

def report_banner(url, mode, proxy, thread, creds, daytime, runtime):
	# if option != "--sqli" and "--single":
	def n_body(creds):
		ret = ""
		for match in creds:
			ret += "|  Username: %-60s |\n  |  Password: %-60s |" %(
				fixLen(match[0], 50), fixLen(match[1], 48)
			)
			ret += "\n  |%s|\n  " %("+" * 73)
		return ret
	
	def s_body(creds):
		ret = ""
		for match in creds:
			ret += "  |  Payload: %-50s |\n" %(
				fixLen(match, 50)
			)
		return ret
	
	header = """
	  =======================================================================
	/       Finish: %-58s\\
	|       Name: %-59s |
	|-------------------------------------------------------------------------|
	|       Attack mode: %-6s |   Using Proxy: %-6s |   Threads: %-4s     |
	|-------------------------------------------------------------------------|
	|  Target: %-62s |
	|  URL: %-65s |
	|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|
	""" %(
		"%s      %s" %(
			daytime.split("_")[1].replace(".", ":"),
			daytime.split("_")[0].replace(".", "/")
		),
		fixLen(daytime + ".txt", 58),
		mode.replace("--", ""),
		proxy,
		thread,
		fixLen(url.split("/")[2], 61),
		fixLen(url, 64),
	)
	
	footer = """\\  Runtime: %-62s/
	  =======================================================================
	  """ %(runtime)
	
	body = n_body(creds) if mode not in ["--sqli"] else s_body(creds)

	return header.replace("\t", "  ") + body + footer.replace("\t", "  ")

def start_banner(url, options, mode, r_options):
	usr = options["-U"] if options["-U"] else options["-u"]

	banner = """
	  =======================================================================
	/%-73s\\
	|-------------------------------------------------------------------------|
	|  Target: %-62s |
	|  URL: %-65s |
	|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|
	|  Userlist: %-60s |
	|  Passlist: %-60s |
	|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|
	|                                                                         |
	|       Attack mode: %-6s |   Using Proxy: %-6s |   Threads: %-4s     |
	|                                                                         |
	|-------------------------------------------------------------------------|
	|       False keyword: %-50s |
	|-------------------------------------------------------------------------|
	\\           Verbose: %-12s       |         Report: %-12s    /
	  =======================================================================
	""" %( " " * 25 + "HTTP LOGIN BRUTE FORCER",
		fixLen(url.split("/")[2], 61),
		fixLen(url, 64),
		fixLen(usr, 59),
		fixLen(options["-p"], 59),
		mode.replace("--", ""),
		r_options["--proxy"],
		options["-t"],
		fixLen(str(options["-k"]), 49),
		r_options["--verbose"],
		r_options["--report"],
	)
	
	return banner.replace("\t", "  ")
	
if __name__ == "__main__":
	die("Oops! Wrong place", "Find other place")