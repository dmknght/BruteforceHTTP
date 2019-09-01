def info(data, info = "INFO"):
	print("[+] [\033[34m%s\033[00m] %s" % (info, data))


def success(data, info = "INFO"):
	print("[*] [\033[32m%s\033[00m] [\033[32m%s\033[00m]" % (info, data))


def error(data, info = "ERR"):
	print("[\033[31mx\033[00m] [\033[31m%s\033[00m] %s" % (info, data))


def warn(data, info = "INFO"):
	print("[-] [\033[33m%s\033[00m] %s" % (info, data))


def fail(account, msg = "", title = "", info = "FAILED"):
	if not msg and not title:
		print("[\033[31m-\033[00m] [\033[31m%s\033[00m] %s" % (info, account))
	else:
		print("[\033[31m-\033[00m] [\033[31m%s\033[00m] [\033[34m%s\033[00m] --> [\033[37m%s\033[00m] %s" % (info, msg, title, account))


def found(user, passwd, title):
	print("[\033[37m*\033[00m] [\033[36mMATCH\033[00m] ['\033[32m%s\033[00m':'\033[32m%s\033[00m'] [\033[37m%s\033[00m]" % (user, passwd, title))
	
	
def vuln(vuln):
	print("[\033[31m*\033[00m] [\033[31m%s\033[00m]" % (vuln))
