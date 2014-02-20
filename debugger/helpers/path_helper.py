import sublime
import os
from os import path

class PathHelper(object):
	def file_exists(file_name, window):
		is_legal = False
		
		if path.isfile(file_name):
			is_legal = True
		elif path.isfile(path.join(window.folders()[0], file_name)):
			file_name = path.join(window.folders()[0], file_name)
			is_legal = True

		return is_legal

	def get_file(command, window):
		is_legal = False
		file_name = ""
		parts = command.split(" ")
		arguments = []

		for part in parts:
			if is_legal:
				arguments.append(part)
				continue

			elif file_name == "":
				file_name = part
			else:
				file_name = " ".join([file_name,part])

			# I tried to DRY here by just using the function file_exists but that somehow broke everything.
			if path.isfile(file_name):
				is_legal = True
			elif path.isfile(path.join(window.folders()[0], file_name)):
				file_name = path.join(window.folders()[0], file_name)
				is_legal = True

		return is_legal, file_name, arguments

	def get_pwd(file_name):
		return path.split(file_name)[0]

	def is_same_path(first, second):
		return path.abspath(first) == path.abspath(second)

	def get_sublime_require():
		return os.path.join(sublime.packages_path(), "Ruby Debugger", "sublime_debug_require.rb")

	def get_ruby_version_discoverer():
		return os.path.join(sublime.packages_path(), "Ruby Debugger", "ruby_version_discoverer.rb")
