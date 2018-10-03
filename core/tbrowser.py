import data, re
from core import actions, utils

def startBrowser():
	import mechanize
	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	browser.set_handle_referer(True)
	browser.set_handle_redirect(True)
	browser.set_handle_equiv(True)
	browser.set_handle_refresh(True) 
	#browser._factory.is_html = True #https://stackoverflow.com/a/4201003
	return browser

def parsePasswdForm(objBrowserForm):
	##########################################
	#	Get Password-only form
	#	Need form ID for select_form(nr = ID)
	#	Password field's name for submiting
	#
	###########################################

	# Using for loop for getting
	retFormID = 0

	regPassField = r"PasswordControl\W(.*)="

	# Find login form
	for form in objBrowserForm:
		try:
			#retTextField = re.findall(regTextField, str(form).encode('utf-8'), re.MULTILINE)[0]
			#retPassField = re.findall(regPassField, str(form).encode('utf-8'), re.MULTILINE)[0]
			retPassField = re.findall(regPassField, str(form), re.MULTILINE)[0]
			return (retFormID, [retPassField, retTextField])
		except:
			retFormID += 1
	return None

def parseLoginForm(objBrowserForm):
	##########################################
	#	Get Login Form Information
	#	Need form ID for select_form(nr = ID)
	#	Username field's name for submiting
	#	Password field's name for submiting
	#
	#	*** NEED IMPROVE ***
	#
	###########################################

	# Using for loop for getting
	retFormID = 0

	regTextField = r"TextControl\W(.*)="
	regPassField = r"PasswordControl\W(.*)="

	# Find login form
	for form in objBrowserForm:
		try:
			#retTextField = re.findall(regTextField, str(form).encode('utf-8'), re.MULTILINE)[0]
			#retPassField = re.findall(regPassField, str(form).encode('utf-8'), re.MULTILINE)[0]
			retTextField = re.findall(regTextField, str(form), re.MULTILINE)[0]
			retPassField = re.findall(regPassField, str(form), re.MULTILINE)[0]
			return (retFormID, [retPassField, retTextField])
		except:
			retFormID += 1
	return None
	
def useragent():
	agents = data.getAgent()
	
	return actions.randomFromList(agents.split("\n"))
	
	
def getLoginForm(optionURL, browser, verbose):
	######################################
	#	Test connect to URL
	#	Fetch login field
	#
	#####################################

	try:
		
		browser.open(optionURL)
		
		formInfo = parseLoginForm(browser.forms())
		if verbose:
			utils.printf("[*] Found login form", "good")
		return formInfo

	# except TypeError as error:
	# 	utils.die("getLoginForm: Can not find login form", error)

	except Exception as error:
		utils.die("getLoginForm: Runtime error", error)