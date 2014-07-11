import sublime
import threading
from .sublime_helper import SublimeHelper
from ..interfaces.debugger_model import DebuggerModel
from .path_helper import PathHelper

class ViewHelper(object):
	@staticmethod
	def region_in_line(region, line):
		return line.begin() <= region.begin() and line.end() >= region.end()

	@staticmethod
	def get_lines(view, regions):
		file_lines = view.lines(sublime.Region(0, view.size()))
		lines = []
		for line in file_lines:
			line_number = file_lines.index(line)
			lines += [line_number for region in regions if ViewHelper.region_in_line(region, line)]

		return lines

	@staticmethod
	def init_debug_layout(window, debug_views):
		window.set_layout({"cols" : [0,0.5,1], "rows":[0,0.7,1], "cells":[[0,0,2,1],[0,1,1,2],[1,1,2,2]]})

		for view in window.views():
			if view.name() in debug_views.keys():
				debug_views[view.name()] = view
				view.set_read_only(False)
				view.run_command("erase_all")
				view.set_read_only(True)
			elif window.get_view_index(view)[0] != 0:
				window.set_view_index(view, 0, len(window.views_in_group(0)))

		groups = [0,0]
		current_group = 0
		for view_name in debug_views.keys():
			view = debug_views[view_name]
			
			if view == None:
				v = window.new_file()
				v.set_scratch(True)
				v.set_read_only(True)
				v.set_name(view_name)
				v.settings().set('word_wrap', False)
				debug_views[view_name] = v

			view_group, view_index = window.get_view_index(debug_views[view_name])

			if view_group != (current_group+1) or view_index != groups[current_group]:
				window.set_view_index(debug_views[view_name], current_group + 1, groups[current_group])
			
			groups[current_group] += 1
			current_group = (current_group + 1) % 2

		window.focus_group(0)

	@staticmethod
	def reset_debug_layout(window, debug_views):
		for view in window.views():
			if view.name() in debug_views.keys():
				window.focus_view(view)
				window.run_command("close_file")

		window.set_layout({"cols" : [0,1], "rows":[0,1], "cells":[[0,0,1,1]]})

	@staticmethod
	def set_cursor(window, file_name, line_number):
		view = window.open_file(file_name)
		if view.is_loading():
			sublime.set_timeout(lambda window=window, file_name=file_name, line_number=line_number: ViewHelper.set_cursor(window, file_name, line_number), 50)
			return


		view.add_regions("debugger", [view.lines(sublime.Region(0, view.size()))[line_number-1]], "lineHighlight", "")
		view.show(view.text_point(line_number-1,0))

		view_group, view_index = window.get_view_index(view)

		if view_group != 0:
			window.set_view_index(view, 0, len(window.views_in_group(0)))

	@staticmethod
	def set_cursor_inner(window, file_name, line_number):
		view.add_regions("debugger", [view.lines(sublime.Region(0, view.size()))[line_number-1]], "lineHighlight", "")
		view.show(view.text_point(line_number-1,0))
		
		view_group, view_index = window.get_view_index(view)

		if view_group != 0:
			window.set_view_index(view, 0, len(window.views_in_group(0)))

	@staticmethod
	def replace_content(view, new_content, line_to_show, should_append):
		view.set_read_only(False)
		if not should_append:
			view.run_command('erase_all')

		view.run_command("move_to", {"to": "eof"})
		view.run_command("move_to", {"to": "bol"})
		view.run_command('insert', {'characters': new_content})
		view.set_read_only(True)
		if not line_to_show:
			line_to_show = len(view.lines(sublime.Region(0, view.size())))

		if view.name() not in DebuggerModel.REFRESHABLE_DATA:
			ViewHelper.move_to_front(sublime.active_window(), view)

		view.show(view.text_point(line_to_show-1, 0))

	@staticmethod
	def get_current_cursor(window, file_name):
		for view in window.views():
			if PathHelper.is_same_path(view.file_name(), file_name):
				return ViewHelper.get_lines(view, view.sel())[0]

		return None

	@staticmethod
	def move_to_front(window, debug_view):
		current_active = window.active_view()
		active_group = window.views_in_group(window.active_group())

		for group in range(0, window.num_groups()):
			if window.get_view_index(debug_view)[0] == group:
				if window.get_view_index(debug_view) != window.get_view_index(window.active_view_in_group(group)):
					window.focus_view(debug_view)
					if debug_view not in active_group:
						window.focus_view(current_active)

	@staticmethod
	def sync_breakpoints(window):
		for view in window.views():
			view.run_command("toggle_breakpoint", {"mode":"refresh"})