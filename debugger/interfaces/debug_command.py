from abc import ABCMeta, abstractmethod

class DebugCommand(object):
	__metaclass__ = ABCMeta

	"""Represent command that use while debugging"""
	def __init__(self):
		super(DebugCommand, self).__init__()

	@abstractmethod
	def execute(self, debugger_controller, *args):
		pass
		