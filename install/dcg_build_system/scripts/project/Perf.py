
'''
Copyright (c) 2016, Dylan Carleton Gundlach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''

import multiprocessing
import threading
int_useCores = max(1, multiprocessing.cpu_count() - 1)


#the total times

class Perf:

	def __init__(self):
		self.totalT = 0
		#
		self.makeDFileT = 0
		self.compileSrcT = 0
		self.compilePchT = 0
		self.linkT = 0

	def add(self, Perf_other):
		self.totalT += Perf_other.totalT
		self.makeDFileT += Perf_other.makeDFileT
		self.compileSrcT += Perf_other.compileSrcT
		self.compilePchT += Perf_other.compilePchT
		self.linkT += Perf_other.linkT

	def print(self):
		if(int_useCores == 1):
			print("1 thread.  precice times:")
		else:
			#because sometimes threads will be waiting for other threads when there's
			#n-1 tasks to complete for any group of tasks (creating precompiled headers, creating object files, etc), where n is the number of threads, but I've estimated the times by assuming that there are n threads always working.  It probably wont be off by much, maybe a couple seconds.
			print(str(int_useCores) + " threads, times are slightly off.")
		print("total time:                    " + str(self.totalT))
		print("time to make dependancy files: " + str(self.makeDFileT / int_useCores))
		print("time to compile source:        " + str(self.compileSrcT / int_useCores))
		print("time to precompile headers:    " + str(self.compilePchT / int_useCores))
		print("time to link:                  " + str(self.linkT / int_useCores))
		print("misc time:                     " + 
			str(max(0, self.totalT - 
				((
					self.makeDFileT +
					self.compileSrcT +
					self.compilePchT +
					self.linkT
				) / int_useCores)
			))
		)


