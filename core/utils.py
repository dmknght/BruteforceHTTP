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

	#######
	#	Newer version:
	#	https://stackoverflow.com/a/3173338
	#######

	sys.stdout.write("\r%s\r" %(mtext)) # Print to screen
	sys.stdout.flush() # Flush code
	sys.stdout.write("\r%s\r" %(" " * len(mtext))) # Clean characters in line


# def printp(count, total, bar_size = 50):
# 	completed = (count * bar_size) / total
# 	prints("|%s%s| %s/%s"%(
# 		completed * '#',
# 		(bar_size - completed) * '-',
# 		count,
# 		total)
# 	)


def printf(mtext, mtype = 'warn'):
	############################################
	#	Print text w/ color
	#
	###########################################

	print(craft_msg(mtext, mtype))

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

	extra_fill = kwargs.get("extra_fill", 3)
	header_separator = kwargs.get("header_separator", "-")
	if not all(map(lambda x: len(x) == len(headers), args)):
		printf("[x] PrintTable: Error headers", 'bad')
		return None

	def custom_len(x):
		try:
			return len(x)
		except TypeError:
			return 0

	##### CRAFTING HEADER ######
	fill = []

	# headers_line += label: Filling_header
	# headers_line = headers_line + "Lable 1 | Label 2"
	headers_line = '  | '
	headers_separator_line = '  +'

	for idx, header in enumerate(headers):
		column = [custom_len(arg[idx]) for arg in args]
		column.append(len(header))
		current_line_fill = max(column) + extra_fill
		fill.append(current_line_fill)
		# label: Filling_header
		headers_line = "%s%s" %(
			"".join((headers_line, "{header:<{fill}}".format(header = header, fill = current_line_fill))),
			"| "
			)

		headers_separator_line = "%s%s" %(
			"-".join((
				headers_separator_line,
				'{:<{}}'.format(header_separator * current_line_fill, current_line_fill)
			)),
			"+"	
		)
		
	# End of crafting header

	# Print header
	print("%s\n%s\n%s" %(headers_separator_line, headers_line, headers_separator_line))

	# Print contents
	for arg in args:
		content_line = '  | ' # print first character before contents
		for idx, element in enumerate(arg):
			content_line = "%s%s" %(
				"".join((
					content_line,
					'{:{}}'.format(element, fill[idx])
				)),
				"| "	
			)
		print(content_line)
		
	# Print end line
	print(headers_separator_line)


def fixLen(text, lim):
	# https://stackoverflow.com/a/37422973
	ret, text = " %.*s" %(lim, text[:lim]), text[lim:]
	lim = 68 # MAX LIM FOR TERMINAL
	
	while text:
		
		if len(text) < lim:
			ret += " |\n  | %s" %(text) + " " * (lim + 1 - len(text))
			break
		ret, text = ret + " |\n  |  %.*s" %(71, text[:lim]), text[lim:]

	return ret

def report_banner(url, mode, proxy, thread, creds, daytime, runtime, regular):
	# if option != "--sqli" and "--single":
	def n_body(creds):
		ret = ""
		for match in creds:
			ret += "|  Username: %-58s |\n  |  Password: %-58s |" %(
				fixLen(match[0], 57), fixLen(match[1], 57)
			)
			ret += "\n  |%s|\n  " %("+" * 71)
		return ret
	
	def s_body(creds, mode):
		ret = ""
		name = "Payload" if mode == "--sqli" else "Password"
		for match in creds:
			payload = match[0] if match[0] else match[1]
			ret += "|  %-10s: %-56s |" %(
				name, 
				fixLen(payload, 48)
			)
			ret += "\n  |%s|\n  " %("+" * 71)
		return ret
	
	header = """
	  =====================================================================
	/       Finish: %-56s\\
	|       Name: %-57s |
	|-----------------------------------------------------------------------|
	|      Attack mode: %-6s |   Using Proxy: %-6s |   Threads: %-4s    |
	|-----------------------------------------------------------------------|
	|  Target: %-60s |
	|  URL: %-63s |
	|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|
	""" %(
		"%s      %s" %(
			daytime.split("_")[1].replace(".", ":"),
			daytime.split("_")[0].replace(".", "/")
		),
		fixLen(daytime + ".txt", 55),
		mode.replace("--", ""),
		proxy,
		thread,
		fixLen(url.split("/")[2], 59),
		fixLen(url, 62),
	)
	
	footer = """\\  Runtime: %-60s/
	  =====================================================================\n""" %(runtime)
	
	body = n_body(creds) if regular else s_body(creds, mode)

	return header.replace("\t", "  ") + body + footer.replace("\t", "  ")

def start_banner(url, options, mode, r_options):
	usr = options["-U"] if options["-U"] else options["-u"]

	banner = """
	  =====================================================================
	/%-71s\\
	|-----------------------------------------------------------------------|
	|  Target: %-60s |
	|  URL: %-63s |
	|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|
	|  Userlist: %-58s |
	|  Passlist: %-58s |
	|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|
	|                                                                       |
	|    Attack mode: %-8s   |  Using Proxy: %-6s |   Threads: %-4s   |
	|                                                                       |
	|-----------------------------------------------------------------------|
	\\           Verbose: %-11s       |         Report: %-11s    /
	  =====================================================================
	""" %( " " * 23 + "HTTP LOGIN BRUTE FORCER",
		fixLen(url.split("/")[2], 59),
		fixLen(url, 62),
		fixLen(usr, 57),
		fixLen(options["-p"], 57),
		mode.replace("--", ""),
		r_options["--proxy"],
		options["-t"],
		r_options["--verbose"],
		r_options["--report"],
	)
	
	return banner.replace("\t", "  ")
	
if __name__ == "__main__":
	die("Oops! Wrong place", "Find other place")