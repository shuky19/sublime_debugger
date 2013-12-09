import os.path
import sublime
import time
import traceback
import socket
import subprocess
from io import StringIO
from threading import Thread
import queue
from queue import Queue
from ..interfaces import *
from ..helpers import *

class RubyDebuggerConnector(DebuggerConnector):
	"""Connector used to communication with debugged process"""
	def __init__(self, debugger):
		super(RubyDebuggerConnector, self).__init__(debugger)
		self.debugger = debugger
		self.process = None
		self.client = None
		self.control_client = None
		self.connected = False
		self.ruby_version = None

	def start(self, current_directory, file_name, *args):
		'''
		Start and attach the process
		'''
		# Create new process
		self.ruby_version = subprocess.Popen(["ruby", PathHelper.get_ruby_version_discoverer()], stdout=subprocess.PIPE).communicate()[0].splitlines()
		self.ruby_version[0] = self.ruby_version[0].decode("UTF-8")
		self.ruby_version[1] = self.ruby_version[1].decode("UTF-8")

		if self.ruby_version[1] == "UNSUPPORTED":
			self.log_message("Ruby version: "+self.ruby_version[0]+" is not supported.")
			return

		if os.name == "posix":
			process_params = "exec ruby '-C"+current_directory+"' '-r"+PathHelper.get_sublime_require()+"' '"+ file_name+"' "
			process_params += " ".join(args)
			self.process = subprocess.Popen(process_params, stdin = subprocess.PIPE, stderr = subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1, shell=True)
		else:
			process_params = ["ruby", "-C"+current_directory, "-r"+PathHelper.get_sublime_require(), file_name]
			process_params += args
			self.process = subprocess.Popen(process_params, stdin = subprocess.PIPE, stderr = subprocess.PIPE, stdout=subprocess.PIPE, bufsize=1, shell=False)

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

				# Start reader thread
				self.reader = Thread(target=self.reader_thread)
				self.reader.daemon = True
				self.reader.start()
				break
			except Exception as ex:
				if i == 8:
					self.log_message("Connection could not be made: "+str(ex)+'\n')
				else:
					time.sleep(1)

		# Start output thread
		self.outputer = Thread(target=lambda stream = self.process.stderr: self.output_thread(stream))
		self.outputer.daemon = True
		self.outputer.start()

		# Start errors thread
		self.outputer = Thread(target=lambda stream = self.process.stdout: self.output_thread(stream))
		self.outputer.daemon = True
		self.outputer.start()

	def output_thread(self, stream):
		# Always read stream`
		try:
			while True:
				bytes = stream.readline()

				if len(bytes) == 0:
					break

				result = str(bytes, "UTF-8")
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

				result = str(bytes, "UTF-8")
				self.data.write(result)
				self.data.flush()
				# self.log_message(result)

				if self.has_end_stream():
					self.handle_response()

		except Exception as ex:
			if self.connected:
				self.log_message("Debugger exception: "+str(ex)+'\n'+" StackTrace: "+traceback.format_exc())
				self.connected = False

		self.outputer.join()

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
			if file_name != "" and not PathHelper.is_same_path(PathHelper.get_sublime_require(), file_name):
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

				if PathHelper.is_same_path(PathHelper.get_sublime_require(), file_name):
					self.debugger.run_command(DebuggerModel.COMMAND_CONTINUTE)
			except queue.Empty:
				pass

		self.data = StringIO()
		self.data.write(next_result)

	def send_data(self, command, reason):
		self.requests.put({"signal": False, "reason": reason, "command": command})
		self.send_data_internal(command)

	def send_without_outcome(self, command):
		self.send_data_internal(command)

	def send_input(self, command):
		self.process.stdin.write(bytes(command+'\n',"UTF-8"))
		self.process.stdin.flush()

	def send_control_command(self, command):
		if not self.connected:
			return

		try:
			self.control_client.sendall(bytes(command+'\n', 'UTF-8'))
		except Exception as e:
			if self.connected:
				self.log_message("Failed communicate with process ("+command+"): "+str(e))

	def send_data_internal(self, command):
		if not self.connected:
			return

		try:
			self.client.sendall(bytes(command+'\n', 'UTF-8'))
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
			if self.debugger.match_ending(self.ruby_version[0], line):
				result.insert(len(result), "")
			else:
				result[len(result)-1] += line + '\n'

		return result

	def has_end_stream(self):
		end_of_stream = False
		for line in self.get_lines():
				if self.debugger.match_ending(self.ruby_version[0], line):
					end_of_stream = True;

		return end_of_stream

	def get_current_position(self):
		current_line = -1
		current_file = ""
		end_of_stream = False

		for line in self.get_lines():
			match = self.debugger.match_line_cursor(self.ruby_version[0], line)

			if match:
				current_line = match.groups()[0]

			match = self.debugger.match_file_cursor(self.ruby_version[0], line)
			if match:
				current_file = match.groups()[0]

		return current_file, int(current_line)

	def get_lines(self):
		return self.data.getvalue().split('\n')

	def stop(self):
		self.connected = False
		self.log_message("Stopping...")
		self.send_control_command("kill")
		if self.process:
			self.process.kill()
		self.process = None
