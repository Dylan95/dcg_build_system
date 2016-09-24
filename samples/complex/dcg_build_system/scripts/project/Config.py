
'''
Copyright (c) 2016, Dylan Carleton Gundlach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''


import os
import glob
import json

from util.Util import *

from .Module import *
from .Bin import *

from cpp.toolsets.Toolset import *


class Config:

	def __init__(self, nodeConfig, str_buildDir, str_projectDir, perf):
		self.modules = None
		self.bin = None
		#
		toolset = Toolset(nodeConfig["toolset"])
		self.modules = Config.Modules(
			nodeConfig["modules"],
			os.path.join(
				str_buildDir, 
				"modules"
			),
			str_projectDir,
			toolset,
			perf
		)
		#
		self.bin = Bin(
			nodeConfig["bin"],
			os.path.join(
				str_buildDir, 
				"bin"
			),
			str_projectDir,
			self.modules.lst_target_objs(),
			toolset,
			perf
		)

	def build(self):
		self.bin.make()

	#

	class Modules:
		def __init__(self, nodeModules, str_buildDir, str_projectDir, toolset, perf):
			self.lst_modules = []
			#
			for str_nodeModuleKey in nodeModules:
				module = Module(
					nodeModules[str_nodeModuleKey], 
					os.path.join(
						str_buildDir, 
						str_nodeModuleKey
					),
					str_projectDir,
					toolset,
					perf
				)
				self.lst_modules.append(module)
		#
		def lst_target_objs(self):
			results = []
			for module in self.lst_modules:
				results += module.lst_target_objs
			return results






