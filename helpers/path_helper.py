from os import path

class PathHelper(object):
	def get_file(file_name, window):
		if not path.isabs(file_name):
			file_name = path.join(window.folders()[0], file_name)

		return file_name, path.isfile(file_name)

	def get_pwd(file_name):
		return path.split(file_name)[0]

	def is_same_path(first, second):
		return path.abspath(first) == path.abspath(second)