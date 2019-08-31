def info(data, info = "INFO"):
	print("[+] [\033[37m%s\033[00m] %s" % (info, data))


def success(data, info = "INFO"):
	print("[*] [\033[32m%s\033[00m] [\033[32m%s\033[00m]" % (info, data))


def error(data, info = "ERR"):
	print("[x] [\033[31m%s\033[00m] %s" % (info, data))


def warn(data, info = "INFO"):
	print("[-] [\033[93m%s\033[00m] %s" % (info, data))

def fail(data, info = "FAILED"):
	print("[-] [\033[31m%s\033[00m] %s" % (info, data))
	
	
def vuln(vuln):
	print("[\033[31m*\033[00m] [\033[31m%s\033[00m]" % (vuln))
