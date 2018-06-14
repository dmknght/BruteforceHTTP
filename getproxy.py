import mechanize, re, utils, actions

"""
support url:
https://free-proxy-list.net/
https://free-proxy-list.net/
"""

def get_proxy_list(url = "https://free-proxy-list.net/"):
	try:
		getproxy = mechanize.Browser()
		getproxy.set_handle_robots(False)
		user_agent = actions.getUserAgent()
		getproxy.addheaders = [('User-Agent', user_agent)]
		getproxy.open(url)
		return getproxy.response().read()
		
	except Exception as error:
		utils.die("Error while getting proxy list", error)
	finally:
		getproxy.close()
		
		
def parse_proxy(data):
	try:
		re_ip_and_port = r"\b(?:\d{1,3}\.){3}\d{1,3}\b<\/td><td>\d{1,5}"
		result = re.findall(re_ip_and_port, data, re.MULTILINE)
		result = [element.replace("</td><td>", ":") for element in result]
		return result
	except Exception as error:
		utils.die("Error while parsing proxy list", error)
	
if __name__ == "__main__":
	data = get_proxy_list("https://free-proxy-list.net/")
	data = parse_proxy(data)
	#print data