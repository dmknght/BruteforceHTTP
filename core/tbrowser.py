import data, actions, re

def startBrowser():
	import mechanize
	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	browser.set_handle_referer(True)
	browser.set_handle_redirect(True)
	browser.set_handle_equiv(True)
	return browser
	
def getLoginForm(objBrowserForm):
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
	for idxSingleForm in objBrowserForm:
		try:
			#retTextField = re.findall(regTextField, str(idxSingleForm).encode('utf-8'), re.MULTILINE)[0]
			#retPassField = re.findall(regPassField, str(idxSingleForm).encode('utf-8'), re.MULTILINE)[0]
			retTextField = re.findall(regTextField, str(idxSingleForm), re.MULTILINE)[0]
			retPassField = re.findall(regPassField, str(idxSingleForm), re.MULTILINE)[0]
			#objBrowserForm.close() #This is seems useless
			return retFormID, retTextField, retPassField
		except:
			retFormID += 1
	return None
	
def useragent():
	agents = data.getAgent()
	
	return actions.randomFromList(agents.split("\n"))