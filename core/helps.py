import sys
from core import utils

def print_fast_help():
	print('\nUsage: %s [<option> <value>] [mode] [--list <list_name>] URL\n' %(
		sys.argv[0])
	)

def print_help():

	#	Print project's help table
	print_fast_help()
	print("\nOptions:\n")
	title = ("Formats", "Default values", "Examples")
	menu = [
		[
			"%-23s" %("-u <path_to_wordlist>"),
			"default (list)",
			"-u /usr/share/wordlists/nmap.lst"
		],
		[
			"%-23s" %("-p <path_to_wordlist>"),
			"default (list)",
			"-p /usr/share/wordlists/fasttrack.txt"
		],
		[
			"%-23s" %("-U <username>"),
			"None",
			"-U admin | -U admin:user1"
		],
		[
			"%-23s" %("-t <threads>"),
			"16 (threads)",
			"-t 32"
		],
	]
	utils.print_table(title, *menu)
	
	print("\nModes: Only ONE attack mode can be used\n")
	title = ("Attack Modes", "Descriptions")
	menu = [
		[
			"%-23s" %("--brute [Default]"),
			"HTTP POST Form attack"
		],
		# Remove, now automatic choose
		# [
		# 	"%-23s" %("--httpget"),
		# 	"HTTP Basic Authentication attack"
		# ],
		[
			"%-23s" %("--sqli [Not Available]"),
			"SQL Injection login bypass attack"
		],
	]
	utils.print_table(title, *menu)

	print("")
	title = ("Running Modes", "Descriptions")
	menu = [
		[
			"%-23s" %("--proxy"),
			"Attack using proxies"
		],
		[
			"%-23s" %("--verbose"),
			"Display running information"
		],
	]
	utils.print_table(title, *menu)
	
	print("")
	title = ("Extra Modes", "Descriptions")
	menu = [
		[
			"%-23s" %("--reauth"),
			"Checks valid credentials on other social-networks"
		],
		[
			"%-23s" %("--getproxy"),
			"Get list of proxy, check connection though each address"
		],
	]
	utils.print_table(title, *menu)

	print("\nWordlists:\n")
	title = ("Values", "Informations")
	menu = [
		[
			"%-23s" %("default"),
			"Top usernames+passwords"
		],
		[
			"%-23s" %("router"),
			"Default router usernames+passwords"
		],
		[
			"%-23s" %("tomcat"),
			"Default tomcat usernames+passwords"
		],
		[
			"%-23s" %("cctv"),
			"Default cctv usernames+passwords"
		],
		[
			"%-23s" %("unix"),
			"Top unix usernames+passwords"
		],
		[
			"%-23s" %("http"),
			"Top http usernames+passwords"
		],
		[
			"%-23s" %("mirai"),
			"List usernames+passwords used by mirai botnet"
		],
		[
			"%-23s" %("webshell"),
			"Common webshell usernames+passwords"
		],
	]
	utils.print_table(title, *menu)
	print("")