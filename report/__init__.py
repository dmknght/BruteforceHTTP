from core import actions

def makeReport(data, path):
	actions.fwrite(path, data)