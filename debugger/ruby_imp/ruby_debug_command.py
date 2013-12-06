from ..interfaces import *

class RubyDebugCommand(DebugCommand):
	"""Represent a command for debugger"""
	def __init__(self, command_strings, reason, is_signal_result = False, is_returning_data = True):
		super(RubyDebugCommand, self).__init__()
		self.commands = command_strings
		self.reason = reason
		self.is_signal_result = is_signal_result
		self.is_returning_data = is_returning_data

	def execute(self, debugger_constroller, *args):
		if args:
			pass
		if self.is_signal_result:
			if isinstance(self.commands, list):
				self.execute_list(debugger_constroller, self.commands.copy(), self.reason, lambda command,reason: debugger_constroller.send_for_result(command, reason))
			else:
				debugger_constroller.send_for_result(self.command_with_args(self.commands, *args), self.reason)
		elif self.is_returning_data:
			if isinstance(self.commands, list):
				self.execute_list(debugger_constroller, self.commands.copy(), self.reason, lambda command,reason: debugger_constroller.send_data(command, reason))
			else:
				debugger_constroller.send_data(self.command_with_args(self.commands, *args), self.reason)
		else:
			debugger_constroller.send_without_outcome(self.command_with_args(self.commands, *args))

	def command_with_args(self, command, *args):
		if args:
			for arg in args:
				command += " "+arg

		return command

	def execute_list(self, debugger_constroller, commands, reason, func):
		first_command = commands[0]
		commands.remove(first_command)
		func(first_command, reason)

		for command in commands:
			debugger_constroller.send_without_outcome(command)
