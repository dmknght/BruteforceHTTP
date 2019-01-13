import sys
from core.utils import print_table

def print_fast_help():
	print(
		'\nUsage: %s [<option> <value>] [mode] [--list <list_name>] <[URL] | [-l <url_list>]>\n' %(
		sys.argv[0])
	)
	print("An URL or URL list is required")

def print_help():

	#	Print project's help table
	print_fast_help()
	print("Options: ")
	title = ("Formats", "Examples")
	menu = [
		[
			"%-14s" %("-u <file_path>"),
			"-u /opt/wordlists/nmap.lst"
		],
		[
			"%-14s" %("-p <file_path>"),
			"-p /opt/wordlists/passwd.txt"
		],
		[
			"%-14s" %("-U <username>"),
			"-U admin | -U admin:user1"
		],
		[
			"%-14s" %("-t <threads>"),
			"-t 32"
		],
		[
			"%-14s" %("-T <timeout>"),
			"-t 25"
		],
		[
			"%-14s" %("-l <file_path>"),
			"-l url_list.txt"
		],
	]
	print_table(title, *menu)
	
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