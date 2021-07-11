
'''
Copyright (c) 2016, Dylan Carleton Gundlach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''


import os

from util.Util import *



class Search:

	#returns: a list of absolute file names
	#folders are either absolute or relative to "str_projectDir"
	@staticmethod
	def lst_str_fileSearch(nodeSearch, str_projectDir):
		lst_str_files = []
		for str_dir in nodeSearch["directories"]:
			lst_str_files += Util.immediate_files(Util.str_projectPath(str_dir, str_projectDir))
		for str_dir in nodeSearch["directories_recursive"]:
			lst_str_files += Util.lst_recursiveFiles(Util.str_projectPath(str_dir, str_projectDir))
		#
		results = []
		for str_file in lst_str_files:
			if(Search._b_match(str_file, nodeSearch["filetypes"])):
				results.append(str_file)
		return results

	#

	@staticmethod
	def _b_match(str_file, lst_str_types):
		for str_type in lst_str_types:
			if(str_file.endswith(str_type)):
				return True
		return False





