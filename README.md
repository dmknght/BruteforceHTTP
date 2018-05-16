<h1 align='center'>BruteforceHTTP</h1>
<p align='center'><i>An automated brute forcing tool</i></p>

## About this project
This project focusing on Brute Forcing HTTP protocol AUTOMATICALLY with minimal options. Unlike hydra, which requires you to fill tons of options, this tool needs as less option as it can.

## Installation

Requirements

| name        |
|-------------|
| python2     |
| python2-pip |
| re         |
| python-mechanize   |

1.
```
sudo apt install python python-mechanize python-regex git
```

2.
```
git clone https://github.com/dmknght/BruteforceHTTP.git
```

## Usage
```
Usage: main.py [options] <url>
```
Options:

 ```
 -u <word_list> : Add word list for username field
 -p <word_list> : Add word list for password field
 -U <username>: user1:user2:user3
 ```

## How this tool work
This tool will detect form field automatically, collect information and submit data therefor it can handle csrf token.

Problems:
 - Detect form field error for some special cases. We will try to improve our function.
 - Wrong password matching: matching condition is not completed.

## Todo list:

- [ ] Multi threading
- [ ] Better form detecting and parsing
- [ ] Better password matching condition

Further improvement:
- [ ] Proxy support, brute forcing with multi proxies
- [ ] Generating password
- [ ] sock 5, tor support

## Author
- [@Ic3W4ll](https://github.com/dmknght)

## Maintainers
- [@Ic3W4ll](https://github.com/dmknght)
- [@ZeroX-DG](https://github.com/ZeroX-DG)

## Additional information
This tool was created in Parrot Security OS 3.11, python 2.7.15rc1.
Windows platform is unsupported

## Credit
Special thank to all authors of these projects:
- [Mechanize Project](http://wwwsearch.sourceforge.net/mechanize/)
- [Fuzzdb-project: user-agent list](https://github.com/fuzzdb-project/fuzzdb/blob/master/discovery/UserAgent/UserAgentListCommon.txt)
- [routersploit project: print_table function](https://github.com/threat9/routersploit/blob/master/routersploit/core/exploit/printer.py)
