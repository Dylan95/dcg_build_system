
'''
Copyright (c) 2016, Dylan Carleton Gundlach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''


import os
import sys
import shutil
import platform
import time
import timeit
import json

from util.Util import *
from project.Module import *
from project.Config import *
from project.Perf import *

#import cpp.Target_Bin
#import cpp.Target_Obj

#usage:
#

str_buildSysDir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
str_projectDir = os.path.dirname(str_buildSysDir)
#
str_buildDir = os.path.join(str_buildSysDir, "build/")
#
rootNode = json.loads(Util.str_readFile(
	os.path.join(str_buildSysDir, "config.json")
))

def main():
	perf = Perf()
	timeStart = timeit.default_timer()
	#
	str_usage = "usage: (-build | -clean) [config_name] [module_name]"
	#
	#verify python version:
	if(sys.version_info[0] != 3):
		print(
			"buildSys.py: fatal error: python major version is \"" + 
			str(sys.version_info[0]) + 
			"\".  The script must be run with python major version 3."
		)
		sys.exit(2)
	#
	if(2 <= len(sys.argv) <= 4):
		if(sys.argv[1] == "-build"):
			_checkLastBuild()
			#
			if(len(sys.argv) == 2):
				make(perf)
			elif(len(sys.argv) == 3):
				makeConfig(sys.argv[2], perf)
			else:
				makeModule(sys.argv[2], sys.argv[3], perf)
			#
			shutil.copyfile(
				os.path.join(str_buildSysDir, "config.json"),
				os.path.join(str_buildDir, "last_config.json")
			)
		elif(sys.argv[1] == "-clean"):
			if(len(sys.argv) == 2):
				clean()
			elif(len(sys.argv) == 3):
				cleanConfig(sys.argv[2])
			else:
				cleanModule(sys.argv[2], sys.argv[3])
		else:
			print(str_usage)
	else:
		print(str_usage)
	#
	perf.totalT = timeit.default_timer() - timeStart
	perf.print()

def make(perf):
	for str_configKey in rootNode["configurations"]:
		makeConfig(str_configKey, perf)

def makeConfig(str_configKey, perf):
	config = Config(
		rootNode["configurations"][str_configKey],
		os.path.join(
			str_buildDir, 
			str_configKey
		),
		str_projectDir,
		perf
	)
	config.build()

def makeModule(str_configKey, str_moduleKey, perf):
	module = Module(
		rootNode["configurations"][str_configKey][str_moduleKey],
		os.path.join(
			str_buildDir, 
			str_configKey, 
			"modules", 
			str_moduleKey,
		),
		str_projectDir,
		perf
	)
	module.precompileHeaders()
	for obj in module.lst_target_objs:
		obj.make()

def clean():
	shutil.rmtree(str_buildDir)
	os.mkdir(str_buildDir)

def cleanConfig(str_configName):
	shutil.rmtree(os.path.join(
		str_buildDir, 
		str_configName
	))

def cleanModule(str_configName, str_moduleName):
	shutil.rmtree(os.path.join(
		str_buildDir, 
		str_configName, 
		"modules", 
		str_moduleName
	))

#

#checks the configuration for the last build to see if any changes in the
#configuration file have occured that require part or all of the last build.
def _checkLastBuild():
	str_lastConfigPath = os.path.join(str_buildDir, "last_config.json")
	if(os.path.exists(str_lastConfigPath)):
		lastRoot = json.loads(Util.str_readFile(str_lastConfigPath))
		for str_configKey in rootNode["configurations"]:
			_checkLastBuild_config(lastRoot, str_configKey)
	else:
		clean()

def _checkLastBuild_config(lastRoot, str_configKey):
	if(str_configKey in rootNode["configurations"]):
		thisBin = rootNode["configurations"][str_configKey]["bin"]
		lastBin = lastRoot["configurations"][str_configKey]["bin"]
		if(
			(thisBin["bin_name"] != 		lastBin["bin_name"]) or
			(thisBin["cc"] != 				lastBin["cc"]) or
			(thisBin["lflags"] != 			lastBin["lflags"]) or
			(thisBin["lib_directories"] != 	lastBin["lib_directories"]) or
			(thisBin["libs"] != 			lastBin["libs"])
		):
			shutil.rmtree(os.path.join(
				str_buildDir, 
				str_configKey, 
				"bin"
			))
		for str_moduleKey in rootNode["configurations"][str_configKey]["modules"]:
			_checkLastBuild_module(lastRoot, str_configKey, str_moduleKey)
	else:
		cleanConfig(str_configKey)

def _checkLastBuild_module(lastRoot, str_configKey, str_moduleKey):
	if(str_moduleKey in rootNode["configurations"][str_configKey]["modules"]):
		lastModule = lastRoot["configurations"][str_configKey]["modules"][str_moduleKey]
		thisModule = rootNode["configurations"][str_configKey]["modules"][str_moduleKey]
		#"src" is the one setting that doesn't require
		#the module to be rebuilt when its changed.
		if(
			(thisModule["cc"] != 					lastModule["cc"]) or
			(thisModule["cflags"] != 				lastModule["cflags"]) or
			(thisModule["include_directories"] != 	lastModule["include_directories"]) or
			(thisModule["pch"] != 					lastModule["pch"])
		):
			cleanModule(str_configKey, str_moduleKey)
	else:
		print("a")
		cleanModule(str_configKey, str_moduleKey)

#

main()





