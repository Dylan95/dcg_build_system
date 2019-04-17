
'''
Copyright (c) 2016, Dylan Carleton Gundlach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''


import re

import util
from target.Target import *

class Target_Obj(Target):

	def __init__(self, str_obj, target_src, lst_target_headers, compiler, perf, target_pch = None):
		self.target_pch = target_pch
		self.compiler = compiler
		#
		if(target_pch == None):
			super().__init__(str_obj, [target_src] + lst_target_headers, perf)
		else:
			super().__init__(str_obj, [target_src] + [target_pch] + lst_target_headers, perf)

	def rule(self, TargetThreadData_data):
		if(self.target_pch == None):
			self.compiler.compile(
				self.str_target, 
				self.lst_target_deps[0].str_target,
				TargetThreadData_data
			)
		else:
			self.compiler.compileWithPCH(
				self.str_target, 
				self.lst_target_deps[0].str_target, 
				self.lst_target_deps[1].str_target,
				self.lst_target_deps[1].lst_target_deps[0].str_target, #header dep, needed for choosing include flags
				TargetThreadData_data
			)



