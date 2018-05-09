This project is focusing on Brute Forcing HTTP protocol AUTOMATICALLY.
Does not like hydra, which requires you to fill tons of options,

This tool needs as less option as it can:

Installing:
sudo apt install python2 python2-pip git
sudo pip install re mechanize
git clone <url>


Using
Usage: main.py [options] url

Options:

   Format                    Example                                   
   ------                    -------                                   
   -u <path_to_wordlist>     -u /usr/share/wordlists/nmap.lst          
   -p <path_to_wordlist>     -p /usr/share/wordlists/fasttrack.txt     
   -U <username>             -U user | -U user1:user2:user3  

This tool will detect form field, collect information and submit data.
We will improve this function and make it more smart and powerful.

Problems:
 *) Detect form field error for some special cases. We need to improve our function
 *) Wrong password matching: matching condition is not completed
 *) Reading huge file "eats" memory.

We will not stop there, here is our TODO list, to make our script more powerful:

##################################################################
#
#	TODO:
#		+) Reading huge file
#		+) Multi threading
#		+) Better form detecting and parsing
#		+) Better automatic login condition - gmail, etc..
#
#	TODO FURTHER
#		+) Proxy support
#		+) auto parse proxy list, brute forcing multi Proxy
#		+) sock 5, tor support
#
##################################################################

This tool was created in Parrot Security OS 3.11, python 2.7.15rc1

Credit:
	Author @Ic3W4ll
	Special thank for Mechanize project authors.
	Special thank for @ZeroX and others who help me for completing this project

	Mechanize Project
		http://wwwsearch.sourceforge.net/mechanize/
	Fuzzdb-project: user-agent list
		https://github.com/fuzzdb-project/fuzzdb/blob/master/discovery/UserAgent/UserAgentListCommon.txt
	routersploit project: print_table function
		https://github.com/threat9/routersploit/blob/master/routersploit/core/exploit/printer.py