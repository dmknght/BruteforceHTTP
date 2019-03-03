import data, re
from cores.actions import randomFromList

def startBrowser(timeout):
	#	Create browser object. All browser settings should be here
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
	# Try random agent everytime it is called
	# TODO better useragent with library (or create my own - takes time)
	return randomFromList(data.getAgent().split("\n"))

def checkHTTPGetLogin(strHeader):
	reg = r"WWW-Authenticate: Basic realm=\"(.*)\""
	try:
		return re.findall(reg, strHeader, re.MULTILINE)[0]
	except:
		return False

def parseLoginForm(allFormControl):
	# Try detect login form from all forms in response. Return form information
	reTextControl = r"TextControl\W(.*)="
	rePasswdControl = r"PasswordControl\W(.*)="

	for uint_formID, form in enumerate(allFormControl):
		txtPasswdControl = re.findall(rePasswdControl, str(form), re.MULTILINE)
		# Find password control. If has
		# 	1 password control -> login field
		# 	2 or more password control -> possibly register field
		if len(txtPasswdControl) == 1:
			txtTextControl = re.findall(reTextControl, str(form), re.MULTILINE)
			if len(txtTextControl) == 1:
				# Regular login field. > 1 can be register specific field (maybe captcha)
				return (uint_formID, [txtPasswdControl[0], txtTextControl[0]])
			elif len(txtTextControl) == 0:
				# Possibly password field login only
				return (uint_formID, [txtPasswdControl[0]])
	return None

def sqlerror(response):
	# Parse html response to define SQL error
	# Copyright: SQLmap
	if re.search(r"SQL (warning|error|syntax)", response, re.MULTILINE):
		return True
	return False
	# TODO improve condition