import mechanize, re, sys, os, threading
from core import actions, utils, tbrowser

try:
	from Queue import Queue
except ImportError:
	from queue import Queue
"""
support url:
https://free-proxy-list.net/
"""

# BUG: import modules error


def getNewProxy(PROXY_PATH):
	
	def parse_proxy(response):
		try:
			re_ip = r"\b(?:\d{1,3}\.){3}\d{1,3}\b<\/td><td>\d{1,5}"
			result = re.findall(re_ip, response, re.MULTILINE)
			result = [element.replace("</td><td>", ":") for element in result]
			return result
		except Exception as error:
			utils.die("GetProxy: Error while parsing proxies.", error)
			
	def checProxyConnProvider(url = "https://free-proxy-list.net/"):
		try:
			utils.printf("Connecting to %s." %(url))

			getproxy = tbrowser.startBrowser()

			user_agent = tbrowser.useragent()
			
			getproxy.addheaders = [('User-Agent', user_agent)]
			getproxy.open(url)
			utils.printf("Gathering proxies completed.", "good")
			return getproxy.response().read()

		except Exception as error:
			utils.die("GetProxy: Error while connecting to proxy server!", error)
		finally:
			getproxy.close()
			

	try:
		listproxy = parse_proxy(checProxyConnProvider())
	except:
		listproxy = ""
	finally:
		try:
			listproxy = "\n".join(listproxy)
			utils.printf("Write data to %s." %(PROXY_PATH))
			actions.fwrite(PROXY_PATH, listproxy)
			utils.printf("Write data to %s completed!" %(PROXY_PATH), "good")

		except Exception as error:
			utils.die("GetProxy: Error while writting data", error)


def check(target, threads, verbose, PROXY_PATH):

	def checProxyConn(proxyAddr, target, result, verbose):
		try:
			proxyTest = tbrowser.startBrowser()
			user_agent = tbrowser.useragent()
			proxyTest.addheaders = [('User-Agent', user_agent)]
			proxyTest.set_proxies({"http": proxyAddr})

			if verbose:
				utils.printf("Trying: %s" %(proxyAddr))

			proxyTest.open(target)

			if verbose:
				utils.printf("Success: %s" %(proxyAddr), "good")
			result.put(proxyAddr)

		except Exception as error:
			if verbose:
				utils.printf("%s %s" %(proxyAddr, error), "bad")
		finally:
			try:
				proxyTest.close()
			except:
				pass
	try:
		
		proxylist = actions.fread(PROXY_PATH).split("\n")
				
		workers = []
		result = Queue()
		for tryProxy in proxylist:
			if len(workers) >= threads:
				for worker in workers:
					worker.start()
				for worker in workers:
					worker.join()
				del workers[:]
			
			worker = threading.Thread(
				target = checProxyConn,
				args = (tryProxy, target, result, verbose)
			)

			worker.daemon = True
			workers.append(worker)
			
		for worker in workers:
			worker.start()	
		for worker in workers:
			workers.join()

	except KeyboardInterrupt as error:
		utils.die("GetProxy: Terminated by user!", error)
	except Exception as error:
		utils.die("GetProxy: Error while checking proxy connection to target", error)

	finally:
		try:
			utils.printf("GetProxy: Write working proxies")
			actions.fwrite(PROXY_PATH, "\n".join(list(result.queue)))
			utils.printf("Write working proxies completed", "good")
		except Exception as err:
			utils.die("GetProxy: Error while writing result", err)

def main(URL, threads, verbose):
	try:
		import data
		save = "%s/liveproxy.txt" %(data.__path__[0])
		getNewProxy(save)
		if URL:
			check(URL, threads, verbose, save)
	except Exception as err:
		utils.die("GetProxy: Error while running module", err)
