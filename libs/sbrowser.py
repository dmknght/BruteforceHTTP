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
		chrome_options.add_argument("--incognito")
		super(sBrowser, self).__init__(driver_path, port, chrome_options, service_args, desired_capabilities, service_log_path)
		self.options = None

	def useragent(self, agent):
		# self.chrome_options.add_argument('--user-agent=%s' %(agent))
		pass

	def setproxy(self, addr):
		pass
		# chrome_options.add_argument('--proxy-server=%s' %(addr))

	def open_url(self, url):
		self.get(url)
	
	def get_opts(self, options):
		self.options = options

	def url(self):
		return self.current_url

	def get_resp(self):
		return self.page_source
	
	def get_title(self):
		return self.title

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

	def xsubmit(self, controls, fields, creds):
		_, button = controls
		for field, cred in zip(fields, creds):
			self.find_element_by_id(field).send_keys(cred)
		
		return self.find_element_by_id(button).click()
		# if button[0]:
		# 	self.find_element_by_name(button[0]).click()
		# else:
		# 	print("Can't click") # DEBUG
			# pass # https://stackoverflow.com/a/35532972

	def close(self):
		try:
			self.quit()
		except:
			pass


