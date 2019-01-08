<h1 align='center'>BruteforceHTTP</h1>
<p align='center'><i>An automated brute forcing tool</i></p>

## About this project
A HTTP brute force tool bases on Mechanize browser.

## Installation

Requirements

| name        |
|-------------|
| python2     |
| python2-pip |
| python-regex |

1.
```
sudo apt install python python-regex git
```

2.
```
git clone https://github.com/dmknght/BruteforceHTTP.git
```

## Options
```
Usage: main.py [options] <url>
```
Options:

 ```
 -u <word_list> : Add word list for username field
 -p <word_list> : Add word list for password field
 -U <username>: user1:user2:user3
 ```

## Usage

Use default userlist and passlit:
```
python main.py <Target URL>
```

Use default passlist for user `admin` (for multiple usernames, use `user1:user2:user3`):
```
python main.py -U admin <Target URL>
```

Use custom userlist and custom passlist:
```
python main.py -u <path to userlist> -p <path to passlist> <Target URL>
```


## How this tool work
This tool will detect form field automatically, collect information and submit data therefor it can handle csrf token.

* Update 1/1/2019: Auto choose HTTP Get authentication and HTTP POST form mode

Problems:
 - Detect form field error for some special cases. We will try to improve our function.
 - Wrong password matching: matching condition is not completed.

Further improvement (See TODO.md)

## DOES NOT work (by now)
- Javascript website (mechanize library problem)
- Login with captcha
(Please read WEBNOTE.md for test cases)

## Author
- [@Ic3W4ll](https://github.com/dmknght)
- [@ZeroX-DG](https://github.com/ZeroX-DG)

## Additional information
- This tool was created in Parrot Security OS 3.11, python 2.7.15rc1.
- Fully tested on Parrot Security OS 4.4 and Debian 10.
- Windows platform is unsupported

## Credit
Special thank to all authors of these projects:
- [Mechanize Project](https://github.com/python-mechanize/)
- [Fuzzdb-project: user-agent list](https://github.com/fuzzdb-project/fuzzdb/blob/master/discovery/UserAgent/UserAgentListCommon.txt)
- [routersploit project: print_table function](https://github.com/threat9/routersploit/blob/master/routersploit/core/exploit/printer.py)
- [Metasploit-framework project: Wordlists](https://github.com/rapid7/metasploit-framework/tree/master/data/wordlists)
