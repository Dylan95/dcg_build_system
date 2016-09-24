
'''
Copyright (c) 2016, Dylan Carleton Gundlach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''


import io
import os

class Util:
	
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
				lst.append(subfile)
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
				os.path.join(result, str_path)
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
		lst_split = str_pathPart.split(os.sep)
		#print("SPLIT: " + str(lst_split))
		for str_item in lst_split[1:]:
			lst_split[0] = os.path.join(lst_split[0], str_item)
		return(lst_split[0])

	#

	#raw path should use '/' seperators
	#path must not have '/' as folder or file names.
	#returns an absolute path.  if rawPath is local, it'll be relative to projectDir
	@staticmethod
	def str_projectPath(str_rawPath, str_projectDir):
		lst_path = str_rawPath.split("/")
		str_path = Util.joinPaths(lst_path)
		if(not os.path.isabs(str_path)):
			str_rawPath = os.path.join(str_projectDir, str_rawPath)
		return str_rawPath

	#

	#write string to file
	@staticmethod
	def writeFile_str(str_filename, string):
		file = open(str_filename, 'w')
		file.write(string)
		file.close()

	#write list of strings to file
	@staticmethod
	def writeFile_lst(str_filename, lst_str):
		str_write = ""
		for string in lst_str:
			str_write += str_write + "\n"
		Util.writeFile_str(str_filename, str_write)















