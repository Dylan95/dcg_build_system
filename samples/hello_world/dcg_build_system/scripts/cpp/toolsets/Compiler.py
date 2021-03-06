
'''
Copyright (c) 2016, Dylan Carleton Gundlach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''


class Compiler:

	def init(
		self,
		str_cc,
		lst_str_cflags,
		lst_str_includeDirs,
		str_pchBuildDir,
		b_forceForwardSlash,
		lst_str_rootPathReplace 
	):
		assert(False)

	#implement
	def compile(self, str_obj, str_src, TargetThreadData_data):
		assert(False)

	#implement
	def compilePCH(self, str_pch, str_header, TargetThreadData_data):
		assert(False)

	#implement
	def compileWithPCH(self, str_obj, str_src, str_pch, TargetThreadData_data):
		assert(False)
		
	#implement
	def makeDFile(self, str_dFile, str_src, TargetThreadData_data):
		assert(False)

	def str_objName(self, str_srcName):
		assert(False)

	def str_pchName(self, str_srcName):
		assert(False)

