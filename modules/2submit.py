from utils import events
from cores.actions import list_choose_randomly
from cores.check import parseLoginForm


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
			return 1
		else:
			return 0
	else:
		return 1


def submit(options, loginInfo, tryCred, result):
	# frmLoginID, frmFields = loginInfo
	tryPassword, tryUsername = tryCred
	
	# proc = Browser(options.timeout) # TODO recovery here
	
	if tryUsername in [x[1] for x in list(result.queue)]:
		return True
	
	from cores.browser import Browser
	try:
		proc = Browser()
		if options.proxy:
			# Set proxy connect
			proxyAddr = list_choose_randomly(options.proxy)
			proc.set_random_proxy(proxyAddr)
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
		resp = proc.form_submit(frmCtrl, frmFields[1], tryUsername)
		if resp.status_code > 400:
			events.error("Error while sending %s" %(frmFields[1]), "BRUTE")
		
		resp = proc.form_submit(frmCtrl, frmFields[0], tryPassword)

		if options.verbose:
			events.warn("['%s']['%s'] <--> %s" % (tryUsername, tryPassword, proxyAddr), "TRY")
		
		if not parseLoginForm(proc.forms()):  # != loginInfo:
			test_result = check_condition(options, proc, loginInfo)
			if test_result == 1:
				if resp.status_code >= 400:
					events.error("['%s':'%s'] <--> %s" % (tryUsername, tryPassword, proxyAddr), "%s" % (resp.status_code))
				else:
					events.found(tryUsername, tryPassword, proc.get_title())
					# events.success("['%s':'%s'] [%s]" % (tryUsername, tryPassword, proc.get_title()), "FOUND")
					result.put([options.url, tryUsername, tryPassword])
			
			else:
				# Possibly Error. But sometime it is true
				if options.verbose:
					events.error("['%s': '%s'] [%s]" % (tryUsername, tryPassword, proc.get_title()), "BRUTE")
		# "Login form is still there. Oops"
		else:
			if options.verbose:
				events.fail("['%s':'%s'] <--> %s ==> %s" % (tryUsername, tryPassword, proxyAddr, proc.get_title()))
		
		return True
	
	except Exception as error:
		events.error("%s" % (error), "BRUTE")
	
	finally:
		proc.close()
