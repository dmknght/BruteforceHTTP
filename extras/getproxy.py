import re, threading, sys
from cores.browser import Browser
from utils import progressbar, events
from cores.actions import fread, fwrite
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
PROXY_PATH = "%s%s" % (ROOT_FOLDER, "/listproxy.txt")
LIVE_PATH = "%s%s" % (ROOT_FOLDER, "/liveproxy.txt")


def livelist():
	return fread(LIVE_PATH).split("\n")


def getlist():
	return fread(PROXY_PATH).split("\n")


def getnew(options):
	def parse_proxy(response):
		try:
			re_ip = r"\b(?:\d{1,3}\.){3}\d{1,3}\b<\/td><td>\d{1,5}"
			result = re.findall(re_ip, response)
			result = [element.replace("</td><td>", ":") for element in result]
			return result
		except Exception as error:
			events.error("%s" % (error), "PROXY")
	
	def checkProxyConnProvider(url = "https://free-proxy-list.net/"):
		try:
			events.info("Gathering proxies from %s" % (url))
			
			getproxy = Browser()
			
			getproxy.open_url(url)
			events.success("Gathering proxies completed", "PROXY")
			return getproxy.get_resp()
		
		except Exception as error:
			events.error("%s" % (error), "PROXY")
			sys.exit(1)
		finally:
			getproxy.close()
	
	try:
		listproxy = parse_proxy(checkProxyConnProvider())
	except Exception as error:
		events.error("%s" % (error), "PROXY")
		listproxy = ""
	finally:
		try:
			events.success("Gathered %s proxies" % (len(listproxy)), "PROXY")
			listproxy = "\n".join(listproxy)
			
			events.info("Saving result to %s" %(PROXY_PATH), "PROXY")
			fwrite(PROXY_PATH, listproxy)
			events.success("New proxy list saved", "PROXY")
		
		except Exception as error:
			events.error("%s" % (error), "PROXY")
			sys.exit(1)


def check(options):
	def run_threads(threads, sending, completed, total):
		# Run threads
		for thread in threads:
			# sending += 1 # Sending
			progressbar.progress_bar(sending, completed, total)
			thread.start()
		
		# Wait for threads completed
		for thread in threads:
			completed += 1
			progressbar.progress_bar(sending, completed, total)
			thread.join()
		
		return completed
	
	def checProxyConn(proxyAddr, target, result, verbose):
		try:
			proxyTest = Browser()
			proxyTest.setproxy(proxyAddr)
			
			if verbose:
				events.info("Testing %s" % (proxyAddr))
			
			proxyTest.open_url(target)
			
			if verbose:
				events.success("Connected via %s" %(proxyAddr), "PROXY")
			result.put(proxyAddr)
			
		except KeyboardInterrupt:
			events.error("Terminated by user", "STOPPED")
			global set_break
			set_break = True
		
		except Exception as error:
			if verbose:
				events.error("[%s] [%s]" % (proxyAddr, error))
		finally:
			try:
				proxyTest.close()
			except:
				pass
	
	try:
		proxylist = fread(PROXY_PATH).split("\n")
		
		workers = []
		completed, total = 0, len(proxylist)
		
		set_break = False
		for trying, tryProxy in enumerate(proxylist):
			if set_break:
				del workers[:]
				break
			if len(workers) == options.threads:
				completed = run_threads(workers, trying, completed, total)
				del workers[:]
			
			worker = threading.Thread(
				target = checProxyConn,
				args = (tryProxy, options.url, result, options.verbose)
			)
			
			worker.daemon = True
			workers.append(worker)
		
		completed = run_threads(workers, trying, completed, total)
		del workers[:]
	
	except Exception as error:
		events.error("%s" % (error), "PROXY")
		sys.exit(1)
	
	finally:
		try:
			_data = "\n".join(list(result.queue))
			events.success("%s proxy alive" %(len(_data.split("\n"))))
			events.info("Saving success list", "PROXY")
			fwrite(LIVE_PATH, _data)
			events.success("New alive list is saved", "PROXY")
		except Exception as error:
			events.error("%s" % (error), "PROXY")
			sys.exit(1)
