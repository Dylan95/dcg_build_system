
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

	def __init__(self, nodeModule, str_buildDir, str_projectDir, toolset, perf, int_numThreads):
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
			STR_DIR_PCH
		)
		#
		dict_str_pchConfig = {}
		dict_pch = {}
		for nodePch in nodeModule["pch"]:
			str_src = Util.str_projectPath(nodePch["src"], str_projectDir)
			str_pch = Util.str_projectPath(nodePch["pch"], str_projectDir)
			dict_str_pchConfig[str_src] = str_pch
			dict_pch[str_src] = self._createPCH(str_pch, STR_DIR_PCH, STR_DIR_PCH_DEPS, perf, int_numThreads)
		#
		lst_str_srcWherePchUsed = []
		for str_src in info.lst_str_src:
			target_src = LeafTarget(str_src)
			#print("str_srcRel:")
			#print(str_src)
			#print(Util.absToRel(str_src))
			#input()
			str_srcRel = Util.absToRel(str_src)
			#
			pch = (
				dict_pch[str_src] 
				if (str_src in dict_pch) else
				None
			)
			if(pch != None):
				lst_str_srcWherePchUsed.append(str_src)
			#
			#print("Module: before Target_Obj")
			#print(str_srcRel)
			#print(os.path.splitext(str_srcRel))
			#print(STR_DIR_OBJ_DEPS)
			#print(self.compiler.str_objName(str_srcRel))
			#print(os.path.join(
			#	STR_DIR_OBJ_DEPS,
			#	os.path.splitext(str_srcRel)[0] + ".d"
			#))
			#input()
			#if(os.path.join(
			#	STR_DIR_OBJ_DEPS,
			#	os.path.splitext(str_srcRel)[0] + ".d"
			#) == "/usr/include/libunwind.h /usr/include/libunwind-x86_64.h"):
			#	print("Target::__init__ 0")
			#	input()
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
					target_src,
					perf,
					int_numThreads
				),
				self.compiler,
				perf,
				pch
			)
			#
			self.lst_target_objs.append(obj)
		if(set(lst_str_srcWherePchUsed) != set(dict_str_pchConfig)):
			print("pch mismatch detected: not all precompiled headers were used")
			print("source: ")
			print(info.lst_str_src)
			print("map: ")
			print(dict_str_pchConfig)
			sys.exit(1)

	#

	def _createPCH(self, str_pchHeader, str_pchDir, str_depDir, perf, int_numThreads):
		target_pchHeader = LeafTarget(str_pchHeader)
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
				target_pchHeader,
				perf,
				int_numThreads
			),
			self.compiler,
			perf
		)
		return result

	#makes a DFile and returns the contents
	def _lst_target_makeDFile(self, str_dFile, target_file, perf, int_numThreads):
		#print("BEFORE")
		#input()
		dFile = Target_DFile(
			str_dFile,
			target_file, 
			self.compiler,
			perf
		)
		#print("AFTER")
		#input()
		dFile.makeRec(int_numThreads)
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
				str_srcList,
				self.lst_str_src
			)
			Util.writeFile_lst(
				str_includeList,
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




