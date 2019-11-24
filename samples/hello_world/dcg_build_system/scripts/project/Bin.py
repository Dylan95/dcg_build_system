
'''
Copyright (c) 2016, Dylan Carleton Gundlach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''


import os

from util.Util import *

from cpp.toolsets.Linker import *
from cpp.Target_Obj import *
from cpp.Target_Bin import *


#a group of source files to compile, and the compiler configuration.
class Bin(Target_Bin):
	#configDir must contain:
	#	binName.txt
	#	cc.txt
	#	lflags.txt
	#	libDirs.txt
	#	libs.txt
	def __init__(self, nodeBin, str_buildDir, str_projectDir, lst_target_objs, toolset, perf):
		str_bin = os.path.join(
			str_buildDir, 
			nodeBin["bin_name"]
		)
		linker = toolset.makeLinker(
			nodeBin["cc"],
			nodeBin["lflags"],
			self._lst_str_libDirs(nodeBin, str_projectDir),
			nodeBin["libs"]
		)
		#
		super().__init__(str_bin, lst_target_objs, linker, perf)

	#

	def _lst_str_libDirs(self, nodeBin, str_projectDir):
		results = []
		for str_dir in nodeBin["lib_directories"]:
			results.append(Util.str_projectPath(str_dir, str_projectDir))
		return results





