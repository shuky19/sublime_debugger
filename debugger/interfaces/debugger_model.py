class DebuggerModel(object):
	"""Represent data model for debugger"""

	# Debugging data types
	DATA_WATCH = "Watch"
	DATA_IMMEDIATE = "Immediate"
	DATA_OUTPUT = "Output"
	DATA_BREAKPOINTS = "Breakpoints"
	DATA_LOCALS = "Locals"
	DATA_THREADS = "Threads"
	DATA_STACK = "Stack"

	COMMAND_DEBUG_LAYOUT = "show_debug_windows"
	COMMAND_RESET_LAYOUT = "hide_debug_windows"

	# Debugging controlling
	COMMAND_START = "start_debug"
	COMMAND_START_CURRENT_FILE = "start_debug_current_file"
	COMMAND_START_RAILS = "start_rails"
	COMMAND_STOP = "stop_debug"
	COMMAND_INTERRUPT = "interrupt"

	# Debuggin cursor movement
	COMMAND_STEP_OVER = "step_over"
	COMMAND_STEP_INTO = "step_into"
	COMMAND_STEP_UP = "step_up"
	COMMAND_STEP_DOWN = "step_down"
	COMMAND_GO_TO = "go_to"
	COMMAND_CONTINUTE = "continute"
	COMMAND_JUMP = "jump"

	# Debugging information
	COMMAND_GET_LOCATION = "get_location"
	COMMAND_GET_STACKTRACE = "get_stacktrace"
	COMMAND_GET_LOCALS = "get_locals"
	COMMAND_GET_THREADS = "get_threads"
	COMMAND_GET_EXPRESSION = "get_expression"
	COMMAND_GET_BREAKPOINTS = "get_breakpoints"

	COMMAND_SEND_INPUT = "send_input"
	COMMAND_SET_BREAKPOINT = "set_breakpoint"
	COMMAND_CLEAR_BREAKPOINTS = "clear_breakpoints"

	COMMAND_ADD_WATCH = "add_watch"
	COMMAND_GET_WATCH = "get_watch"

	REFRESHABLE_DATA = [DATA_WATCH, DATA_THREADS, DATA_STACK, DATA_LOCALS, DATA_BREAKPOINTS]

	REFRESHABLE_COMMANDS = [COMMAND_GET_THREADS, COMMAND_GET_STACKTRACE, COMMAND_GET_LOCALS, COMMAND_GET_BREAKPOINTS]

	APPENDABLE_DATA = [DATA_IMMEDIATE, DATA_OUTPUT]

	STARTERS_COMMANDS = [COMMAND_DEBUG_LAYOUT, COMMAND_RESET_LAYOUT, COMMAND_START_RAILS, COMMAND_START, COMMAND_START_CURRENT_FILE]
	COMMANDS = [COMMAND_DEBUG_LAYOUT, COMMAND_RESET_LAYOUT, COMMAND_START_RAILS, COMMAND_INTERRUPT, COMMAND_START_CURRENT_FILE, COMMAND_GO_TO, COMMAND_ADD_WATCH, COMMAND_GET_WATCH, COMMAND_START, COMMAND_STOP, COMMAND_SEND_INPUT, COMMAND_STEP_OVER, COMMAND_STEP_INTO, COMMAND_STEP_UP, COMMAND_STEP_DOWN, COMMAND_CONTINUTE, COMMAND_JUMP, COMMAND_GET_LOCATION, COMMAND_GET_STACKTRACE, COMMAND_GET_LOCALS, COMMAND_GET_THREADS, COMMAND_GET_EXPRESSION, COMMAND_GET_BREAKPOINTS, COMMAND_SET_BREAKPOINT, COMMAND_CLEAR_BREAKPOINTS]
	MOVEMENT_COMMANDS = [COMMAND_CONTINUTE, COMMAND_STEP_OVER, COMMAND_STEP_INTO, COMMAND_STEP_UP, COMMAND_STEP_DOWN, COMMAND_JUMP]
	BREAKPOINTS = []

	def __init__(self, debugger):
		super(DebuggerModel, self).__init__()
		self.debugger = debugger
		self.data = {}
		self.data[DebuggerModel.DATA_WATCH] = []
		self.data[DebuggerModel.DATA_IMMEDIATE] = ""
		self.data[DebuggerModel.DATA_OUTPUT] = ""
		self.data[DebuggerModel.DATA_BREAKPOINTS] = ""
		self.data[DebuggerModel.DATA_LOCALS] = ""
		self.data[DebuggerModel.DATA_THREADS] = ""
		self.data[DebuggerModel.DATA_STACK] = ""
		self.file_name = None
		self.line_number = None

	def get_data(self):
		return self.data

	def set_cursor(self, file_name, line_number):
		if self.file_name == file_name and self.line_number == line_number:
			return False

		self.file_name = file_name
		self.line_number = line_number

		self.referesh_data()

		return True

	def clear_cursor(self):
		self.file_name = None
		self.line_number = None

	def update_data(self, data_type, new_value):
		line_to_show = None
		should_append = False

		if data_type not in self.data.keys():
			return False

		if new_value == self.data[data_type]:
			return False

		if data_type == DebuggerModel.DATA_WATCH:
			self.update_watch_expression(new_value[0], new_value[1])
			return self.watch_to_str(), line_to_show, should_append
		elif data_type == DebuggerModel.DATA_IMMEDIATE:
			self.data[data_type] += new_value[0]+" => "+ new_value[1] + '\n'
			self.referesh_data()
		elif data_type in DebuggerModel.APPENDABLE_DATA:
			should_append = True
			if not new_value.endswith('\n'):
				new_value = new_value + '\n'
			new_value = new_value.replace("\r", "")
			self.data[data_type] += new_value
			return new_value, line_to_show, should_append
		else:
			self.data[data_type] = new_value

		if data_type == DebuggerModel.DATA_STACK:
			for idx, line in enumerate(self.data[data_type].splitlines()):
				if line.startswith("-->"):
					line_to_show = idx

		return self.data[data_type], line_to_show, should_append

	def referesh_data(self):
		# Refresh autoreferesh data
		for command in DebuggerModel.REFRESHABLE_COMMANDS:
			self.debugger.run_command(command)

		# Refresh watch
		for watch_exp in self.data[DebuggerModel.DATA_WATCH]:
			self.debugger.run_result_command(DebuggerModel.COMMAND_GET_WATCH, watch_exp[0], watch_exp[0])

	def update_watch_expression(self, watch_exp, watch_value):
		for watch in self.data[DebuggerModel.DATA_WATCH]:
			if watch_exp == watch[0]:
				watch[1] = watch_value

	def add_watch(self, watch_expression):
		self.data[DebuggerModel.DATA_WATCH].append([watch_expression, ""])
		self.debugger.run_result_command(DebuggerModel.COMMAND_GET_WATCH, watch_expression, watch_expression)

	def watch_to_str(self):
		result = []
		for exp, value in self.data[DebuggerModel.DATA_WATCH]:
			result.append(exp + " = " + value)

		return '\n'.join(result)

	def get_current_file(self):
		return self.file_name

	def get_all_breakpoints(self):
		breakpoints = []
		for breakpoint in DebuggerModel.BREAKPOINTS:
			breakpoints.append((breakpoint.file_name, breakpoint.line_number, breakpoint.condition))

		return breakpoints
