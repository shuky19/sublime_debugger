import sublime, sublime_plugin
import threading

try:
    from .debugger import *
except:
    from debugger import *

class DebugCommand(sublime_plugin.WindowCommand):
	def __init__(self, window):
		super(DebugCommand, self).__init__(window)
		self.debugger = None
		self.debugger_model = None
		self.debug_views = None

	def run(self, command, **args):
		# Allow only known commands
		if command not in DebuggerModel.COMMANDS:
			sublime.message_dialog("Unknown command: "+command)
			return
		# Allow only start command when inactive
		if not self.debugger and command not in DebuggerModel.STARTERS_COMMANDS:
			return

		# Cursor movement commands
		if command == DebuggerModel.COMMAND_JUMP:
			current_line = ViewHelper.get_current_cursor(self.window, self.debugger_model.get_current_file())

			if current_line:
				self.clear_cursor()
				self.debugger.run_command(command, str(current_line+1))
				self.debugger.run_command(DebuggerModel.COMMAND_GET_LOCATION)
		elif command == DebuggerModel.COMMAND_GO_TO:
			file_name = self.debugger_model.get_current_file()
			current_line = ViewHelper.get_current_cursor(self.window, file_name)

			if current_line:
				self.clear_cursor()
				self.debugger.run_command(DebuggerModel.COMMAND_SET_BREAKPOINT, file_name+":"+str(current_line+1))
				self.debugger.run_command(DebuggerModel.COMMAND_CONTINUTE)
				self.register_breakpoints()
		elif command in DebuggerModel.MOVEMENT_COMMANDS:
			self.clear_cursor()
			self.debugger.run_command(command, **args)
			self.debugger.run_command(DebuggerModel.COMMAND_GET_LOCATION)
		# Input commands
		elif command == DebuggerModel.COMMAND_DEBUG_LAYOUT:
			self.show_debugger_layout()
		elif command == DebuggerModel.COMMAND_RESET_LAYOUT:
			if not self.debugger_model:
				self.debugger_model = DebuggerModel(self.debugger)

			if not self.debug_views:
				self.debug_views = dict([(key, None) for key in self.debugger_model.get_data().keys()])

			ViewHelper.reset_debug_layout(self.window, self.debug_views)
		elif command == DebuggerModel.COMMAND_SEND_INPUT:
			self.window.show_input_panel("Enter input", '', lambda input_line: self.on_input_entered(input_line), None, None)
		elif command == DebuggerModel.COMMAND_GET_EXPRESSION:
			self.window.show_input_panel("Enter expression", '', lambda exp: self.on_expression_entered(exp), None, None)
		elif command == DebuggerModel.COMMAND_ADD_WATCH:
			self.window.show_input_panel("Enter watch expression", '', lambda exp: self.on_watch_entered(exp), None, None)
		# Start command
		elif command == DebuggerModel.COMMAND_START_RAILS:
			settings = sublime.load_settings('Ruby Debugger.sublime-settings')

			if PathHelper.file_exists(settings.get("rails_executable_path"), self.window):
				self.start_command(settings.get("rails_executable_path") + " s", True)
			elif PathHelper.file_exists("script/rails", self.window):
				self.start_command("script/rails s", True)
			elif PathHelper.file_exists("bin/rails", self.window): # Rails 4 support
				self.start_command("bin/rails s", True)
			else:
				sublime.message_dialog("Cannot find file. Are you sure you're in a rails project?")
		elif command == DebuggerModel.COMMAND_START_CURRENT_FILE:
			self.start_command(self.window.active_view().file_name())
		elif command == DebuggerModel.COMMAND_START:
			self.window.show_input_panel("Enter file name", '', lambda file_name: self.start_command(file_name), None, None)
		# Register breakpoints command
		elif command == DebuggerModel.COMMAND_SET_BREAKPOINT:
			self.register_breakpoints()
		# All othe commands
		else:
			self.debugger.run_command(command)

	def start_command(self, file_name, use_bundler=False):
		is_legal, file_path, arguments = PathHelper.get_file(file_name, self.window)

		if is_legal:
			# Intialize debugger layout
			self.show_debugger_layout()
			SublimeHelper.set_timeout_async(lambda file_path=file_path,bundle=use_bundler, args=arguments: self.start_command_async(file_path, bundle, *args), 0)
		else:
			sublime.message_dialog("File: " + file_path+" does not exists")

	def start_command_async(self, file_path, use_bundler, *args):
		if self.debugger:
			self.debugger.run_command(DebuggerModel.COMMAND_STOP)

		# Initialize variables
		self.debugger = RubyDebugger(self, use_bundler)
		self.debugger_model = DebuggerModel(self.debugger)

		# Start debugging
		self.debugger.run_command(DebuggerModel.COMMAND_START, PathHelper.get_pwd(file_path), file_path, *args)

		# Register all breakpoint
		self.register_breakpoints()

	def show_debugger_layout(self):
		if not self.debugger_model:
			self.debugger_model = DebuggerModel(self.debugger)

		self.debug_views = dict([(key, None) for key in self.debugger_model.get_data().keys()])
		ViewHelper.init_debug_layout(self.window, self.debug_views)

	def register_breakpoints(self):
		self.debugger.run_command(DebuggerModel.COMMAND_CLEAR_BREAKPOINTS)
		self.window.run_command("view_helper", {"command" : "sync_breakpoints"})

		for file_name, line_number, condition in self.debugger_model.get_all_breakpoints():
			if condition:
				condition = " if "+condition
			else:
				condition = ""
			self.debugger.run_command(DebuggerModel.COMMAND_SET_BREAKPOINT, file_name+":"+str(line_number)+str(condition))

		# Refresh breakpoints window
		self.debugger.run_command(DebuggerModel.COMMAND_GET_BREAKPOINTS)

	def on_input_entered(self, input_string):
		self.debugger.run_command(DebuggerModel.COMMAND_SEND_INPUT, input_string)

	def on_expression_entered(self, expression):
		self.debugger.run_result_command(DebuggerModel.COMMAND_GET_EXPRESSION, expression, expression)
		self.window.run_command("view_helper", {"command" : "move_to_front", "debug_view" : self.debug_views[DebuggerModel.DATA_IMMEDIATE]})

	def on_watch_entered(self, expression):
		self.debugger_model.add_watch(expression)
		self.window.run_command("view_helper", {"command" : "move_to_front", "debug_view" : self.debug_views[DebuggerModel.DATA_WATCH]})

	def add_text_result(self, result, reason):
		result = self.debugger_model.update_data(reason, result)

		if result:
			new_data = result[0]
			line_to_show = result[1]
			should_append = result[2]
			self.debug_views[reason].run_command("replace_content", {"new_content" : new_data, "line_to_show" : line_to_show, "should_append" : should_append})

	def set_cursor(self, file_name, line_number):
		# Updating only if position changed
		if self.debugger_model.set_cursor(file_name, line_number):
			self.window.run_command("view_helper", {"command" : "set_cursor", "file_name" : file_name, "line_number" : line_number})

	def clear_cursor(self):
		for view in self.window.views():
			view.erase_regions("debugger")

		self.debugger_model.clear_cursor()

	def stop(self):
		self.clear_cursor()
		self.debugger = None
