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
from selenium import webdriver
import time, sys
reload(sys)
sys.setdefaultencoding('utf8')

def firefox():
	# 1. Download firefox webdriver and throw it into PATH
	# 2. Install Firefox
	# Run firefox in background
	options = webdriver.firefox.options.Options()
	options.headless = True

	# Set profile settings. Proxy and user agent,...
	# profile = webdriver.FirefoxProfile()
	# profile.set_preference()
	try:
		brow = webdriver.Firefox(options=options)
		brow.get('http://192.168.56.103/dvwa/login.php')
		print brow.title
	except Exception as error:
		print error
	finally:
		try:
			brow.quit()
		except:
			pass

# url = 'http://192.168.56.103/mutillidae/index.php?page=login.php'
url = "http://192.168.56.103/dvwa/login.php"

def chrome():
	# 1. Download webdriver and throw it into PATH (make sure it can be executed - 755)
	# 2. Install chromium
	try:
		options = webdriver.chrome.options.Options()
		options.headless = True

		brow = webdriver.Chrome(chrome_options=options)
		# brow.get('http://giapbat.gsatgt.vn:8088/#/login')
		brow.get(url)

		resp = str("%s" %(brow.page_source))

		import mechanize
		mbrow = mechanize.Browser()
		# mresp = mbrow.open('http://giapbat.gsatgt.vn:8088/#/login')
		mresp = mbrow.open(url)
		mresp.set_data(resp)
		mbrow.set_response(mresp)
		# Parse login form here
		from cores.mbrowser import parseLoginForm
		lInfo = parseLoginForm(mbrow.forms())
		if not lInfo:
			print "Exit! No login form"
		else:
			fid, info = lInfo
			fid, btn = fid
			passField, usrField = info
			for form in mbrow.forms():
				print form
			brow.find_element_by_name(usrField).send_keys("admin")
			brow.find_element_by_name(passField).send_keys("admin")
			brow.find_element_by_name(btn).click()

			print brow.title
			# form = brow.find_element_by_id('id')
			# form.submit()
			# if "Sai" in brow.page_source:
			# 	print "Failed"
			# else:
			# 	print "Not sure"

			# for form in mbrow.forms():
			# 	print form
		# Test submit with mechanize
		# Done well with non java script sites
			# mbrow.select_form(nr = fid)
			# mbrow.form[usrField] = 'admin'
			# mbrow.form[passField] = 'admin'
			# mbrow.submit()
			# # print mbrow.title()
			# print mbrow.geturl()
			# print mbrow.response().read()

		# Test submit with selenium
		
	except Exception as error:
		print error
	finally:
		try:
			brow.quit()
		except:
			pass

runtime = time.time()
chrome()
# firefox()

print "Elasped: %s" %(time.time() - runtime)

