import data, re
from cores.actions import randomFromList
from mechanicalsoup.stateful_browser import StatefulBrowser

"""
	Rewrite all methods
	Goal: Attack modules call same method name, so switch to selenium can be much more easier
"""

class Browser(StatefulBrowser):
	def __init__(self):
		super(Browser, self).__init__()
		#	Create browser object. All browser settings should be here
		#https://stackoverflow.com/a/27096416
		# self.set_handle_robots(False)
		# self.set_handle_referer(True)
		# self.set_handle_redirect(True)
		# self.set_handle_equiv(True)
		# self.set_handle_refresh(True)
		# self.timeout = timeout
		# self._factory.is_html = True #https://stackoverflow.com/a/4201003
		self.addheaders = [('User-Agent', self.useragent())]

	def useragent(self):
		# Try random agent everytime it is called
		# TODO better useragent with library (or create my own - takes time)
		return randomFromList(data.getAgent().split("\n"))
	
	def setproxy(self, proxyaddr):
		self.session.proxies = ({"http": proxyaddr})

	def open_url(self, url):
		return self.open(url)

	# def get_opts(self, options):
	# 	pass

	def url(self):
		return self.get_url()

	def get_resp(self):
		try:
			return str(self.get_current_page())
		except UnicodeEncodeError:
			return str(self.get_current_page().encode('utf-8'))
	
	def get_title(self):
		try:
			return str(self.get_current_page().title.text)
		except UnicodeEncodeError:
			return str(self.get_current_page().title.text.encode('utf-8'))
		except:
			return "No title"

	def xsubmit(self, controls, fields, creds):
		formID, button = controls
		loginForm = self.select_form(nr = formID)
		# FILLS ALL FIELDS https://stackoverflow.com/a/5389578
		for field, cred in zip(fields, creds):
			loginForm.set(field, cred)
		return self.submit_selected()

	def close(self):
		try:
			self.close()
		except:
			pass
		# TODO print error using verbose mode
