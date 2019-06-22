############################
#	Selenium - based browser
#	++: Support javascript by default
#	--: Must install drivers,...
#		Doesn't support form object by default
############################

"""
	Firefox: Slow
	Suggestion using chrome
	Set chromium by default
"""
from selenium.webdriver import ChromeOptions
from selenium.webdriver import Chrome
import bs4


class sBrowser(Chrome):
	def __init__(self, driver_path="/usr/local/bin/chromedriver", port=0, chrome_options=None, service_args=None, desired_capabilities=None, service_log_path=None):
		chrome_options = ChromeOptions()
		chrome_options.headless = True
		super(sBrowser, self).__init__(driver_path, port, chrome_options, service_args, desired_capabilities, service_log_path)
		self.options = None

	def useragent(self):
		pass

	def setproxy(self, addr):
		pass

	def open_url(self, url):
		self.get(url)
	
	def get_opts(self, options):
		self.options = options

	def geturl(self):
		pass

	def get_resp(self):
		return self.page_source
	
	def get_title(self):
		pass


	def forms(self):
		"""Get a summary of the form with classic mechanize style

		"""
		for form in bs4.BeautifulSoup(self.page_source, features="lxml").find_all('form'):
			info = "<%s[%s]>\n" %(form.get('method'), form.get('action'))
			for fields in form.find_all(("input", "textarea", "select", "button")):
				fType = fields.get('type') or None
				fID = fields.get('id') or None
				fValue = fields.get('value') or None
				fName = fields.get('name') or None

				fID = fName if fName else fID
				info += "  %s(%s)=\'%s\'\n" %(fType, fID, fValue)

			yield info
	
	# def forms(self):
	# 	forms = self.find_elements_by_css_selector("form")
	# 	# Get source code of form element self.get_attribute('innerHTML') https://stackoverflow.com/a/8575709
	# 	# Find by type https://stackoverflow.com/a/48365300
	# 	return forms
	# def forms(self):
	# 	response = self.get_resp()
	# 	response = self.options.bresp.set_data(str(response)) # BUG
	# 	self.options.bbrowser.set_response(response)
	# 	return self.options.bbrowser.forms()

	def xsubmit(self, controls, fields, creds):
		_, button = controls
		for field, cred in zip(fields, creds):
			self.find_element_by_name(field).send_keys(cred)
		
		# usrField, passField = fields
		# usrname, passwd = creds
		# self.find_element_by_name(usrField).send_keys(usrname)
		# self.find_element_by_name(passField).send_keys(passwd)
		if button[0]:
			self.find_element_by_name(button[0]).click()
		else:
			print("Can't click") # DEBUG
			pass # https://stackoverflow.com/a/35532972

	def close(self):
		# TODO add clear storage data here
		try:
			self.quit()
		except:
			pass

# def startBrowser():
# 	# 1. Download webdriver and throw it into PATH (make sure it can be executed - 755)
# 	# 2. Install chromium
# 	try:
# 		options = webdriver.chrome.options.Options()
# 		options.headless = True

# 		brow = webdriver.Chrome(chrome_options=options)
# 		# brow.get('http://giapbat.gsatgt.vn:8088/#/login')
# 		# brow.get(url)

# 		# resp = str("%s" %(brow.page_source))

# 		# import mechanize
# 		# mbrow = mechanize.Browser()
# 		# # mresp = mbrow.open('http://giapbat.gsatgt.vn:8088/#/login')
# 		# mresp = mbrow.open(url)
# 		# mresp.set_data(resp)
# 		# mbrow.set_response(mresp)
# 		# # Parse login form here
# 		# from cores.mbrowser import parseLoginForm
# 		# lInfo = parseLoginForm(mbrow.forms())
# 		# if not lInfo:
# 		# 	print "Exit! No login form"
# 		# else:
# 		# 	fid, info = lInfo
# 		# 	fid, btn = fid
# 		# 	passField, usrField = info
# 		# 	for form in mbrow.forms():
# 		# 		print form
# 		# 	brow.find_element_by_name(usrField).send_keys("admin")
# 		# 	brow.find_element_by_name(passField).send_keys("admin")
# 		# 	brow.find_element_by_name(btn).click()

# 		# 	print brow.title
# 			# form = brow.find_element_by_id('id')
# 			# form.submit()
# 			# if "Sai" in brow.page_source:
# 			# 	print "Failed"
# 			# else:
# 			# 	print "Not sure"

# 			# for form in mbrow.forms():
# 			# 	print form
# 		# Test submit with mechanize
# 		# Done well with non java script sites
# 			# mbrow.select_form(nr = fid)
# 			# mbrow.form[usrField] = 'admin'
# 			# mbrow.form[passField] = 'admin'
# 			# mbrow.submit()
# 			# # print mbrow.title()
# 			# print mbrow.geturl()
# 			# print mbrow.response().read()

# 		# Test submit with selenium
		
# 	except Exception as error:
# 		print error
# 	finally:
# 		try:
# 			brow.quit()
# 		except:
# 			pass

