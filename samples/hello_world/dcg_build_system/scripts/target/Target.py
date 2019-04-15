
'''
Copyright (c) 2016, Dylan Carleton Gundlach

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

'''


import os
import sys
import io

from project.Perf import *

#from multiprocessing import Process, Queue, Lock #Queues are thread and process safe.
import multiprocessing
import threading
int_useCores = max(1, multiprocessing.cpu_count() - 1)

def TargetThreadData_threadMake(TargetThreadData_data):
	#print("concurrent make")
	TargetThreadData_data.target.rule(TargetThreadData_data)
	#TargetThreadData_data.perf.compileSrcT += 1
	return TargetThreadData_data
	
#input/output for a thread
class TargetThreadData:
	def __init__(self, target): #, lock
		self.target = target
		self.perf = Perf() #by creating a seperate perf for every thread, then later adding them together, the need for synchronization of perf is avoided
		#self.lock = lock #broken

class Target:
	def __init__(self, str_target, lst_target_deps, perf):
	#def __init__(self, str_target, lst_target_deps):
		self.str_target = str_target
		self.lst_target_deps = lst_target_deps
		self.perf = perf

	def makeRec(self):
		#TargetThreadData(self, perf)
		#
		lst_lst_target_layers = []
		set_target_dirty = set()
		self.b_addToBuildTree(lst_lst_target_layers, 0, set(), set_target_dirty)
		#print(lst_lst_target_layers)
		#input()
		#
		#creation of directories needs to happen seperately, because 
		#(checking for the existence of a directory, then conditionally creating a directory) can't
		#be multithreaded, because that's a race condition.
		for target_dirty in set_target_dirty:
			if(target_dirty.str_target != None): #phony targets
				if not os.path.exists(os.path.dirname(target_dirty.str_target)):
					os.makedirs(os.path.dirname(target_dirty.str_target))
		#
		if(len(set_target_dirty) > 1):
			#lock = threading.Lock() #broken
			lst_lst_TargetThreadData_layers = list(map(
				lambda lst_target_layer: list(map(
					(lambda target_t: TargetThreadData(target_t)),
					lst_target_layer
				)),
				lst_lst_target_layers
			))
			#
			with multiprocessing.Pool(int_useCores) as p:
				for lst_TargetThreadData_layer in reversed(lst_lst_TargetThreadData_layers):
					if(len(lst_TargetThreadData_layer) != 0):
						lst_TargetThreadData_results = p.map(
							TargetThreadData_threadMake, 
							lst_TargetThreadData_layer
						)
						#print(lst_TargetThreadData_results)
						#input()
						#
						for TargetThreadData_result in lst_TargetThreadData_results:
							#print("did it mutate?")
							#TargetThreadData_result.perf.print()
							self.perf.add(TargetThreadData_result.perf)
		elif(len(set_target_dirty) == 1):
			TargetThreadData_data = TargetThreadData(list(set_target_dirty)[0])
			list(set_target_dirty)[0].rule(TargetThreadData_data)
			#
			self.perf.add(TargetThreadData_data.perf)

	#implement this
	def rule(self, TargetThreadData_data):
		assert(False)

	#
	
	#stores the layers of the build tree.  It's stored in layers instead of as a tree
	#because when it's run in parallel it will go layer by layer, doing all the dependancy files,
	#then the precompiled headers, etc.  This is so that the layers don't get garbled up: it's 
	#more intuitive to see a bunch of object files being compiled all at once, then see
	#them broken up with generating dependancy files, and doing other things.  The loss
	#in efficiency is pretty small, the only time that threads spend waiting is for the last
	#n-1 (where n is the number of threads) tasks being processed on each layer.  Overall this
	#inefficiency will probably add up to a couple seconds on most full builds.  A small
	#price to pay for keeping things in order.  Also this way makes the code easier.
	#
	#returns whether it's dirty or not
	def b_addToBuildTree(self, lst_lst_target_layers, int_layer, set_target_traversed, set_target_dirty):
		if(self in set_target_dirty):
			return True
		elif(self in set_target_traversed):
			return False
		else:
			set_target_traversed.add(self)
			#
			if(len(lst_lst_target_layers) <= int_layer):
				lst_lst_target_layers.append([])
			#
			b_childrenDirty = False
			for dep in self.lst_target_deps:
				if(dep.b_addToBuildTree(lst_lst_target_layers, int_layer+1, set_target_traversed, set_target_dirty)):
					b_childrenDirty = True
			#
			b_selfDirty = self._b_dirty()
			if(b_childrenDirty or b_selfDirty):
				lst_lst_target_layers[int_layer].append(self)
				set_target_dirty.add(self)

	def _b_dirty(self):
		if(self.str_target == None): #phony
			return False
		else:
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
	

class PhonyTarget(Target):
	def __init__(self, lst_target_deps, perf):
		super().__init__(None, lst_target_deps, perf)

	def rule(self, TargetThreadData_data):
		assert(True)


class LeafTarget(Target):
	def __init__(self, str_target):
		super().__init__(str_target, [], None)

	def rule(self, TargetThreadData_data):
		assert(True)

