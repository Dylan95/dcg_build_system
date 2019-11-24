
'''
Copyright (c) 2016, Dylan Carleton Gundlach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''


from util.Util import *
from target.Target import *
from cpp.toolsets.Compiler import *

class Target_DFile(Target):

	#str_cc: only gcc/g++ compilers are supported.  ex. g++, g++-6, etc.
	def __init__(self, str_dFile, target_srcFile, compiler, perf):
		self.compiler = compiler
		self.target_srcFile = target_srcFile
		#
		super().__init__(str_dFile, [target_srcFile], perf)

	def rule(self, TargetThreadData_data):
		self.compiler.makeDFile(
			self.str_target, 
			self.target_srcFile.str_target,
			TargetThreadData_data
		)

	def lst_target_getTargets(self):
		results = []
		for str_header in Util.str_readFile(self.str_target).split("\n"):
			if(str_header != ""):
				#if(str_header == "/usr/include/libunwind.h /usr/include/libunwind-x86_64.h"):
				#	print("Target::__init__ 1")
				#	input()
				#print("Target_DFile::lst_target_getTargets")
				#print(self.str_target)
				#print(str_header)
				#input()
				results.append(LeafTarget(str_header))
		return results

