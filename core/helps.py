import sys
from core.utils import print_table

def print_fast_help():
	print('\nUsage: %s [<option> <value>] [mode] [--list <list_name>] URL\n' %(
		sys.argv[0])
	)

def print_help():

	#	Print project's help table
	print_fast_help()
	print("Options: ")
	#title = ("Formats", "Default values", "Examples")
	title = ("Formats", "Examples")
	menu = [
		[
			"%-14s" %("-u <file_path>"),
			#"--list default",
			"-u /opt/wordlists/nmap.lst"
		],
		[
			"%-14s" %("-p <file_path>"),
			#"--list default",
			"-p /opt/wordlists/passwd.txt"
		],
		[
			"%-14s" %("-U <username>"),
			#"None",
			"-U admin | -U admin:user1"
		],
		[
			"%-14s" %("-t <threads>"),
			#"16 (threads)",
			"-t 32"
		],
	]
	print_table(title, *menu)
	
	# TODO: move sqli to extras mode, no reauth for sqli
	# print("\nAttack mode: Attack method")
	# title = ("Modes", "Descriptions")
	# menu = [
	# 	[
	# 		"%-14s" %("--brute [Default]"),
	# 		"Brute Force [HTTP GET / POST Form]"
	# 	],
	# 	# Remove, now automatic choose
	# 	# [
	# 	# 	"%-14s" %("--httpget"),
	# 	# 	"HTTP Basic Authentication attack"
	# 	# ],
	# 	[
	# 		"%-14s" %("--sqli [N/A]"),
	# 		"SQL Injection login bypass"
	# 	],
	# ]
	# print_table(title, *menu)

	print("\nRunning mode:")
	title = ("Modes", "Descriptions")
	menu = [
		[
			"%-14s" %("--proxy"),
			"Attack using proxies"
		],
		[
			"%-14s" %("--verbose"),
			"Display running information"
		],
	]
	print_table(title, *menu)
	
	print("\nExtra modes: Combines with attack mode")
	title = ("Modes", "Descriptions")
	menu = [
		[
			"%-14s" %("--reauth"),
			"Check credentials on social networks"
		],
		[
			"%-14s" %("--getproxy"),
			"Provide new proxy list"
		],
	]
	print_table(title, *menu)

	print("\nWordlists: Values will be replaced by [-U/-u/-p] options")
	title = ("List name", "Descriptions")
	menu = [
		[
			"%-14s" %("default"),
			"Top common users+passwords"
		],
		[
			"%-14s" %("router"),
			"Router wordlist"
		],
		[
			"%-14s" %("tomcat"),
			"Tomcat manager wordlist"
		],
		[
			"%-14s" %("cctv"),
			"CCTV wordlist"
		],
		[
			"%-14s" %("unix"),
			"Top Unix wordlist"
		],
		[
			"%-14s" %("http"),
			"Top HTTP wordlist"
		],
		[
			"%-14s" %("mirai"),
			"Mirai botnet wordlist"
		],
		[
			"%-14s" %("webshell"),
			"Webshell wordlist"
		],
	]
	print_table(title, *menu)
	print("")