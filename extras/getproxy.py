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

THREADS = 16
PROXY_PATH = "data/liveproxy.txt"

def help():
	print("""
	\rUsage: python getproxy.py <options>
	\rOptions:
	\r    [*] help / --help / -h: Display help banner
	\r    [*] get: Save new proxy list
	\r    [*] check: Check live proxy from list
	\r               Requires an exist list
	""")


def getNewProxy():
	
	def parse_proxy(response):
		try:
			re_ip = r"\b(?:\d{1,3}\.){3}\d{1,3}\b<\/td><td>\d{1,5}"
			result = re.findall(re_ip, response, re.MULTILINE)
			result = [element.replace("</td><td>", ":") for element in result]
			return result
		except Exception as error:
			utils.die("Error while parsing proxy list.", error)
			
	def checProxyConnProvider(url = "https://free-proxy-list.net/"):
		try:
			utils.printf("Connecting to %s." %(url))

			getproxy = tbrowser.startBrowser()

			user_agent = tbrowser.useragent()
			
			getproxy.addheaders = [('User-Agent', user_agent)]
			getproxy.open(url)
			utils.printf("Gathering proxy completed.", "good")
			return getproxy.response().read()

		except Exception as error:
			utils.die("Error while connecting to live proxy server!", error)
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
			utils.die("Error while writting proxy data", error)


def check(target = "https://google.com"):

	def checProxyConn(proxyAddr, target, result):
		try:
			proxyTest = tbrowser.startBrowser()
			user_agent = tbrowser.useragent()
			proxyTest.addheaders = [('User-Agent', user_agent)]
			utils.printf(proxyAddr)
			proxyTest.set_proxies({"http": proxyAddr})
			proxyTest.open(target)
			utils.printf("Trying: %s" %(proxyAddr), "good")
			result.put(proxyAddr)
		except Exception as error:
			utils.printf("%s %s" %(proxyAddr, error), "bad")
		finally:
			try:
				proxyTest.close()
			except:
				pass
	# Single thread
	try:
		
		proxylist = actions.fread(PROXY_PATH).split("\n")
		
		#actions.fwrite(TMP_PATH, "") # create new empty list
		
		workers = []
		result = Queue()
		for tryProxy in proxylist:
			if len(workers) >= THREADS:
				for worker in workers:
					worker.start()
				for worker in workers:
					worker.join()
				del workers[:]
			
			worker = threading.Thread(
				target = checProxyConn,
				args = (tryProxy, target, result)
			)

			worker.daemon = True
			workers.append(worker)
			
		for worker in workers:
			worker.start()	
		for worker in workers:
			workers.join()

	except KeyboardInterrupt as error:
		utils.die("Terminated by user!", error)
	except Exception as error:
		utils.die("Error while checking live proxy", error)

	finally:
		try:
			open("data/liveproxy.txt", "w").write("\n".join(list(result.queue))) #TODO better code
		except Exception as err:
			utils.die("Error while writing result", err)
			



if __name__ == "__main__":
	#current_dir = actions.getRootDir(sys.argv[0])
	# if current_dir:
	# 	os.chdir(current_dir)
	if len(sys.argv) == 1:
		help()
	elif len(sys.argv) == 2:
		option = sys.argv[1]
		if option in ["help", "--help", "-h"]:
			help()
		elif option == "get":
			getNewProxy()
		elif option == "check":
			check()
		else:
			utils.die("Invalid options!", "Usage:\n\tpython getproxy.py help")
	elif len(sys.argv) == 3:
		option, value = sys.argv[1], sys.argv[2]
		if option == "check":
			check(value)
		else:
			utils.die("Invalid options!", "Usage:\n\tpython getproxy.py help")