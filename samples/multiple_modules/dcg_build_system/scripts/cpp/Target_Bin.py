
'''
Copyright (c) 2016, Dylan Carleton Gundlach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''


from target.Target import *

class Target_Bin(Target):

	def __init__(self, str_bin, lst_target_objs, linker):
		self.linker = linker
		self.lst_target_objs = lst_target_objs[:]
		#
		super().__init__(str_bin, lst_target_objs)

	def rule(self):
		lst_str_objs = []
		for o in self.lst_target_objs:
			lst_str_objs.append(o.str_target)
		self.linker.link(self.str_target, lst_str_objs)


