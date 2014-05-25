import sublime
from threading import Thread

class SublimeHelper(object):
	@staticmethod
	def set_timeout_async(command, delay):
		try:
			sublime.set_timeout_async(command, delay)
		except Exception, e:
			thread  = Thread(target=command)
			thread.daemon = True
			# # thread  = Thread(target=lambda command=command, delay=delay: sublime.set_timeout(command, delay))
			thread.start()