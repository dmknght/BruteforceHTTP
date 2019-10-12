from utils import events
import re


def check_sqlerror(response):
	"""
	Check all sql error text returns in http response
	:param response: string = response of server
	:return:
		True if found any result like it
		False if not found
	@Copyright: wapiti
	"""
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


def get_response_diff(first_content, current_content):
	"""
	Analysis different in response data
	:param first_content: string = body of server html responses in first time
	:param current_content: string = current body of server html response
	:return:
		source_diff: string = New text appears in html source
		text_diff: string = New text appears in html view [html2text]
	"""
	import html2text
	convert = html2text.HTML2Text()

	text_diff, source_diff = "", ""
	
	# 2 loops: fix bug lines(source) > lines(text)
	
	for src_line in current_content.split("\n"):
		source_diff += src_line if src_line not in first_content else ""
	
	for line in convert.handle(current_content).split("\n"):
		text_diff += line if line not in convert.handle(first_content) else ""
	
	return text_diff, source_diff


def get_redirection(response):
	"""
	Analysis all redirection request in html response via meta tag, windows.location or href
	:param response: string = server response html
	:return: list of string = all possible URL
	"""
	regex_js = r"window\.location(?:[a-zA-Z\.\ \=\(])+\"|\'(.*)\"|\'"
	regex_meta = r"<meta[^>]*?url=(.*?)[\"\']"
	regex_href = r"href=[\'\"]?([^\'\" >]+)"
	
	url = list(set(re.findall(regex_meta, response)))
	if url:
		return url

	url = list(set(re.findall(regex_js, response)))
	if url:
		return url

	url = list(set(re.findall(regex_href, response)))
	return url
