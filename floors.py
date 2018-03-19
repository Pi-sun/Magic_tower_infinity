import random, threading, wx

from cells import *
from generator import map_generate

dim = 10
def genLoc():
	return (random.randint(0, dim - 1), random.randint(0, dim - 1))

start = (1,) + genLoc()

floors = {}
startLocs = {1: start[1:]}

SECTION_SIZE = 10

class FloorPreparer:
	def __init__(self, sectionStart, handler):
		self.sectionStart = sectionStart
		self.handler = handler
		self.currentIndex = 0
		
	def prepare(self):
		index = self.sectionStart + self.currentIndex
		
		def afterWork(floor):
				global floors, startLocs
				floor.present()

				floors[index] = []
				for ri in range(dim):
					row = []
					for ci in range(dim):
						item = floor.content[ri][ci]
						if item == -1:
							row.append(Empty()) # TODO: Staircase down
						elif item == -2:
							row.append(Empty()) # TODO: Staircase up
							startLocs[index + 1] = (ri, ci)
						elif item == 0 or item == 1:
							row.append(Empty())
						elif item == 2:
							row.append(Wall())
						elif item == 3:
							row.append(Wall()) # TODO: Door
						elif item == 5:
							row.append(Wall()) # TODO: Special entities
					floors[index].append(row)
			
				self.currentIndex += 1
				self.handler(self.currentIndex)
				if self.currentIndex < SECTION_SIZE:
					self.prepare()
		
		def work():
			wx.CallAfter(afterWork, map_generate(dim, startLocs[index], 'shop'))
			
		threading.Thread(target = work).start()

def prepareFloor(target, handler):
	if target in floors:
		return 0
	else:
		sectionStart = (target - 1) // SECTION_SIZE * SECTION_SIZE + 1		
		FloorPreparer(sectionStart, handler).prepare()
		return SECTION_SIZE
			