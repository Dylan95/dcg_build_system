
'''
Copyright (c) 2016, Dylan Carleton Gundlach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''


import io
import os
import subprocess
import sys
import tempfile
import time
import collections
import json

class Util:
	
	@staticmethod
	def map_jsonLoadFolder(str_dir):
		map_result = {}
		for str_path in sorted(Util.lst_recursiveFiles(str_dir)):
			if(str_path.endswith("json")):
				print("parsing: " + str_path)
				map_m = json.loads(Util.str_readFile(str_path))
				Util.map_mergeJsonMaps(map_result, map_m)
		return map_result
	
	@staticmethod
	def map_mergeJsonMaps(map_insert, map_copy):
		for key,val in map_copy.items():
			if(
				isinstance(val, collections.Mapping) and
				(key in map_insert)
			):
				Util.map_mergeJsonMaps(map_insert[key], val)
			elif(
				isinstance(val, list) and
				(key in map_insert)
			):
				map_insert[key] += val
			else:
				map_insert[key] = val
	
	@staticmethod
	def str_readFile(str_filename):
		file = open(str_filename, 'r')
		s = file.read()
		file.close()
		return s

	@staticmethod
	def lst_readLines(str_filename):
		file = open(str_filename, 'r')
		lst = file.read().split("\n")
		file.close()
		return lst

	#

	@staticmethod
	def lst_recursiveDirs(str_dir):
		lst = []
		for dirname, subdirs, subfiles in os.walk(str_dir):
			lst.append(dirname)
		return lst

	@staticmethod
	def lst_recursiveFiles(str_dir):
		lst = []
		for dirname, subdirs, subfiles in os.walk(str_dir):
			for subfile in subfiles:
				lst.append(os.path.join(dirname, subfile))
		return lst

	@staticmethod
	def lst_files(str_dir):
		return os.listdir(str_dir)
	
	#

	#http://stackoverflow.com/questions/800197/how-to-get-all-of-the-immediate-subdirectories-in-python
	@staticmethod
	def immediate_subdirs(a_dir):
		results = []
		for name in os.listdir(a_dir):
			if os.path.isdir(os.path.join(a_dir, name)):
				results.append(name)
		return results

	#full paths of files returned
	@staticmethod
	def immediate_files(a_dir):
		results = []
		for name in os.listdir(a_dir):
			if os.path.isfile(os.path.join(a_dir, name)):
				results.append(a_dir + "/" + name)
		return results

	#

	@staticmethod
	def joinPaths(lst_paths):
		if(len(lst_paths) == 0):
			return root_path()
		else:
			result = lst_paths[0]
			for str_path in lst_paths[1:]:
				result = os.path.join(result, str_path)
			return result
		
	#see:
	#http://stackoverflow.com/questions/12041525/a-system-independent-way-using-python-to-get-the-root-directory-drive-on-which-p
	@staticmethod
	def root_path():
		return os.path.abspath(os.sep)

	#absolute path to a path relative to the root directory.
	#usefull for when you want to join an absolute path: 
	#	os.path.join(otherPath, absToRel(absolutePath))
	@staticmethod
	def absToRel(str_abs):
		str_pathPart = os.path.splitdrive(str_abs)[1]
		#lst_split = str_pathPart.split(os.sep + "|" + "/")
		lst_split = str_pathPart.split(os.sep)
		str_result = lst_split[0]
		for str_item in lst_split[1:]:
			str_result = os.path.join(str_result, str_item)
		#if(str_abs.endswith("image_DXT.o")):
		#	print("absToRel:")
		#	print(str_abs)
		#	print(str_result)
		#	input()
		return(str_result)

	#

	#raw path should use '/' seperators
	#path must not have '/' as folder or file names.
	#returns an absolute path.  if rawPath is local, it'll be relative to projectDir
	@staticmethod
	def str_projectPath(str_rawPath, str_projectDir):
		if("\\" in str_rawPath):
			print(rawPath)
			print("error: path has backslashes in it.  Use only forward slashes for seperators, they will be converted to windows' uncivilized format internally when absolutely nessecary.")
			intentional_crash
		lst_path = str_rawPath.split("/")
		str_path = Util.joinPaths(lst_path)
		#
		return os.path.join(str_projectDir, str_rawPath)

	#

	#write string to file
	@staticmethod
	def writeFile_str(str_filename, string):
		file = open(str_filename, 'w+')
		file.write(string)
		file.close()

	#write list of strings to file
	@staticmethod
	def writeFile_lst(str_filename, lst_str):
		str_write = ""
		for string in lst_str:
			str_write += string + "\n"
		Util.writeFile_str(str_filename, str_write)

	#







	#return: return code of process
	#prints the stderr and stdout from the subprocess to
	#sys.stderr and sys.stdout respectivly.
	#using sys.stderr and sys.stdout directly doesn't seem to work.
	def exec(str_command):
		proc = subprocess.Popen(
			str_command, 
			shell=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE
		)
		#
		#nessecary to do this instead of proc.wait() to prevent hanging on large amount of output
		while(proc.poll() != None):
			proc.communicate()
			time.sleep(.1)
		#
		out, err = proc.communicate()
		sys.stdout.write(out.decode(sys.getdefaultencoding()))
		sys.stderr.write(err.decode(sys.getdefaultencoding()))
		#
		return(proc.returncode)










"""
	#return: return code of process
	#def exec(str_command, tempOut, tempErr):
	def exec(str_command):
		proc = subprocess.Popen(
			str_command, 
			shell=True,
			#stdout=subprocess.PIPE,
			#stderr=subprocess.PIPE
			#stdout=sys.stderr,
			stdout=sys.stdout,
			stderr=sys.stderr
		)
		proc.wait()
		#
		#out, err = proc.communicate()
		#sys.stdout.write(out.decode())
		#sys.stdout.write(proc.stdout.read())
		#sys.stderr.write(proc.stderr.read())
		#
		return(proc.returncode)

"""











