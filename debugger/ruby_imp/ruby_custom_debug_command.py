from ..interfaces import *

class RubyCustomDebugCommand(DebugCommand):
	"""Represent send start debug command"""
	def __init__(self, lambda_command):
		super(RubyCustomDebugCommand, self).__init__()
		self.lambda_command = lambda_command

	def execute(self, debugger_constroller, *args):
		self.lambda_command(debugger_constroller, *args)
