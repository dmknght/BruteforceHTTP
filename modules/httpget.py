from cores.browser import Browser
from utils import events
from cores.actions import list_choose_randomly


# https://stackoverflow.com/a/4089075

def submit(options, login_field, creds, result):
	password, username = creds
	
	if username in [x[1] for x in list(result.queue)]:
		return True
	
	try:
		proc = Browser()
		if options.proxy:
			proxyAddr = list_choose_randomly(options.proxy)
			proc.set_random_proxy(proxyAddr)
		else:
			proxyAddr = ""

		resp = proc.open_url(options.url, auth = (username, password))
		
		if resp.status_code == 401:
			if options.verbose:
				events.fail("['%s':%s'] <==> %s" % (username, password, proxyAddr), title = proc.get_title())
		elif resp.status_code > 400:
			events.error("[%s] ['%s': '%s']" % (proc.get_url(), username, password), "%s" % resp.status_code)
		else:
			events.found(username, password, proc.get_title())
			result.put([options.url, username, password])
	
	except Exception as error:
		events.error("%s" % (error), "BRUTE")
		return False
	
	finally:
		proc.close()