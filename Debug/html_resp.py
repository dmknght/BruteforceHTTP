import mechanize, sys

if len(sys.argv) == 1:
	print "Need URL"

else:
	url = sys.argv[1]
	browser = mechanize.Browser()
	browser.set_handle_robots(False)
	browser.set_handle_referer(True)
	browser.set_handle_redirect(True)
	browser.set_handle_equiv(True)
	browser.set_handle_refresh(True)

	browser.open(url)

	print browser.response().read()

	browser.close()