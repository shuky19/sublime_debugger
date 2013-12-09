import sublime, sublime_plugin
from .debugger import *

class EraseAllCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.view.erase(edit, sublime.Region(0, self.view.size()))

class ToggleBreakpointCommand(sublime_plugin.TextCommand):
	def run(self, edit, mode, **args):
		if mode == "clear_all":
			for view in self.view.window().views():
				view.erase_regions("breakpoint")
				DebuggerModel.BREAKPOINTS = []
				self.view.window().run_command("debug", {"command" : "set_breakpoint"})
		elif mode == "normal":
			self.update_breakpoints()
		elif mode == "conditional":
			self.view.window().show_input_panel("Enter condition", '', lambda condition : self.update_breakpoints(condition), None, None)
		elif mode == "refresh":
			self.view.erase_regions("breakpoint")
			self.update_regions(self.view.file_name(), [], "")

	def update_breakpoints(self, condition=None):
		self.view.erase_regions("breakpoint")
		selected_lines = ViewHelper.get_lines(self.view, self.view.sel())
		self.update_regions(self.view.file_name(), selected_lines, condition)
		self.view.window().run_command("debug", {"command" : "set_breakpoint"})

	def update_regions(self, selected_file, selcted_line_numbers, condition):
		current_breakpoints = DebuggerModel.BREAKPOINTS

		unchanged = []
		unchanged_in_selected_file = []
		added = []

		for breakpoint in current_breakpoints:
			was_found = False
			for line_number in selcted_line_numbers:
				if breakpoint.line_number-1 == line_number:
					was_found = True
					break

			if not was_found and breakpoint.file_name == selected_file:
				unchanged_in_selected_file += [breakpoint]

			if not was_found :
				unchanged += [breakpoint]

		for line_number in selcted_line_numbers:
			was_found = False
			for breakpoint in current_breakpoints:
				if breakpoint.line_number-1 == line_number:
					was_found = True
					break

			if not was_found:
				added += [self.create_breakpoint(line_number, condition)]

		self.view.add_regions("breakpoint", self.to_regions(added+unchanged_in_selected_file), "string", "circle", sublime.PERSISTENT)
		DebuggerModel.BREAKPOINTS = added+unchanged

	def create_breakpoint(self, line_number, condition):
		return Breakpoint(self.view.file_name(), line_number+1, condition)

	def create_region(self, breakpoint):
		point = self.view.text_point(breakpoint.line_number-1, 0)
		region = sublime.Region(point, point)
		return region

	def to_regions(self, breakpoints):
		return [self.create_region(breakpoint) for breakpoint in breakpoints]

