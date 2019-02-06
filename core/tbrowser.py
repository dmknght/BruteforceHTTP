import data, re
from core.actions import randomFromList

def startBrowser(timeout):
	import mechanize
	#https://stackoverflow.com/a/27096416
	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	browser.set_handle_referer(True)
	browser.set_handle_redirect(True)
	browser.set_handle_equiv(True)
	browser.set_handle_refresh(True)
	browser.timeout = timeout
	browser._factory.is_html = True #https://stackoverflow.com/a/4201003
	browser.addheaders = [('User-Agent', useragent())]
	return browser

def useragent():
	return randomFromList(data.getAgent().split("\n"))

def checkHTTPGetLogin(strHeader):
	reg = r"WWW-Authenticate: Basic realm=\"(.*)\""
	try:
		return re.findall(reg, strHeader, re.MULTILINE)[0]
	except:
		return False

def parseLoginForm(objForm):
	regTextField = r"TextControl\W(.*)="
	regPassField = r"PasswordControl\W(.*)="

	for retFormID, form in enumerate(objForm):
		retPassField = re.findall(regPassField, str(form), re.MULTILINE)
		# Find password control. If has
		# 	1 password control -> login field
		# 	2 or more password control -> possibly register field
		if len(retPassField) == 1:
			retTextField = re.findall(regTextField, str(form), re.MULTILINE)
			if len(retTextField) == 1:
				# Regular login field. > 1 can be register specific field (maybe captcha)
				return (retFormID, [retPassField[0], retTextField[0]])
			elif len(retTextField) == 0:
				# Possibly password field login only
				return (retFormID, [retPassField[0]])
	return None

def sqlerror(response):
	# Parse html response to define SQL error
	# Copyright: SQLmap
	if re.search(r"SQL (warning|error|syntax)", response, re.MULTILINE):
		return True
	return False
	# TODO improve condition