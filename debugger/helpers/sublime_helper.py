import sublime
from threading import Thread

class SublimeHelper(object):
	@staticmethod
	def set_timeout_async(command, delay):
		try:
			sublime.set_timeout_async(command, delay)
		except Exception:
			thread  = Thread(target=command)
			thread.daemon = True
			thread.start()