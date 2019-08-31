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
		'bad': '\033[91m{}\033[00m'.format(mtext),
		'warn': '\033[93m{}\033[00m'.format(mtext),
		'good': '\033[92m{}\033[00m'.format(mtext),
		'norm': '\033[97m{}\033[00m'.format(mtext)
	}
	return (mtext[mtype])


def print_table(headers, *args, **kwargs):
	################################################
	#	print beautiful table in terminal style
	#	author @routersploit project
	#	ALL input data must be string
	################################################
	
	extra_fill = kwargs.get("extra_fill", 2)
	header_separator = kwargs.get("header_separator", "-")
	if not all(map(lambda x: len(x) == len(headers), args)):
		from utils import events
		events.error("Error headers", "PrintTable")
		return False
	
	def custom_len(x):
		try:
			return len(x)
		except TypeError:
			return 0
	
	##### CRAFTING HEADER ######
	fill = []
	
	# headers_line += label: Filling_header
	# headers_line = headers_line + "Lable 1 | Label 2"
	headers_line = '  |  '
	headers_separator_line = '  +'
	
	for idx, header in enumerate(headers):
		column = [custom_len(arg[idx]) for arg in args]
		column.append(len(header))
		current_line_fill = max(column) + extra_fill
		fill.append(current_line_fill)
		# label: Filling_header
		headers_line = "%s%s" % (
			"".join((headers_line, "{header:<{fill}}".format(header = header, fill = current_line_fill))),
			"|  "
		)
		
		headers_separator_line = "%s-%s" % (
			"-".join((
				headers_separator_line,
				'{:<{}}'.format(header_separator * current_line_fill, current_line_fill)
			)),
			"+"
		)
	
	# End of crafting header
	
	# Print header
	print("%s\n%s\n%s" % (headers_separator_line, headers_line, headers_separator_line))
	
	# Print contents
	for arg in args:
		content_line = '  |  '  # print first character before contents
		for idx, element in enumerate(arg):
			content_line = "%s%s" % (
				"".join((
					content_line,
					'{:{}}'.format(element, fill[idx])
				)),
				"|  "
			)
		print(content_line)
	
	# Print end line
	print(headers_separator_line)

