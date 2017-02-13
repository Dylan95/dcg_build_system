
'''
Copyright (c) 2016, Dylan Carleton Gundlach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''


import sys

from .GCC_Compiler import *
from .GCC_Linker import *

class Toolset:

	def __init__(self, str_toolset):
		self.CompilerType = None
		self.LinkerType = None
		#
		if(str_toolset == "GCC"):
			self.CompilerType = GCC_Compiler
			self.LinkerType = GCC_Linker
		else:
			print("buildSys: fatal error: unrecognized toolset: \"" + str_toolset + "\"")
			sys.exit(4)

	def makeCompiler(self, str_cc, lst_str_cflags, lst_str_includeDirs, str_pchBuildDir, perf):
		result = self.CompilerType()
		result.init(
			str_cc, lst_str_cflags, lst_str_includeDirs, str_pchBuildDir, perf
		)
		return result

	def makeLinker(self, str_cc, lst_str_lflags, lst_str_libDirs, lst_str_libs, perf):
		result = self.LinkerType()
		result.init(
			str_cc, lst_str_lflags, lst_str_libDirs, lst_str_libs, perf
		)
		return result



