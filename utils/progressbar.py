import sys


def prints(text):
	"""
	Print text to screen and then delete it (replace by spaces)
	:param text: string = text to screen
	:return: True (dummy)
	"""
	sys.stdout.write("%s\r" % (" " * len(text)))
	sys.stdout.flush()
	sys.stdout.write("%s\r" % (text))


def progress_bar(trying, completed, total, bar_size=60):
	"""
	Print current status of task. It will be [+++####---]
		+ is completed threads
		# is running threads
		- is threads will run
	:param trying: int = current running threads
	:param completed: int = threads executed
	:param total: int = total number of threads
	:param bar_size: int = maximum length size of progress bar
	:return: True (dummy)
	"""
	finished = int((completed * bar_size) / total)
	running = int((trying * bar_size) / total - finished)
	running = 1 if running < 1 else running

	prints("|%s%s%s| %10s" % (finished * "+", running * "#", (bar_size - finished - running) * '-', completed))
