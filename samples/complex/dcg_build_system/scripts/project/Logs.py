
import os
import sys

from util.Util import *

class Logs:
	def __init__(self, str_outDir):
		self.file_out = open(
			os.path.join(
				str_outDir,
				"stdout.txt"
			),
			"w"
		)
		self.file_err = open(
			os.path.join(
				str_outDir,
				"stderr.txt"
			),
			"w"
		)
		#
		self.log_out = Logs.LogStream(sys.stdout, self.file_out)
		self.log_err = Logs.LogStream(sys.stderr, self.file_err)

	def start(self):
		sys.stdout = self.log_out
		sys.stderr = self.log_err

	def end(self):
		self.log_out.flush()
		self.log_err.flush()
		#
		sys.stdout = sys.__stdout__
		sys.stderr = sys.__stderr__
		#
		self.file_out.close()
		self.file_err.close()


	#outputs to log files and to the console
	#
	#usage:
	#myout = LogOutput(sys.stdout, "logFile.txt")
	#sys.stdout = myout
	#
	#reset to default
	#myout.flush()
	#sys.stdout = sys.__stdout__
	#
	class LogStream:
		def __init__(self, stream, logFile):
			self.stream = stream
			self.logFile = logFile

		def write(self, data):
			self.stream.write(data)
			self.logFile.write(data)

		def flush(self):
			self.stream.flush()
			self.logFile.flush()

		def fileno(self):
			return(self.stream.fileno())


