import os.path
import sublime
import time
import traceback
import socket
import subprocess

from threading import Thread
try:
	import queue
	from queue import Queue
	from queue import Empty
	from io import StringIO
except:
    from Queue import Queue
    from Queue import Empty
    from StringIO import StringIO

from ..interfaces import *
from ..helpers import *

class RubyDebuggerConnector(DebuggerConnector):
	"""Connector used to communication with debugged process"""
	def __init__(self, debugger, use_bundler):
		super(RubyDebuggerConnector, self).__init__(debugger)
		self.debugger = debugger
		self.process = None
		self.client = None
		self.control_client = None
		self.connected = False
		self.ruby_version = None
		self.ruby_protocol_type = None
		self.use_bundler = use_bundler
		self.errors_reader = None
		self.outputer = None
		self.reader = None

	def start(self, current_directory, file_name, *args):
		'''
		Start and attach the process
		'''
		# Vaildate ruby versions and gem version
		if not self.validation_environment():
			return

		# Start the debuggee process
		self.start_process(current_directory, file_name, args)

		# Start read from socket, output, errors
		self.errors_reader = self.start_tread(lambda stream = self.process.stderr: self.output_thread(stream))
		self.outputer = self.start_tread(lambda stream = self.process.stdout: self.output_thread(stream))

		# Try to connect to process with sockets
		if not self.connect_debugger():
			return

		self.reader = self.start_tread(self.reader_thread)

	def validation_environment(self):
		settings = sublime.load_settings('Ruby Debugger.sublime-settings')

		try:
			if os.name == "posix":
				# Fixing permissions
				subprocess.Popen("bash -c \"chmod +x '" + PathHelper.get_ruby_executor() + "'\"", stdin = subprocess.PIPE, stderr = subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1, shell=True).communicate()[0]

				# On Unix using rvm and bash
				ruby_binaries = "'"+settings.get("ruby_binaries")+"'"

				# On Unix using exec and shell to get environemnt variables of ruby version
				process_command = "'"+PathHelper.get_ruby_executor()+"' " + ruby_binaries + " False '" + PathHelper.get_ruby_version_discoverer() + "'"
				process_params = ["bash", "-c", "\""+process_command+"\""]
				self.ruby_version = subprocess.Popen(" ".join(process_params), stdin = subprocess.PIPE, stderr = subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1, shell=True).communicate()[0]
			else:
				# On Windows not using shell, so the proces is not visible to the user
				startupinfo = subprocess.STARTUPINFO()
				startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
				process_params = ["ruby", PathHelper.get_ruby_version_discoverer()]
				self.ruby_version = subprocess.Popen(process_params, stdout=subprocess.PIPE, startupinfo=startupinfo).communicate()[0]
		except Exception as ex:
			self.log_message("Could not start process: "+str(ex)+'\n')
			return False

		self.ruby_version = self.ruby_version.decode("UTF-8").replace("\n", "").replace("\r", "")

		if self.ruby_version not in settings.get('supported_ruby_versions'):
			self.log_message("Ruby version: "+self.ruby_version+" is not supported.")
			return False

		if self.ruby_version == "1.9.3":
			self.ruby_protocol_type = "debugger"
		else:
			self.ruby_protocol_type = "byebug"

		return True

	def start_process(self, current_directory, file_name, args):
		settings = sublime.load_settings('Ruby Debugger.sublime-settings')
		requires = " '-r"+PathHelper.get_sublime_require()+"'"
		directory = " '-C"+current_directory+"'"
		program = " '"+file_name+"' "+" ".join(args)

		# Case of running rails
		if self.use_bundler or settings.get('should_use_bundle'):
				requires = requires + " '-rbundler/setup'"
				directory = " '-C"+sublime.active_window().folders()[0]+"'"

		# Initialize params acourding to OS type
		if os.name == "posix":
			ruby_binaries = "'"+settings.get("ruby_binaries")+"'"
			debug_logs_enabled = str(settings.get("debug_logs"))
			ruby_arguments = directory + requires + " " + settings.get("ruby_arguments")+ " " +program

			# On Unix using exec and shell to get environemnt variables of ruby version
			process_command = "'"+PathHelper.get_ruby_executor()+"' " + ruby_binaries + " " + debug_logs_enabled + " " + ruby_arguments
			process_params = ["bash", "-c", "\""+process_command+"\""]
			self.process = subprocess.Popen(" ".join(process_params), stdin = subprocess.PIPE, stderr = subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1, shell=True, cwd=sublime.active_window().folders()[0])

			if self.is_debug():
					self.log_message("Started process command: " + " ".join(process_params) )
		else:
			# On Windows not using shell, so the proces is not visible to the user
			startupinfo = subprocess.STARTUPINFO()
			startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
			process_params = ["ruby", "-C"+current_directory, "-r"+PathHelper.get_sublime_require(), file_name]
			process_params += args
			self.process = subprocess.Popen(process_params, stdin = subprocess.PIPE, stderr = subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1, startupinfo=startupinfo)

			if self.is_debug():
				self.log_message("Started process command: " + " ".join(process_params) )

	def connect_debugger(self):
		self.data = StringIO()
		self.requests = Queue()
		self.requests.put({"signal":False, "reason":"get_location"})

		self.connected = False
		self.log_message("Connecting... ")
		for i in range(1,9):
			try:
				self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.client.connect(("localhost", 8989))
				self.control_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				self.control_client.connect(("localhost", 8990))
				self.connected = True
				self.log_message("Connected"+'\n')
				break
			except Exception as ex:
				if i == 9:
					self.log_message("Connection could not be made: "+str(ex)+'\n')
					return False
				else:
					time.sleep(1)

		return True

	def start_tread(self, threads_method):
		thread  = Thread(target=threads_method)
		thread.daemon = True
		thread.start()
		return thread

	def output_thread(self, stream):
		# Always read stream`
		try:
			while True:
				bytes = stream.readline()

				if len(bytes) == 0:
					break

				result = bytes.decode("UTF-8")
				self.log_message(result)
		except Exception:
			pass

	def reader_thread(self):
		# Alwast read stream
		try:
			while True:
				bytes = self.client.recv(4096)

				if len(bytes) == 0:
					break

				result = bytes.decode("UTF-8")
				self.data.write(result)
				self.data.flush()

				if self.has_end_stream():
					self.handle_response()

		except Exception as ex:
			if self.connected:
				self.log_message("Debugger exception: "+str(ex)+'\n'+" StackTrace: "+traceback.format_exc())
				self.connected = False

		self.outputer.join()
		self.errors_reader.join()

		# Signal that the process has exited
		self.log_message("Debugger stopped")
		self.debugger.signal_process_ended()

	def handle_response(self):
		results = self.split_by_results()
		next_result = results.pop()

		for result in results:
			if result:
				pass

			file_name, line_number = self.get_current_position()

			# Check wheather position was updated
			if file_name != "" and not PathHelper.is_same_path(PathHelper.get_sublime_require(), file_name) and not "kernel_require.rb" in file_name:
				self.debugger.signal_position_changed(file_name, line_number)
				# self.log_message("New position: "+file_name+":"+str(line_number))

			try:
				request = self.requests.get_nowait()
				# self.log_message("Pop request: "+str(request)+", current queue size: "+str(self.requests.qsize())+", request result:"+result)

				# Check if should return the result
				if request["signal"]:
					prefix = request.get("prefix")
					data = result.strip()

					if prefix:
						data = (prefix, data)

					# Return result
					self.debugger.signal_text_result(data, request["reason"])
				else:
					pass

				if PathHelper.is_same_path(PathHelper.get_sublime_require(), file_name) or "kernel_require.rb" in file_name:
					self.debugger.run_command(DebuggerModel.COMMAND_STEP_OVER)
			except Empty:
				pass

		self.data = StringIO()
		self.data.write(next_result)

	def send_data(self, command, reason):
		self.requests.put({"signal": False, "reason": reason, "command": command})
		self.send_data_internal(command)

	def send_without_outcome(self, command):
		self.send_data_internal(command)

	def send_input(self, command):
		self.process.stdin.write(bytearray(command+'\n', "UTF-8"))
		self.process.stdin.flush()

	def send_control_command(self, command):
		if not self.connected:
			pass

		try:
			self.control_client.sendall(bytearray(command+'\n', "UTF-8"))
		except Exception as e:
			if self.connected:
				self.log_message("Failed communicate with process ("+command+"): "+str(e))

	def send_data_internal(self, command):
		if not self.connected:
			return

		try:
			self.client.sendall(bytearray(command+'\n', "UTF-8"))
		except Exception as e:
			if self.connected:
				self.log_message("Failed communicate with process ("+command+"): "+str(e))

	def send_for_result(self, command, reason):
		self.requests.put({"signal": True, "reason": reason, "command": command})
		self.send_data_internal(command)

	def send_with_result(self, command, reason, prefix):
		self.requests.put({"signal": True, "prefix": prefix, "reason": reason, "command": command})
		self.send_data_internal(command)

	def split_by_results(self):
		result = [""]
		for line in self.get_lines():
			if self.debugger.match_ending(self.ruby_protocol_type, line):
				result.insert(len(result), "")
			else:
				result[len(result)-1] += line + '\n'

		return result

	def has_end_stream(self):
		end_of_stream = False
		for line in self.get_lines():
			if self.debugger.match_ending(self.ruby_protocol_type, line):
				end_of_stream = True;

		return end_of_stream

	def get_current_position(self):
		current_line = -1
		current_file = ""
		end_of_stream = False

		for line in self.get_lines():
			match = self.debugger.match_line_cursor(self.ruby_protocol_type, line)

			if match:
				current_line = match.groups()[0]

			match = self.debugger.match_file_cursor(self.ruby_protocol_type, line)
			if match:
				current_file = match.groups()[0]

		return current_file, int(current_line)

	def get_lines(self):
		return self.data.getvalue().split('\n')

	def stop(self):
		self.log_message("Stopping...")
		self.send_control_command("kill")
		if self.process:
			self.process.kill()

		self.connected = False
		self.process = None

	def is_debug(self):
		settings = sublime.load_settings('Ruby Debugger.sublime-settings')
		return settings.get('debug_logs')