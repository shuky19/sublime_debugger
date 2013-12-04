from abc import ABCMeta, abstractmethod

class Debugger(object):
	__metaclass__ = ABCMeta

	def __init__(self, debug_view):
		self.debug_view = debug_view

	def signal_position_changed(self, file_name, line_number):
		'''
		Raised when debugger change position
		'''
		self.debug_view.set_cursor(file_name, line_number)

	def signal_text_result(self, result, reason):
		'''
		Raised when command result is returned (Expression or Threads command for example)
		'''
		self.debug_view.add_text_result(result, reason)

	def signal_process_ended(self):
		self.debug_view.stop()

	@abstractmethod
	def run_command(self, command_type, **args):
		pass