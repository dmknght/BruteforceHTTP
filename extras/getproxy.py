import re, threading, sys
from libs import mbrowser
import utils
from cores import actions
from utils import progressbar
import data

if sys.version_info[0] == 2:
	import Queue
	result = Queue.Queue()
else:
	import queue
	result = queue.Queue()
"""
support url:
https://free-proxy-list.net/
"""

ROOT_FOLDER = data.__path__[0]
PROXY_PATH = "%s%s" %(ROOT_FOLDER, "/listproxy.txt")
LIVE_PATH = "%s%s" %(ROOT_FOLDER, "/liveproxy.txt")

def livelist():
	return actions.fread(LIVE_PATH).split("\n")

def getlist():
	return actions.fread(PROXY_PATH).split("\n")

def getnew(options):
	def parse_proxy(response):
		try:
			re_ip = r"\b(?:\d{1,3}\.){3}\d{1,3}\b<\/td><td>\d{1,5}"
			result = re.findall(re_ip, response.decode('utf-8'), re.UNICODE) # FIX PYTHON3 string pattern on a bytes-like object
			result = [element.replace("</td><td>", ":") for element in result]
			return result
		except Exception as error:
			utils.die("[x] GetProxy: Error while parsing proxies.", error)
			
	def checkProxyConnProvider(url = "https://free-proxy-list.net/"):
		try:
			utils.printf("[+] Getting proxy list from %s" %(url))

			getproxy = mbrowser.Browser()

			getproxy.open_url(url)
			utils.printf("[*] Gathering proxies completed.", "good")
			return getproxy.get_resp()

		except Exception as error:
			utils.die("[x] GetProxy: Error while connecting to proxy server!", error)
		finally:
			getproxy.close()
			

	try:
		listproxy = parse_proxy(checkProxyConnProvider())
	except Exception as error:
		utils.printf("[x] Getproxy.getnew: %s" %(error))
		listproxy = ""
	finally:
		try:
			listproxy = "\n".join(listproxy)
			utils.printf("[*] Get %s proxies." %(len(listproxy)), "good")
			utils.printf("[+] Saving to %s" %(PROXY_PATH))
			actions.fwrite(PROXY_PATH, listproxy)
			utils.printf("[*] Data saved!", "good")

		except Exception as error:
			utils.die("[x] GetProxy: Error while writting data", error)


def check(options):
	
	def run_threads(threads, sending, completed, total):
		# Run threads
		for thread in threads:
			sending += 1 # Sending
			progressbar.progress_bar(sending, completed, total)
			thread.start()

		# Wait for threads completed
		for thread in threads:
			completed += 1
			progressbar.progress_bar(sending, completed, total)
			thread.join()
		
		return sending, completed

	def checProxyConn(proxyAddr, target, result, verbose):
		try:
			proxyTest = mbrowser.Browser()
			proxyTest.setproxy(proxyAddr)

			if verbose:
				utils.printf("[+] Trying: %s" %(proxyAddr))

			proxyTest.open_url(options.url)

			if verbose:
				utils.printf("[*] Success: %s" %(proxyAddr), "good")
			result.put(proxyAddr)

		except Exception as error:
			if verbose:
				utils.printf("[x] %s %s" %(proxyAddr, error), "bad")
		finally:
			try:
				proxyTest.close()
			except:
				pass
	try:
		proxylist = actions.fread(PROXY_PATH).split("\n")
				
		workers= []
		trying, completed, total = 0, 0, len(proxylist)

		for tryProxy in proxylist:
			if len(workers) == options.threads:
				trying, completed = run_threads(workers, trying, completed, total)
				del workers[:]
			
			worker = threading.Thread(
				target = checProxyConn,
				args = (tryProxy, options.url, result, options.verbose)
			)

			worker.daemon = True
			workers.append(worker)
			
		trying, completed = run_threads(workers, trying, completed, total)
		del workers[:]

	except KeyboardInterrupt as error:
		utils.printf("[x] Terminated by user!", "bad")
		import os
		os._exit(0)
	
	except Exception as error:
		utils.die("[x] GetProxy: Error while checking proxy connection to target", error)

	finally:
		try:
			_data = "\n".join(list(result.queue))
			utils.printf("[*] %s proxies worked." %(len(_data)), "good")
			utils.printf("[+] Write working proxies")
			actions.fwrite(LIVE_PATH, _data)
			utils.printf("[*] Write working proxies completed", "good")
		except Exception as err:
			utils.die("[x] GetProxy: Error while writing result", err)