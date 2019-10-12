from utils import events
from cores.actions import list_choose_randomly
from cores.check import find_login_form
from cores.analysis import check_login, check_sqlerror, get_redirection


def submit(options, login_field, tryCred, result):
	password, username = tryCred
	
	if username in [x[1] for x in list(result.queue)]:
		return True
	
	from cores.browser import Browser
	try:
		proc = Browser()
		if options.proxy:
			# Set proxy connect
			proxy_address = list_choose_randomly(options.proxy)
			proc.set_random_proxy(proxy_address)
		else:
			proxy_address = ""
		
		proc.open_url(options.login_url)
		_form = find_login_form(proc.forms())
		
		if not _form:
			if options.verbose:
				events.error("Get blocked", "BRUTE")
			return False
		else:
			form_control, form_fields = _form

		if options.verbose and login_field != _form:
			events.info("Login form has been changed", "BRUTE")

		resp = proc.form_submit(form_control, form_fields, tryCred)
		
		from cores.analysis import get_response_diff
		text_changed, source_changed = get_response_diff(options.txt.decode('utf-8'), resp.content.decode('utf-8'))
		
		"""
			If there is no other login form, check all changes in response
			If there is no login request from all new urls -> successfully
			== > Behavior: Login fail, click here or windows.location = login_page
		"""
		isLoginForm = False
		
		if not find_login_form(proc.forms()):
			for new_urls in get_redirection(source_changed):
				if not new_urls.startswith("http") and not new_urls.endswith(options.exceptions()):
					try:
						from urllib.parse import urljoin
					except ImportError:
						from urlparse import urljoin
					new_urls = urljoin(options.login_url, new_urls)
					proc.open_url(new_urls)
					if find_login_form(proc.forms()):
						isLoginForm = True
					break

			if not isLoginForm:
				"""
					Check SQL Injection
					1. SQL Injection
					2. Login successfully: No SQLi + No Login form
				"""
				
				if check_sqlerror(proc.get_response()):
					events.success("SQL Injection bypass", "BRUTE")
					events.info("['%s': '%s']" % (username, password))
				else:
					# "If we tried login form with username+password field"
					if username:
						if resp.status_code >= 400:
							events.error("['%s':'%s'] <--> %s" % (username, password, proxy_address), "%s" % (resp.status_code))
						else:
							events.found(username, password, proc.get_title())
							result.put([options.url, username, password])
					# "Else If we tried login form with password field only"
					else:
						if resp.status_code >= 400:
							events.error("[%s] <--> %s" % (password, proxy_address), "%s" % (resp.status_code))
						else:
							events.found('', password, proc.get_title())
							result.put([options.url, username, password])
			else:
				if username:
					events.fail("['%s':'%s'] <==> %s" % (username, password, proxy_address), text_changed.encode('utf-8'), proc.get_title())
				else:
					events.fail("['%s'] <==> %s" % (password, proxy_address), text_changed.encode('utf-8'), proc.get_title())

		# "Login form is still there. Oops"
		else:
			"""
				Possibly SQL injection or fail
			"""
			if options.verbose:
				if check_sqlerror(proc.get_response()):
					events.success("Possibly SQL Injection", "BRUTE")
					events.info("['%s': '%s']" % (username, password))
				else:
					if username:
						events.fail("['%s':'%s'] <==> %s" % (username, password, proxy_address), text_changed.encode('utf-8'), proc.get_title())
					else:
						events.fail("['%s'] <==> %s" % (password, proxy_address), text_changed.encode('utf-8'), proc.get_title())
		
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