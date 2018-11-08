import sys
from core import utils

def print_fast_help():
	print('\nUsage: %s [<option> <value>] [mode] [--list <values>] URL\n' %(sys.argv[0]))

def print_help():

	#	Print project's help table
	print_fast_help()
	print("\nOptions:\n")
	title = ("Formats", "Default values", "Examples")
	menu = [
		[ "%-25s" %("-u <path_to_wordlist>"), "default (list)", "-u /usr/share/wordlists/nmap.lst"],
		[ "%-25s" %("-p <path_to_wordlist>"), "default (list)", "-p /usr/share/wordlists/fasttrack.txt"],
		[ "%-25s" %("-U <username>"), "None", "-U admin | -U admin:user1"],
		[ "%-25s" %("-t <threads>"), "16 (threads)", "-t 32"],
	]
	utils.print_table(title, *menu)
	
	print("\nModes: Only ONE attack mode can be used\n")
	title = ("Attack Modes", "Descriptions")
	menu = [
		[ "%-25s" %("--brute [Default]"), "HTTP POST Form attack"],
		[ "%-25s" %("--httpget"), "HTTP Basic Authentication attack"],
		[ "%-25s" %("--sqli [Not Available]"), "SQL Injection login bypass attack"],
	]
	utils.print_table(title, *menu)

	print("")
	title = ("Running Modes", "Descriptions")
	menu = [
		[ "%-25s" %("--proxy"), "Attack using proxies"],
		[ "%-25s" %("--verbose"), "Display running information"],
	]
	utils.print_table(title, *menu)
	
	print("")
	title = ("Extra Modes", "Descriptions")
	menu = [
		[ "%-25s" %("--reauth"), "Checks valid credentials on other social-networks"],
		[ "%-25s" %("--getproxy"), "Get list of proxy, check connection though each address"],
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