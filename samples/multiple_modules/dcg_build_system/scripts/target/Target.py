
'''
Copyright (c) 2016, Dylan Carleton Gundlach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''


import os
import sys
import io

class Target:
	def __init__(self, str_target, lst_target_deps):
		self.str_target = str_target
		self.lst_target_deps = lst_target_deps

	def make(self):
		for dep in self.lst_target_deps:
			dep.make()
		if(self._b_dirty()):
			if not os.path.exists(os.path.dirname(self.str_target)):
				os.makedirs(os.path.dirname(self.str_target))
			self.rule()

	#implement this
	def rule(self):
		assert(False)

	#

	def _b_dirty(self):
		if(os.path.isfile(self.str_target)):
			targetTime = self._findTargetTime()
			for target_dep in self.lst_target_deps:
				if(target_dep._b_dirty()):
					return True
				elif(target_dep._findTargetTime() > targetTime):
					return True
			return False
		else:
			return True

	def _findTargetTime(self):
		return(os.stat(self.str_target).st_mtime)
	

class LeafTarget(Target):
	def __init__(self, str_target):
		super().__init__(str_target, [])

	def rule(self):
		assert(True)

