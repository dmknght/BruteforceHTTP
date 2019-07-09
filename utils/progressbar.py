import sys

def prints(mtext):
	#############################################
	#	print message and replace it after
	#	Use for status bar, brute forcing process
	#	https://stackoverflow.com/a/5291044
	#
	#	Update code by this (Works better)
	#	https://stackoverflow.com/a/41511658
	#############################################

	#######
	#	Newer version:
	#	https://stackoverflow.com/a/3173338
	#######

	
	sys.stdout.write("%s\r" %(mtext))
	sys.stdout.flush()
	sys.stdout.write("%s\r" %(" " * len(mtext)))

def progress_bar(trying, completed, total, bsize = 60):
	"""
		MULTIPLE LINES PROGRESS BAR IS NOT WORKING FOR WINDOWS AND ANDROID TERM
		Create a progress bar to show current process
		Progessbar format [+++#####-----]
			+ is completed tasks. Tasks should recived responses
			# is submited tasks. Tasks have no responses
			- is waiting tasks
	"""
	finished = int((completed * bsize) / total)
	running = int((trying * bsize) / total - finished)
	running = 1 if running < 1 else running

	prints("|%s%s%s| %10s" %(
		finished * "+",
		running * "#",
		(bsize - finished - running) * '-',
		completed
	))