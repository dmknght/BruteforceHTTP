def fixLen(inpText, lim):
	# https://stackoverflow.com/a/37422973
	finalText, inpText = " %.*s" % (lim, inpText[:lim]), inpText[lim:]
	lim = 68  # MAX LIM FOR TERMINAL
	
	while inpText:
		
		if len(inpText) < lim:
			finalText += " |\n  | %s" % (inpText) + " " * (lim + 1 - len(inpText))
			break
		finalText, inpText = finalText + " |\n  |  %.*s" % (71, inpText[:lim]), inpText[lim:]
	
	return finalText


# def report_banner(url, mode, proxy, thread, creds, daytime, runtime, regular):
# 	# if option != "--sqli" and "--single":
# 	def n_body(creds):
# 		ret = ""
# 		for match in creds:
# 			ret += "|  Username: %-58s |\n  |  Password: %-58s |" %(
# 				fixLen(match[0], 57), fixLen(match[1], 57)
# 			)
# 			ret += "\n  |%s|\n  " %("+" * 71)
# 		return ret

# 	def s_body(creds, mode):
# 		ret = ""
# 		name = "Payload" if mode == "--sqli" else "Password"
# 		for match in creds:
# 			payload = match[0] if match[0] else match[1]
# 			ret += "|  %-10s: %-56s |" %(
# 				name, 
# 				fixLen(payload, 48)
# 			)
# 			ret += "\n  |%s|\n  " %("+" * 71)
# 		return ret

# 	header = """
# 	  =====================================================================
# 	/       Finish: %-56s\\
# 	|       Name: %-57s |
# 	|-----------------------------------------------------------------------|
# 	|      Attack mode: %-6s |   Using Proxy: %-6s |   Threads: %-4s    |
# 	|-----------------------------------------------------------------------|
# 	|  Target: %-60s |
# 	|  URL: %-63s |
# 	|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|
# 	""" %(
# 		"%s      %s" %(
# 			daytime.split("_")[1].replace(".", ":"),
# 			daytime.split("_")[0].replace(".", "/")
# 		),
# 		fixLen(daytime + ".txt", 55),
# 		mode.replace("--", ""),
# 		proxy,
# 		thread,
# 		fixLen(url.split("/")[2], 59),
# 		fixLen(url, 62),
# 	)

# 	footer = """\\  Runtime: %-60s/
# 	  =====================================================================\n""" %(runtime)

# 	body = n_body(creds) if regular else s_body(creds, mode)

# 	return header.replace("\t", "  ") + body + footer.replace("\t", "  ")

def start_banner(options):
	usr = options.options["-U"] if options.options["-U"] else options.options["-u"]
	
	banner = """
	  =====================================================================
	/%-71s\\
	|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|
	|  Userlist: %-58s |
	|  Passlist: %-58s |
	|+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++|
	|                                                                       |
	| %s |
	|                                                                       |
	|-----------------------------------------------------------------------|
	|    Extra mode: %-52s   |
	|-----------------------------------------------------------------------|
	|           Verbose: %-11s       |         Report: %-11s    |
	|***********************************************************************|
	|  %68s |
	+-----------------------------------------------------------------------+
	\\ %-69s /
	  =====================================================================
	""" % (
		" " * 23 + "HTTP LOGIN BRUTE FORCER",
		fixLen(usr, 57),
		fixLen(options.options["-p"], 57),
		# fixLen( "Attack mode: %-6s |  Proxy: %-5s  |  Threads: %-3s |  Timeout: %-3s" %(
		# 		options.attack_mode.replace("--", ""),
		# 		options.run_options["--proxy"],
		# 		options.threads,
		# 		options.timeout,
		# 	),
		# 	68
		fixLen("   Attack mode: %-8s |   Proxy: %-8s  |   Threads: %-8s " % (
			options.attack_mode.replace("--", ""),
			options.run_options["--proxy"],
			options.threads,
		),
		       68
		       ),
		"None" if len(options.extras) == 0 else fixLen(str(options.extras), 51),
		options.verbose,
		options.report,
		fixLen("%s target[s]: %-53s" % (
			len(options.target),
			options.options["-l"] if options.options["-l"] else (
				options.url.split("/")[2] if options.url.startswith(("http://", "https://")) else options.url.split("/")[0]
			)
		),
		       67
		       ),
		" " * 11 + "Github: https://github.com/dmknght/BruteforceHTTP"
	)
	
	return banner.replace("\t", "  ")
