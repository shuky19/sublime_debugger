import sublime
import re
from ..interfaces import *
from .ruby_debugger_connector import RubyDebuggerConnector
from .ruby_debug_command import RubyDebugCommand
from .ruby_custom_debug_command import RubyCustomDebugCommand

class RubyDebugger(Debugger):
	PROTOCOL = {"1.9.3": {"end_regex":r"PROMPT \(rdb:\d+\) ",
							 "line_regex":r"^=>\s+?(\d+)  .*$",
							 "file_regex":r"\[-*\d+, \d+\] in (.*)$"},
					"2.0.0": {"end_regex":r"PROMPT \(byebug\) ",
							  "line_regex":r"^=>\s+?(\d+): .*$",
							  "file_regex":r"\[-*\d+, \d+\] in (.*)$"}}

	# Define protocol
	COMMANDS = { DebuggerModel.COMMAND_GET_LOCATION:RubyDebugCommand("l=", "GetLocation"),
				 DebuggerModel.COMMAND_GET_STACKTRACE:RubyDebugCommand("where", DebuggerModel.DATA_STACK, True),
				 DebuggerModel.COMMAND_GET_LOCALS:RubyDebugCommand("info local", DebuggerModel.DATA_LOCALS, True),
				 DebuggerModel.COMMAND_GET_THREADS:RubyDebugCommand("thread l", DebuggerModel.DATA_THREADS, True),
				 DebuggerModel.COMMAND_GET_EXPRESSION:RubyDebugCommand("eval", DebuggerModel.DATA_IMMEDIATE, True),
				 DebuggerModel.COMMAND_GET_BREAKPOINTS:RubyDebugCommand("info break", DebuggerModel.DATA_BREAKPOINTS, True),

				 DebuggerModel.COMMAND_SEND_INPUT:RubyCustomDebugCommand(lambda debugger_constroller, *args: debugger_constroller.send_input(*args)),
				 DebuggerModel.COMMAND_START:RubyCustomDebugCommand(lambda debugger_constroller, *args: debugger_constroller.start(*args)),
				 DebuggerModel.COMMAND_STOP:RubyCustomDebugCommand(lambda debugger_constroller, *args: debugger_constroller.stop()),

				 DebuggerModel.COMMAND_GET_WATCH:RubyCustomDebugCommand(lambda debugger_constroller, prefix, expression: debugger_constroller.send_with_result("eval " + expression, DebuggerModel.DATA_WATCH, prefix)),
				 DebuggerModel.COMMAND_GET_EXPRESSION:RubyCustomDebugCommand(lambda debugger_constroller, prefix, expression: debugger_constroller.send_with_result("eval " + expression, DebuggerModel.DATA_IMMEDIATE, prefix)),

				 DebuggerModel.COMMAND_SET_BREAKPOINT:RubyCustomDebugCommand(lambda debugger_constroller, location: debugger_constroller.send_control_command("b " + location)),
				 DebuggerModel.COMMAND_CLEAR_BREAKPOINTS:RubyCustomDebugCommand(lambda debugger_constroller: debugger_constroller.send_control_command("delete")),
				 DebuggerModel.COMMAND_INTERRUPT:RubyCustomDebugCommand(lambda debugger_constroller: debugger_constroller.send_control_command("interrupt")),

				 DebuggerModel.COMMAND_STEP_OVER:RubyDebugCommand("n", "step_over"),
				 DebuggerModel.COMMAND_STEP_INTO:RubyDebugCommand("s", "step_into"),
				 DebuggerModel.COMMAND_STEP_UP:RubyDebugCommand("up", "step_up"),
				 DebuggerModel.COMMAND_STEP_DOWN:RubyDebugCommand("down", "step_down"),
				 DebuggerModel.COMMAND_CONTINUTE:RubyDebugCommand("c", "continue"),
				 DebuggerModel.COMMAND_JUMP:RubyDebugCommand("jump", "jump") }

	def __init__(self, debugger_view, use_bundler):
		super(RubyDebugger, self).__init__(debugger_view)
		self.connector = RubyDebuggerConnector(self, use_bundler)

	def run_command(self, command_type, *args):
		RubyDebugger.COMMANDS[command_type].execute(self.connector, *args)

	def run_result_command(self, command_type, prefix, *args):
		RubyDebugger.COMMANDS[command_type].execute(self.connector, prefix, *args)

	def match_ending(self, ruby_version, line):
		return re.match(RubyDebugger.PROTOCOL[ruby_version]["end_regex"], line)

	def match_line_cursor(self, ruby_version, line):
		return re.match(RubyDebugger.PROTOCOL[ruby_version]["line_regex"], line)

	def match_file_cursor(self, ruby_version, line):
		return re.match(RubyDebugger.PROTOCOL[ruby_version]["file_regex"], line)
