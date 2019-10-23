<h1 align='center'>BruteforceHTTP</h1>
<p align='center'><i>An automated brute forcing tool</i></p>

## About this project
A HTTP brute force tool bases on Mechanize browser.

## Installation

Requirements

| name        |
|-------------|
| python / python3 / pypy |
| bs4 [beautifulsoup] |
| python-regex (optional) |
| python-lxml (optional) |
| html2text |
| python-uritools (optional) |
| mechanicalsoup |


1. On Debian distros:
This project should work on both python2, python3 and pypy. But, unfortunately Debian and pip has mechanicalsoup for python3 only.
 - Install for python3:
```
sudo apt install python3 python3-regex git python3-uritools python3-bs4 python3-mechanicalsoup
sudo pip3 install html2text
```
 - Install for pypy:
```
sudo apt install pypy python-uritools python-bs4 python-regex git
sudo pip2 install html2text mechanicalsoup
```

Python2 could have error `ImportError: No module named mechanicalsoup.stateful_browser`

2. Clone the project:
```
git clone https://github.com/dmknght/BruteforceHTTP.git
```

3. Run project
- Pypy:
`pypy main.py`
- Python3:
`python3 main.py`

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
python main.py <TARGET URL>
```

Use default passlist for user `admin` (for multiple usernames, use `user1:user2:user3`):
```
python main.py -U admin <TARGET URL>
```

Use custom userlist and custom passlist:
```
python main.py -u <path to userlist> -p <path to passlist> <TARGET URL>
```

Brute force with random proxy address:
```
python main.py <TARGET URL> --getproxy --proxy
```

## How this tool work
This tool will detect form field automatically, collect information and submit data therefor it can handle csrf token.

* Update 1/1/2019: Auto choose HTTP Get authentication and HTTP POST form mode
* Update 7/7/2019: Work with both python 2 and 3

Problems:
 - Detect form field error for some special cases. We will try to improve our function.
 - Wrong password matching: matching condition is not completed.

Further improvement (See TODO.md)

## Limitation
- Javascript website (mechanize library problem)
- Login with captcha
- There is a bug makes project can't detect login form (bs4 parse problem)
(Please read WEBNOTE.md for test cases)

## Why this / that (FAQ)
- Q: What is this tool?
- A: This tool is a brute-force attack tool, based on mechanize browser project. It means this tool can submit login request simulately.
- Q: What can it do?
- A: This tool is aimed to perform a brute-force attack automatically to all website with easy options.
- Q: Why not other tools?
- A: There are other tools can do brute force http. But...
	+ Almost scripts are static. They can attack 1 or few website only (based on form name)
	+ Hydra can do http login. But it has complex options, can't do login with CSRF token (and you have to give name of submit fields manually)
	+ Burp suite: can't do CSRF form by default, doesn't show you the readable report, complex steps and free version is not very fast.
- Q: This tool is aimed to brute-force all website, why it can't do this site:
- A: There are known issues:
	+ Javascript websites: mechanize can't do anything with javascript. Execute javascript brings security problems to client-side as well so, ... it is impossible right now.
	+ Gmail, Yahoo: this 2 sites use 2 submit times. I am trying to combine this case to project
	+ There are some login pages has wrong html syntax. I am working with mechanize to fix it
	+ Captcha: This is not easy one. But I am trying my best.
- Q: How about bypassing techniques?
- A: I am trying to combine SQL injection login bypass as well. Be patient!
- Q: Why does this tool show wrong result (multiple passwords for 1 username)
- A: There are 2 known cases:
	+ Web server shows block message with 200 HTTP Response (or error message in some cases). I am unable to analysis it exactly by now.
	+ I've found "Bypass authentication" issue in some CCTV. I think it is a "race condition" vulnerability.
- Q: You mentioned CCTV. So can this tool attack HTTP GET Authentication?
- A: Yes it can. It will choose HTTP GET / HTTP POST FORM attack automatically
- Q: How about wordlist? Secure password?
- A: This tool brings some default wordlists. You can use your custom wordlist as well. But becareful with huge file, there is a memory management issue that i can't fix it right now. I am trying with generating password from keywords as well. 
- Q: Sounds like this tool is trash
- A: Not really. I did some succesful real-world attacks with this tool and I can say it deserve to try. Ofcourse you can do it with other tools, or your own script. But as I said, my tool is easy to use and it will save your time.
- Q: Why do you do this so slow?
- A: I have to do almost everything: test, debug, analysis, research, ... @ZeroX-DG is doing his project, so I have to do it myself. I am not a good developer is an other reason. Actually I am not even a developer.
- Q: Can I customize your tool?
- A: Yes, you are welcome. But if you find something good, please hep me by make a pull request. It will help me (and others ;) ) so much.

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
- [MechanicalSoup Project](https://github.com/MechanicalSoup/MechanicalSoup)
- [BeautifulSoup Project](https://github.com/waylan/beautifulsoup)
