
'''
Copyright (c) 2016, Dylan Carleton Gundlach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

import os
import re
import sys
import timeit
import subprocess
import _thread

import cpp

from util.Util import *

from .Compiler import *

import project.Perf



class GCC_Compiler(cpp.toolsets.Compiler.Compiler):

	def init(
		self,
		str_cc,
		lst_str_cflags,
		lst_str_includeDirs,
		str_pchBuildDir
	):
		self.str_cc = str_cc
		self.lst_str_cflags = lst_str_cflags
		self.lst_str_includeDirs = lst_str_includeDirs
		self.str_pchBuildDir = str_pchBuildDir

	def compile(self, str_obj, str_src, TargetThreadData_data):
		TargetThreadData_data.perf.compileSrcT += self._compile("compile command", str_obj, str_src)

	def compilePCH(self, str_pch, str_header, TargetThreadData_data):
		TargetThreadData_data.perf.compilePchT += self._compile("precompile header command", str_pch, str_header)

	def makeDFile(self, str_dFile, str_file, TargetThreadData_data):
		TargetThreadData_data.perf.makeDFileT += self._exec(
			"make d file command",
			str(
				self.str_cc + " " + 
				self._str_includeDirs(self.lst_str_includeDirs) + " " +
				"-M " + 
				str_file + " " + 
				self._str_cflags(self.lst_str_cflags) + " " +
				"> " + str_dFile
			)
		)
		#
		str_write = ""
		for str_header in self._lst_parseDepFile(str_dFile):
			str_write += str_header + "\n"
		Util.writeFile_str(str_dFile, str_write)


	def compileWithPCH(self, str_obj, str_src, str_pch, str_pchHeader, TargetThreadData_data):
		#lst_str_pchIncludeDirs = []
		#for str_includeDir in self.lst_str_includeDirs:
		#	str_includeDirRel = Util.absToRel(str_includeDir)
		#	lst_str_pchIncludeDirs.append(os.path.join(self.str_pchBuildDir, str_includeDirRel))
		##
		#print(str_pchHeader)
		#print(lst_str_pchIncludeDirs)
		#print(list(filter(
		#	(lambda str_includeDir: (str_includeDir in str_pchHeader)),
		#	lst_str_pchIncludeDirs
		#)))
		TargetThreadData_data.perf.compileSrcT += self._exec(
			"compile with pch command",
			str(
				self.str_cc + " " + 
				self._str_includeDirs(list(map(
					(lambda str_includeDir: os.path.join(
						self.str_pchBuildDir,
						Util.absToRel(str_includeDir)
					)),
					list(filter(
						(lambda str_includeDir: (str_includeDir in str_pchHeader)),
						self.lst_str_includeDirs
					))
				))) + " " + 
				self._str_includeDirs(self.lst_str_includeDirs) + " " + 
				#"-H " + #debugging, see which headers are used
				"-c -o " + 
				str_obj + " " + 
				str_src + " " + 
				self._str_cflags(self.lst_str_cflags)
			)
		)

	def str_objName(self, str_srcName):
		return os.path.splitext(str_srcName)[0] + ".o"

	def str_pchName(self, str_headerName):
		return str_headerName + ".gch"

	#

	#returns: time to execute the command
	def _compile(self, str_message, str_out, str_in):
		return(self._exec(
			str_message,
			str(
				self.str_cc + " " + 
				self._str_includeDirs(self.lst_str_includeDirs) + " " +
				"-c -o " + 
				str_out + " " + 
				str_in + " " + 
				self._str_cflags(self.lst_str_cflags)
			)
		))

	#returns: time to execute the command
	def _exec(self, str_description, str_command):
		print(str_description + ":\n" + str_command + "\n\n")
		tStart = timeit.default_timer()
		returnCode = Util.exec(str_command)
		tEnd = timeit.default_timer()
		#
		if(returnCode != 0):
			print("makeSys: fatal error: the last command returned: " + str(returnCode))
			#_thread.interrupt_main();
			#os._exit(1) #nessecary to kill all threads, not just the current one
			#sys.exit(1)
			#todo: find a way to exit all threads properly, cause this is dumb
			this_code_will_crash_on_purpose_because_exit_doesnt_work_w_multi_threads
		return(tEnd - tStart)

	#
		
	def _str_cflags(self, lst_str_cflags):
		result = ""
		for str_cflag in lst_str_cflags:
			result += "-" + str_cflag + " "
		if(result != ""):
			result = result[0:-1]
		return result

	def _str_includeDirs(self, lst_str_includeDirs):
		result = ""
		for str_includeDir in lst_str_includeDirs:
			result += "-I\"" + str_includeDir + "\" "
		if(result != ""):
			result = result[0:-1]
		return result

	def _lst_parseDepFile(self, str_dFile):
		results = []
		for token in Util.str_readFile(str_dFile).split()[3:]:
			if(token != "\\"):
				results.append(token)
		return results






"""

	#returns: time to execute the command
	def _exec(self, str_description, str_command):
		print(str_description + ":\n" + str_command + "\n\n")
		tStart = timeit.default_timer()
		exitCode = os.system(str_command);
		tEnd = timeit.default_timer()
		#
		if(exitCode != 0):
			print("makeSys: fatal error: the last command returned: " + str(exitCode))
			#sys.exit(1)
		return(tEnd - tStart)


"""


