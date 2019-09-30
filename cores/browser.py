import data
from mechanicalsoup.stateful_browser import StatefulBrowser


def random_user_agent():
	"""
	Generate agent of client randomly
	:return: string = agent value (PC)
	"""
	# TODO better useragent with library (or create my own - takes time)
	from cores.actions import list_choose_randomly
	return list_choose_randomly(data.getAgent().split("\n"))


class Browser(StatefulBrowser):
	def __init__(self, *args, **kwargs):
		super(Browser, self).__init__()
		# Create browser object. All browser settings should be here
		# https://stackoverflow.com/a/27096416
		# self.set_handle_robots(False)
		# self.set_handle_referer(True)
		# self.set_handle_redirect(True)
		# self.set_handle_equiv(True)
		# self.set_handle_refresh(True)
		# self.timeout = timeout
		# self._factory.is_html = True #https://stackoverflow.com/a/4201003
		# self.addheaders = [('User-agent', self.useragent())]
		self.set_user_agent(random_user_agent())

	def set_random_proxy(self, proxyaddr):
		"""
		Set a proxy of browser randomly
		:param proxyaddr: string:{<IP>:<Port>} = address of proxy in http method
		:return: True
		"""
		self.session.proxies = ({"http": proxyaddr})

	def open_url(self, url, *args, **kwargs):
		"""
		Open url
		:param url: string: {http[s]://domain.com/foo/bar} = URL of target
		:param args:
		:param kwargs:
		:return: True
		"""
		return self.open(url, verify=False, *args, **kwargs)

	def get_response(self):
		"""
		Get server response for the request
		:return: string = server response
		"""
		try:
			return str(self.get_current_page())
		except UnicodeEncodeError:
			return str(self.get_current_page().encode('utf-8'))

	def get_title(self):
		"""
		Get title from http response
		:return: string = title of the page
		"""
		try:
			page_title = str(self.get_current_page().title.text)
		except UnicodeEncodeError:
			page_title = str(self.get_current_page().title.text.encode('utf-8'))
		except:
			page_title = "No title"
		finally:
			return page_title.replace("\n", "").replace("\r", "").replace("\t", "")

	def form_submit(self, controls, fields, send_data):
		"""
		Fill all fields and submit request
		:param controls: list of string = all information about form control
		:param fields: list of string = all information about form fields
		:param send_data: list of string = username and password
		:return: object_form_submit
		:refer: https://stackoverflow.com/a/5389578
		"""
		# form_id, button = controls

		# Get position of form to select
		form_id = controls[0]
		select_login_form = self.select_form(nr=form_id)

		# Fill all fields with values by zip loop
		for field, cred in zip(fields, send_data):
			select_login_form.set(field, cred)
		return self.submit_selected()
