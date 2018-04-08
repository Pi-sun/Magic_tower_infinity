import ctypes, datetime, os, random, threading

from kivy.clock import Clock

import generate_section as generator

SECTION_SIZE = generator.SECTION_SIZE
DEBUG_LOG = generator.DEBUG_LOG

DIM = generator.DIM
START = (1,) + tuple(generator.nextStart)
floors = {}

class EndGeneration(Exception):
	pass

def generateFloors(iters, callback):
	for i in range(iters):
		if DEBUG_LOG:
			if not os.path.exists("logs"):
				os.makedirs("logs")
			file = open("logs/generator_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_%d-to-%d.log" % (generator.nextFloor, generator.nextFloor + SECTION_SIZE - 1), "w")
		else:
			file = None
		
		def operate(sectionIndex, globalIndex, floor):
			def createWork(i):
				def work(dt):
					global floors
					floors[globalIndex] = floor
					callback(i * SECTION_SIZE + sectionIndex)
				return work
			Clock.schedule_once(createWork(i), 0)
		
		try:
			generator.generate_section(operate, file)
		except EndGeneration:
			return
		finally:
			if DEBUG_LOG and file:
				file.close()

generationThread = None

def prepareFloor(target, callback):
	global generationThread
	
	if target in floors:
		return 0
	elif target > 0:
		sectionStart = (target - 1) // SECTION_SIZE * SECTION_SIZE + 1
		iters = (sectionStart - generator.nextFloor) // SECTION_SIZE + 1
		generationThread = threading.Thread(target = lambda: generateFloors(iters, callback))
		generationThread.start()
		
		return SECTION_SIZE * iters
	else:
		raise ValueError("Cannot prepare non-positive floors yet!")
		
def stopPreparation():
	if not generationThread or not generationThread.isAlive():
		return

	exc = ctypes.py_object(EndGeneration)
	res = ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(generationThread.ident), exc)
	if res == 0:
		raise ValueError("Nonexistent thread id!")
	elif res > 1:
		# """if it returns a number greater than one, you're in trouble,
		# and you should call it again with exc=NULL to revert the effect"""
		ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(generationThread.ident), None)
		raise SystemError("PyThreadState_SetAsyncExc failed!")

def getState():
	return {
		"floors": floors,
		"generator": generator.getState()
	}

def setState(state):
	global floors
	floors = state["floors"]
	generator.setState(state["generator"])