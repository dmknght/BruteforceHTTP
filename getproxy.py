import mechanize, re, sys, os, threading
from core import actions, utils, tbrowser


"""
support url:
https://free-proxy-list.net/
"""

THREADS = 10
PROXY_PATH = "data/liveproxy.txt"
TMP_PATH = "proxies.tmp"

def help():
	print("""
	\rUsage: python getproxy.py <options>
	\rOptions:
	\r    [*] help / --help / -h: Display help banner
	\r    [*] get: Save new proxy list
	\r    [*] check: Check live proxy from list
	\r               Requires an exist list
	""")

def get_proxy_list(url = "https://free-proxy-list.net/"):
	try:
		utils.printf("Connecting to %s." %(url))
		# getproxy = mechanize.Browser()
		# getproxy.set_handle_robots(False)

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


def parse_proxy(response):
	try:
		re_ip = r"\b(?:\d{1,3}\.){3}\d{1,3}\b<\/td><td>\d{1,5}"
		result = re.findall(re_ip, response, re.MULTILINE)
		result = [element.replace("</td><td>", ":") for element in result]
		return result
	except Exception as error:
		utils.die("Error while parsing proxy list.", error)

def refresh():
	try:
		listproxy = parse_proxy(get_proxy_list())
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
	# Single thread
	try:
		
		proxylist = actions.fload(PROXY_PATH)
		
		#actions.fwrite(TMP_PATH, "") # create new empty list
		
		workers = []
		for i in xrange(THREADS):
			worker = threading.Thread(
				target = checkAllProxy,
				args = (proxylist, target,)
			)
			workers.append(worker)
			
		for worker in workers:
			worker.daemon = True
			worker.start()	

	except KeyboardInterrupt as error:
		utils.die("Terminated by user!", error)
	except Exception as error:
		utils.die("Error while checking live proxy", error)

	finally:
		try:
			for worker in workers:
				worker.join()
		except:
			pass


def checkAllProxy(proxyList, target):
	try:
		for proxyAddr in proxyList:
			proxyAddr = proxyAddr.replace("\n", "")

			result = connProxy(proxyAddr, target)
			if result:
				#livelist.append(result)
				actions.fwrite_c(TMP_PATH, "%s\n" %(proxyAddr)) #TODO use queu here

	except Exception as error:
		utils.printf(error, "bad")

	# finally:
	# 	return "\n".join(livelist)


def connProxy(proxyAddr, target):
	try:
		proxyTest = tbrowser.startBrowser()
		user_agent = tbrowser.useragent()
		proxyTest.addheaders = [('User-Agent', user_agent)]
		utils.printf(proxyAddr)
		proxyTest.set_proxies({"http": proxyAddr})
		proxyTest.open(target)
		utils.printf(proxyAddr, "good")
		return proxyAddr
	except Exception as error:
		utils.printf("%s %s" %(proxyAddr, error), "bad")
		return None
	finally:
		try:
			proxyTest.close()
		except:
			pass


if __name__ == "__main__":
	current_dir = actions.getRootDir(sys.argv[0])
	if current_dir:
		os.chdir(current_dir)
	if len(sys.argv) == 1:
		help()
	elif len(sys.argv) == 2:
		option = sys.argv[1]
		if option in ["help", "--help", "-h"]:
			help()
		elif option == "get":
			refresh()
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