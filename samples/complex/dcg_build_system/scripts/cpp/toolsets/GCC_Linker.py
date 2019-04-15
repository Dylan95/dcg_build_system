
'''
Copyright (c) 2016, Dylan Carleton Gundlach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''


import os
import sys
import timeit

from .Linker import *

class GCC_Linker(Linker):

	#implement
	def init(
		self,
		str_cc,
		lst_str_lflags,
		lst_str_libDirs,
		lst_str_libs
	):
		self.str_cc = str_cc
		self.lst_str_lflags = lst_str_lflags
		self.lst_str_libDirs = lst_str_libDirs
		self.lst_str_libs = lst_str_libs

	def link(self, str_bin, lst_str_objs, TargetThreadData_data):
		TargetThreadData_data.perf.linkT += self._exec(
			"link command",
			str(
				self.str_cc + " " + 
				self._str_lflags() + " " + 
				self._str_objs(lst_str_objs) + " " + 
				"-o " + 
				str_bin + " " + 
				self._str_libDirs() + " " + 
				self._str_libs()
			)
		)

	#

	#returns: time to execute the command
	def _exec(self, str_description, str_command):
		print(str_description + ":\n" + str_command + "\n\n")
		tStart = timeit.default_timer()
		exitCode = os.system(str_command);
		tEnd = timeit.default_timer()
		#
		if(exitCode != 0):
			print("makeSys: fatal error: the last command returned: " + str(exitCode))
			sys.exit(1)
		return(tEnd - tStart)

	def _str_objs(self, lst_str_objs):
		result = ""
		for o in lst_str_objs:
			result += o + " "
		if(result != ""):
			result = result[0:-1]
		return result

	def _str_lflags(self):
		result = ""
		for str_flag in self.lst_str_lflags:
			result += "-" + str_flag + " "
		if(result != ""):
			result = result[0:-1]
		return result

	def _str_libDirs(self):
		result = ""
		for str_libDir in self.lst_str_libDirs:
			result += "-L\"" + str_libDir + "\" "
		if(result != ""):
			result = result[0:-1]
		return result

	def _str_libs(self):
		result = ""
		for str_lib in self.lst_str_libs:
			result += "-l" + str_lib + " "
		if(result != ""):
			result = result[0:-1]
		return result



