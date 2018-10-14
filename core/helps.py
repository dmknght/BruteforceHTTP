import sys
from core import utils

def print_fast_help():
	print('\nUsage: %s [<option> <value>] [mode] [--list <value>] URL\n' %(sys.argv[0]))

def print_help():

	#	Print project's help table
	print_fast_help()
	print("\nOptions:\n")
	title = ("Formats", "Examples")
	menu = [
		[ "%-25s" %("-u <path_to_wordlist>"), "-u /usr/share/wordlists/nmap.lst"],
		[ "%-25s" %("-p <path_to_wordlist>"), "-p /usr/share/wordlists/fasttrack.txt"],
		[ "%-25s" %("-U <username>"), "-U admin | -U admin:user1 | -U admin,root,user"],
		[ "%-25s" %("-t <threads>"), "-t 32"],
		[ "%-25s" %("-k <false_key>"), "-k 'Invalid username'"]
	]
	utils.print_table(title, *menu)
	
	print("\nModes:\n")
	title = ("Attack Modes", "Ony ONE attack mode can be used")
	menu = [
		[ "%-25s" %("--brute [Default]"), "Brute Forcing credentials"],
		[ "%-25s" %("--httpauth"), "HTTP Basic Authentication"],
		[ "%-25s" %("--reauth"), "Checks valid credentials on other social-networks"],
		[ "%-25s" %("--sqli [Not Available]"), "SQL Injection bypassing"],
	]
	utils.print_table(title, *menu)

	print("")
	title = ("Running Modes", "Descriptions")
	menu = [
		[ "%-25s" %("--proxy"), "Use Proxy each connection"],
		[ "%-25s" %("--verbose"), "Display more information"],
		[ "%-25s" %("--getproxy"), "Get proxy list [Auto check connect to target]"],
	]
	utils.print_table(title, *menu)

	print("\nWordlists:\n")
	title = ("Values", "Informations")
	menu = [
		["%-25s" %("default"), "Top usernames+passwords"],
		["%-25s" %("router"), "Default router usernames+passwords"],
		["%-25s" %("tomcat"), "Default tomcat usernames+passwords"],
		["%-25s" %("cctv"), "Default cctv usernames+passwords"],
		["%-25s" %("unix"), "Top unix usernames+passwords"],
		["%-25s" %("http"), "Top http usernames+passwords"],
		["%-25s" %("mirai"), "List usernames+passwords used by mirai botnet"],
		["%-25s" %("webshell"), "Common webshell usernames+passwords"],
	]
	utils.print_table(title, *menu)
	print("")