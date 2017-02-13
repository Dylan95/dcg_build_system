
'''
Copyright (c) 2016, Dylan Carleton Gundlach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''


#the total times

class Perf:

	def __init__(self):
		self.totalT = 0
		#
		self.makeDFileT = 0
		self.compileSrcT = 0
		self.compilePchT = 0
		self.linkT = 0

	def print(self):
		print("total time:                    " + str(self.totalT))
		print("time to make dependancy files: " + str(self.makeDFileT))
		print("time to compile source:        " + str(self.compileSrcT))
		print("time to precompile headers:    " + str(self.compilePchT))
		print("time to link:                  " + str(self.linkT))
		print("misc time:                     " + 
			str(
				self.totalT - 
				self.makeDFileT -
				self.compileSrcT -
				self.compilePchT -
				self.linkT
			)
		)


