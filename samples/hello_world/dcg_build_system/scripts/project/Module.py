
'''
Copyright (c) 2016, Dylan Carleton Gundlach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''


import os
import sys
import io

from util.Util import *

from cpp.toolsets.Toolset import *

from cpp.Target_Obj import *
from cpp.Target_PCH import *
from cpp.Target_DFile import *

from .Search import *



#a group of source files to compile, and the compiler configuration.
class Module:

	def __init__(self, nodeModule, str_buildDir, str_projectDir, toolset, perf):
		self.compiler = None
		self.lst_target_objs = []
		#
		STR_DIR_PCH = os.path.join(str_buildDir, "pch")
		STR_DIR_OBJS = os.path.join(str_buildDir, "objs")
		STR_DIR_OBJ_DEPS = os.path.join(str_buildDir, "src_deps")
		STR_DIR_PCH_DEPS = os.path.join(str_buildDir, "pch_deps")
		#
		info = Module.Info(nodeModule, str_projectDir)
		info.write(str_buildDir)
		#
		self.compiler = toolset.makeCompiler(
			nodeModule["cc"],
			nodeModule["cflags"],
			info.lst_str_includeDirs,
			STR_DIR_PCH,
			perf
		)
		#
		dict_pch = {}
		for nodePch in nodeModule["pch"]:
			str_src = Util.str_projectPath(nodePch["src"], str_projectDir)
			str_pch = Util.str_projectPath(nodePch["pch"], str_projectDir)
			dict_pch[str_src] = str_pch
		#
		for str_src in info.lst_str_src:
			target_src = LeafTarget(str_src)
			str_srcRel = Util.absToRel(str_src)
			#
			obj = Target_Obj(
				os.path.join(
					STR_DIR_OBJS,
					self.compiler.str_objName(str_srcRel)
				),
				target_src, 
				self._lst_target_makeDFile(
					os.path.join(
						STR_DIR_OBJ_DEPS,
						os.path.splitext(str_srcRel)[0] + ".d"
					),
					target_src
				),
				self.compiler,
				self._target_pch(
					dict_pch, 
					STR_DIR_PCH,
					STR_DIR_PCH_DEPS,
					str_src
				)
			)
			#
			self.lst_target_objs.append(obj)

	#

	def _target_pch(self, dict_pch, str_pchDir, str_depDir, str_src):
		if(str_src in dict_pch):
			target_pchHeader = LeafTarget(dict_pch[str_src])
			str_headerRel = Util.absToRel(target_pchHeader.str_target)
			#
			result = Target_PCH(
				os.path.join(
					str_pchDir, 
					self.compiler.str_pchName(str_headerRel)
				), 
				target_pchHeader, 
				self._lst_target_makeDFile(
					os.path.join(
						str_depDir,
						os.path.splitext(str_headerRel)[0] + ".d"
					),
					target_pchHeader
				),
				self.compiler
			)
			return result
		else:
			return None

	#makes a DFile and returns the contents
	def _lst_target_makeDFile(self, str_dFile, target_file):
		dFile = Target_DFile(
			str_dFile,
			target_file, 
			self.compiler
		)
		dFile.make()
		return dFile.lst_target_getTargets()

	#

	class Info:
		def __init__(self, nodeModule, str_projectDir):
			#the source files to be compiled
			self.lst_str_src = self._lst_str_src(nodeModule["src"], str_projectDir)
			#include directories
			self.lst_str_includeDirs = self._lst_str_includeDirs(nodeModule["include_directories"], str_projectDir)
		#
		def write(self, str_buildDir):
			str_infoDir = os.path.join(str_buildDir, "info")
			str_includeList = os.path.join(str_infoDir, "include_directories_list.txt")
			str_srcList = os.path.join(str_infoDir, "src_list.txt")
			#
			if not os.path.exists(os.path.dirname(str_srcList)):
				os.makedirs(os.path.dirname(str_srcList))
			#
			Util.writeFile_lst(
				str_includeList,
				self.lst_str_src
			)
			Util.writeFile_lst(
				str_srcList,
				self.lst_str_includeDirs
			)
		#
		def _lst_str_src(self, nodeSrc, str_projectDir):
			results = []
			#
			for str_src in nodeSrc["src"]:
				results.append(Util.str_projectPath(str_src, str_projectDir))
			for str_src in Search.lst_str_fileSearch(nodeSrc["search"], str_projectDir):
				results.append(str_src)
			return results
		#
		def _lst_str_includeDirs(self, nodeInclude, str_projectDir):
			results = []
			#
			for str_dir in nodeInclude["include_directories"]:
				results.append(Util.str_projectPath(
					str_dir, 
					str_projectDir
				))
			for str_dir in nodeInclude["include_directories_recursive"]:
				results += Util.lst_recursiveDirs(Util.str_projectPath(
					str_dir, 
					str_projectDir
				))
			return results




