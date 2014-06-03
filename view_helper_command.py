import sublime, sublime_plugin
try:
    from .debugger import *
except:
    from debugger import *

class ViewHelperCommand(sublime_plugin.WindowCommand):
	def __init__(self, window):
		super(ViewHelperCommand, self).__init__(window)

	def run(self, command, **args):
		if command == "set_cursor":
			sublime.set_timeout(lambda window=self.window, args=args: ViewHelper.set_cursor(window, **args), 0)
		elif command == "get_current_cursor":
			sublime.set_timeout(lambda window=self.window, args=args: ViewHelper.get_current_cursor(window, **args), 0)
		elif command == "show_debug_windows":
			sublime.set_timeout(lambda window=self.window, args=args: ViewHelper.init_debug_layout(window, **args), 0)
		elif command == "hide_debug_windows":
			sublime.set_timeout(lambda window=self.window, args=args: ViewHelper.hide_debug_windows(window, **args), 0)
		elif command == "move_to_front":
			sublime.set_timeout(lambda window=self.window, args=args: ViewHelper.move_to_front(window, **args), 0)
		elif command == "sync_breakpoints":
			sublime.set_timeout(lambda window=self.window, args=args: ViewHelper.sync_breakpoints(window, **args), 0)