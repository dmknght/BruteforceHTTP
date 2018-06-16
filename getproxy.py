import mechanize, re, sys, os
from core import actions, utils

"""
support url:
https://free-proxy-list.net/
"""

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
		getproxy = actions.createBrowserObject()
		user_agent = actions.getUserAgent()
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
			location = "data/liveproxy.txt"
			utils.printf("Write data to %s." %(location))
			actions.writeDataToFile(location, listproxy)
			utils.printf("Write data to %s completed!" %(location), "good")

		except Exception as error:
			utils.die("Error while writting proxy data", error)
		
# def check(threads = 16):
#	#Check Multithread
# 	import threading
# 	try:
# 		proxylist = actions.loadDataFromFile("data/liveproxy.txt")
# 
# 	except Exception as error:
# 		utils.die("You must get proxy list before checking it", error)
# 
# 	try:
# 		workers = []
# 		for i in xrange(threads):
# 			worker = threading.Thread(
# 				target = checkAllProxy,
# 				args = (proxylist,)
# 			)
# 			workers.append(worker)
# 
# 	except Exception as error:
# 		utils.die("Error while checking", error)	
# 
# 	try:	
# 		for worker in workers:
# 			worker.daemon = True
# 			worker.start()
# 
# 	except KeyboardInterrupt:
# 		utils.die("Terminated by user", error)
# 
# 	except Exception as error:
# 		utils.die("Error while checking", error)
# 
# 	finally:
# 		try:
# 			proxylist.close()
# 		except:
# 			pass

def check():
	try:
		proxylist = actions.loadDataFromFile("data/liveproxy.txt")
		checkAllProxy(proxylist)
	except KeyboardInterrupt as error:
		utils.die("Terminated by user!", error)
	except Exception as error:
		utils.die("Error while checking live proxy", error)
	
def checkAllProxy(proxyList):
	for proxyAddr in proxyList:
		proxyAddr = proxyAddr.replace("\n", "")
		#connProxy(proxyAddr)
		result = connProxy(proxyAddr)
		if result:
			pass #write new data to file here


def connProxy(proxyAddr):
	try:
		proxyTest = actions.createBrowserObject()
		#utils.printf(proxyAddr)
		proxyTest.set_proxies({"http": proxyAddr})
		proxyTest.open("https://google.com")
		utils.printf(proxyAddr, "good")
		return proxyAddr
	except Exception as error:
		utils.die(proxyAddr, error)
		return None
	finally:
		try:
			proxyTest.close()
		except:
			pass
		
	
if __name__ == "__main__":
	current_dir = actions.getProjectRootDirectory(sys.argv[0])
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
			utils.die("Invalid option!", "Usage:\n\tpython getproxy.py help")