import data, re
from core import actions, utils

def startBrowser():
	import mechanize
	#https://stackoverflow.com/a/27096416
	#browser = mechanize.Browser(factory=mechanize.RobustFactory())
	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	browser.set_handle_referer(True)
	browser.set_handle_redirect(True)
	browser.set_handle_equiv(True)
	browser.set_handle_refresh(True) 
	browser._factory.is_html = True #https://stackoverflow.com/a/4201003
	return browser

def useragent():
	agents = data.getAgent()
	
	return actions.randomFromList(agents.split("\n"))

def checkPasswdForm(objBrowserForm):
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
			return (retFormID, [retPassField])
		except:
			retFormID += 1
	return None

def checkLoginForm(objBrowserForm):
	##########################################
	#	Get Login Form Information
	#	Need form ID for select_form(nr = ID)
	#	Username field's name for submiting
	#	Password field's name for submiting
	#
	#	*** TODO NEED IMPROVE ***
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

def parseLoginForm(objForm):
	# https://stackoverflow.com/a/4945175
	import itertools
	form1, form2 = itertools.tee(objForm)

	login, passwd = checkLoginForm(form1), checkPasswdForm(form2)

	if login:
		return login
	elif passwd:
		return passwd
	else:
		return None