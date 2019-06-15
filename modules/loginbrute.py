from utils.utils import printf, die
from cores.actions import randomFromList
from cores.check import parseLoginForm, check_sqlerror
from libs.mbrowser import mBrowser as Browser

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
	# if options.engine == "mechanize":
	# 	from libs.mbrowser import mBrowser as Browser
	# 	proc = Browser(options.timeout) # TODO remove here
	# elif options.engine == "selenium":
	# 	from libs.sbrowser import sBrowser as Browser
	# 	proc = Browser() # TODO remove here
	# else:
	# 	pass # ERROR
	# #	Get login form field informations
	
	# frmLoginID, frmFields = loginInfo
	tryPassword, tryUsername = tryCred

	# proc = Browser(options.timeout) # TODO recovery here

	# BREAK if we had valid payload?
	# if options.options["-p"] == "sqli" and len(list(result.queue)) > 1:
	# 	return True
	
	for cred in list(result.queue):
		if tryUsername == cred[1]:
			return True
	
	try:
		proc = Browser()
		if options.proxy:
		# Set proxy connect
			proxyAddr = randomFromList(options.proxy)
			proc.setproxy(proxyAddr)
		proc.open_url(options.login_url)
		proc.get_opts(options) # TODO remove this fucntion in sbrowser and mbrowser
		_form = parseLoginForm(proc.forms())
		if not _form:
			if options.verbose:
				printf("[x] LoginBrute: No login form found. Possibly get blocked!")
			return False
		else:
			frmCtrl, frmFields = _form
			frmLoginID, btnSubmit = frmCtrl
		if options.verbose and loginInfo != _form:
			printf("[+] Warning: Form field has been changed!")	
		#	Select login form
		# page_title = proc.title()
		#	Send request
		
		#	Reload the browser. For javascript redirection and others...
		# proc.reload()
		#	If no login form -> maybe success. Check conditions
		proc.xsubmit(frmCtrl, frmFields, tryCred)
		if options.verbose:
			if options.proxy:
				printf("[+] {%s: %s; %s: %s} through %s" %(frmFields[1], tryUsername, frmFields[0], tryPassword, proxyAddr), 'norm')
			else:
				if len(frmFields) == 2:
					printf("[+] {%s: %s; %s: %s}" %(frmFields[1], tryUsername, frmFields[0], tryPassword), 'norm')
				else:
					printf("[+] {%s: %s}" %(frmFields[0], tryPassword), 'norm')

		if not parseLoginForm(proc.forms()):# != loginInfo:
			test_result = check_condition(options, proc, loginInfo)
			if test_result == 1:
				#printf("[*] Page title: ['%s']" %(proc.title()), "good")
				# "If we tried login form with username+password field"
				if tryUsername:
					printf("[*] %s [%s]" %([tryUsername, tryPassword], proc.get_title()), "good")
				# "Else If we tried login form with password field only"
				else:
					printf("[*] %s []" %([tryPassword], proc.get_title()), "good")
				result.put([options.url, tryUsername, tryPassword])
			elif test_result == 2 and options.verbose:
				printf("[+] SQL Injection vulnerable found")
				printf("   %s" %([tryUsername, tryPassword]), "norm")
			else:
				# Possibly Error. But sometime it is true
				if options.verbose:
					printf("[x] Get error page: %s" %([tryUsername, tryPassword]), "bad")
					printf("   [x] Page title: ['%s']" %(proc.get_title()), "bad")
		# "Login form is still there. Oops"
		else:
			# TODO test if web has similar text (static)
			if check_sqlerror(proc.get_resp()) and options.verbose:
				printf("[+] SQL Injection vulnerable found")
				printf("   %s" %([tryUsername, tryPassword]), "norm")
			if options.verbose:
				if options.proxy:
					printf("[-] Failed: %s through %s" %([tryUsername, tryPassword], proxyAddr), "bad")
				else:
					printf("[-] Failed: %s" %([tryUsername, tryPassword]), "bad")
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
