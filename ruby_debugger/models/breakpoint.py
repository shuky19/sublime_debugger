class Breakpoint(object):
	"""Represent a breakpoint"""
	def __init__(self, file_name, line_number, condition):
		super(Breakpoint, self).__init__()
		self.file_name = file_name
		self.line_number = line_number
		self.condition = condition
		