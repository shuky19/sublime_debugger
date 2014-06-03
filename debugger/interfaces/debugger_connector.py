from abc import ABCMeta, abstractmethod

try:
	from .debugger_model import DebuggerModel
except:
	from debugger_model import DebuggerModel

class DebuggerConnector(object):
	"""Connector used to communication with debugged process"""
	__metaclass__ = ABCMeta

	def __init__(self, debugger):
		super(DebuggerConnector, self).__init__()
		self.debugger = debugger

	def log_message(self, message):
		self.debugger.signal_text_result(message, DebuggerModel.DATA_OUTPUT)

	@abstractmethod
	def start(self, current_directory, file_name, *args):
		'''
		Start and attach the process
		'''
		pass

	@abstractmethod
	def send_data(self, command, reason):
		'''
		Send command to the debugger (reason parameters is just for logging)
		'''

	@abstractmethod
	def send_without_outcome(self, command):
		'''
		Send command to the debugger when no result is returned
		'''

	@abstractmethod
	def send_input(self, command):
		'''
		Send text to the process's STDIN
		'''

	@abstractmethod
	def send_for_result(self, command, reason):
		'''
		Send command to the debugger and when result returned
		signal result with the given reason
		'''

	@abstractmethod
	def send_with_result(self, command, reason, prefix):
		'''
		Send command to the debugger and when result returned
		signal result with the given reason and prefix
		'''

	@abstractmethod
	def stop(self):
		'''
		Stop the debugger process
		'''
