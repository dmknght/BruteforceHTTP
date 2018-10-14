import requests
from requests.auth import HTTPBasicAuth
from core import utils

# http://docs.python-requests.org/en/master/user/authentication/
# USING PROXY WITH REQUESTS https://stackoverflow.com/a/13395324
# TODO Using proxy

def submit(URL, tryUsername, tryPassword, proxy, verbose, result):

	for cred in list(result.queue):
		if tryUsername == cred[0]:
			return 0 # don't run if find password of username
			
	if verbose:
		utils.printf("Trying: %s:%s" %(tryUsername, tryPassword), 'norm')
	
	try:

		resp = requests.get(URL, auth = HTTPBasicAuth(tryUsername, tryPassword))
		
		if resp.status_code == 200:
			result.put([tryUsername, tryPassword])
			utils.printf("[*] Match found: %s:%s" %(tryUsername, tryPassword), "good") 
			# pass
		elif resp.status_code == 401:
			if verbose:
				utils.printf("[-] Failed: %s:%s" %(tryUsername, tryPassword), "bad")
		else:
			# unknown
			pass
	except Exception as err:
		utils.printf("[x] Error: %s:%s\n%s at %s" %(tryUsername, tryPassword, error, URL), "bad")