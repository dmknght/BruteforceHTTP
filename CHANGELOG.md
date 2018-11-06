# 07/11/2018
* Print username, password in message now using list format so space characters won't be missed
* Remove -k option (key false)
* New way for detecting user's session

# 15/10/2018
* Added --reauth option: Check password for other social URLs
* Change --httpauth to --httpget

## 14/10/2018
* Upgrade print table function
* Fix bugs

## 09/10/2018
* Code improvment

## 03/10/2018
* Password form only brute

## 02/10/2018
* Bugs fixed and codes improved
* Added Basic HTTP Get Authentication

## 1.4
* Add new wordlists by default and using option
* Add getproxy option
* Threading now working properly
* Remove progress bar (Issue with threading)
* Add report option (And making report after finishing job)
* Add verbose option
* Bugs fixed and codes improvement

## 27/09/2018
* Add making report funcs
* Add wordlists as default

## 26/09/2018
* Mov httpbrute to plugins/loginbrute
* Testing: threads stop after valid password found

## 24/09/2018
* New threading logic. Fix threading problems.

## 1.3 test 4
* Modify many function names
* Rework options.py module
* Default lists now are modules instead of reading form files
* New tbrowser.py module for browsing
* Update help menu
* Userlist (`-U` option now use `:` and `,` to split names)

## 1.3 test 3
* Add change working directory (chdir) to project's root directory 
* Move some data to /data/
* Move module utils, actions to package core
* Create actions.startBrowser() instead of lines of code each function


## 1.3 test 2
* Add actions.die() -> print error message and exit(1)
* Add in-dev get proxy module


## 1.3 test 1
* Use readlines instead of itertools.islice (Testing)
* Module actions:
	* Rename functions
	* Add seek(0) to actions.getObjectSize() when read file object
	* Add read lines of string object
* Add set threads to options
* New progress bar, new progress bar function (utils.printp)

## 1.3 test 0
* Add multithreading
* Move parsing args to new module
* Rework httpbrute module (no OOP). Keep old version in old_httpbrute.py
* Use list of itertools.islice to read Password list

## 1.2g
* Remove encode UTF 8 in find form information (wrong detect in some cases)

## 1.2f
* Edit variable names
* Rework actions.subaction_countListSize
* Rework action.action_getUserAgent

## 1.2e
* Improve exception logic

## 1.2d
* Create new function for single authenticate task
* Edit code struct

## 1.2c
* print result now in finally block

## 1.2b
* actions.getFileData() now returning file object instead of list
* Passlist and userlist (if userlist is read from file) are file object now
	-> Reading huge file is no longer using huge memory
* Improve code logic. File objects will close automatically
* Sort default userlist
* Fix info banner detail

## 1.2
* Fixed Meta data login bug (show wrong password)
* Improve code logic

## 1.1
* Edit code struct, improve logic
## 1.0
* Create Project