from cores.check import parseLoginForm
from utils import events
import re


def check_login(options, proc, loginInfo):
	"""
		Check logged in successfully condition.
		This function will check SQL injection as well
			return 0 -> False
			return 1 -> True
			return 2 -> Should be SQL Injection error-based
	"""
	# TODO check diff response instead of whole
	if options.panel_url:
		# User provided panel url (/wp-admin/ for example, repopen this url to check sess)
		proc.open_url(options.panel_url)
		if not parseLoginForm(proc.forms()):  # != loginInfo:
			if check_sqlerror(proc.get_resp()):
				return 2
			else:
				return 1
		else:
			return 0
	else:
		# User provided direct login URL (/wp-login.php).
		# DEBUG
		# proc.open(options.url)
		# if parseLoginForm(proc.forms()) != loginInfo:
		# 	return 1
		# else:
		# 	return 0
		if check_sqlerror(proc.get_resp()):
			return 2
		else:
			return 1


def check_sqlerror(response):
	# if re.search(r"SQL (warning|error|syntax)", response):
	# TODO add condition -> don't have to loop all time
	# COPYRIGHT: wapiti ..
	signatures = {
		"MySQL Injection": [
			"You have an error in your SQL syntax",
			"supplied argument is not a valid MySQL",
			"mysql_fetch_array() expects parameter 1 to be resource, boolean given in"
		],
		"Java SQL Injection": [
			"java.sql.SQLException: Syntax error or access violation",
			"java.sql.SQLException: Unexpected end of command"
		],
		"PostgreSQL Injection": [
			"PostgreSQL query failed: ERROR: parser:",
		],
		"XPathException": [
			"XPathException",
			"Warning: SimpleXMLElement::xpath():"
		],
		"MSSQL Injection": [
			"[Microsoft][ODBC SQL Server Driver]",
			"Microsoft OLE DB Provider for ODBC Drivers</font> <font size=\"2\" face=\"Arial\">error",
			"Microsoft OLE DB Provider for ODBC Drivers",
		],
		"MSAccess SQL Injection": [
			"[Microsoft][ODBC Microsoft Access Driver]",
		],
		"LDAP Injection": [
			"supplied argument is not a valid ldap",
			"javax.naming.NameNotFoundException"
		],
		"DB2 Injection": [
			"DB2 SQL error:"
		],
		"Interbase Injection": [
			"Dynamic SQL Error",
		],
		"Sybase Injection": [
			"Sybase message:",
		],
		".NET SQL Injection": [
			"Unclosed quotation mark after the character string",
		],
	}
	
	for injectType in signatures:
		for error in signatures[injectType]:
			if re.findall(re.escape(error), response):
				events.vuln(injectType)
				return True
	return False


def getdiff(first, content):
	import html2text
	convert = html2text.HTML2Text()

	diff, source_diff = "", ""
	for src_line, line in zip(content.split("\n"), convert.handle(content).split("\n")):
		source_diff += src_line if src_line not in first else ""
		diff += line if line not in convert.handle(first) else ""

	return diff, source_diff

	# diff = ""
	# print(list(convert.handle(content).split("\n")))
	# for line in convert.handle(content).split("\n"):
	# 	diff += line if line not in convert.handle(first) else ""
	#
	# return diff
	

def getredirect(src):
	js_redirection = r"window\.location(?:[a-zA-Z\.\ \=\(])+\"|\'(.*)\"|\'"
	url = re.findall(r"url=(.*?)\'|\">", src.lower())
	return list(set(url))