import ctypes, datetime, os, random, threading, traceback

from kivy.clock import Clock

import generate_section as generator

SECTION_SIZE = generator.SECTION_SIZE
DEBUG_LOG = generator.DEBUG_LOG
DIM = generator.DIM

class EndGeneration(Exception):
	pass

def generateSection(i, callback, completion):
	if DEBUG_LOG:
		if not os.path.exists("logs"):
			os.makedirs("logs")
		file = open("logs/generator_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_%d-to-%d.log" % (generator.nextFloor, generator.nextFloor + SECTION_SIZE - 1), "w")
	else:
		file = None
	
	def operate(sectionIndex, finalize = None):
		def work(dt):
			global floors
			if finalize:
				fs = finalize()
				floors.update(fs)
			callback(i * SECTION_SIZE + sectionIndex)
			if finalize:
				completion()
		Clock.schedule_once(work, 0)
	
	try:
		generator.generate_section(operate, file)
	except EndGeneration:
		if DEBUG_LOG:
			print("Program stopped, force generation to end...", file = file)
			traceback.print_exc(file = file)
		return
	except:
		traceback.print_exc()
		Clock.schedule_once(lambda dt: exit(), 0)
	finally:
		if DEBUG_LOG:
			file.close()

generationThread = None

def generateFloors(iters, callback):
	i = -1
	def completion():
		nonlocal i
		i += 1
		if i < iters:
			generationThread = threading.Thread(target = lambda: generateSection(i, callback, completion))
			generationThread.start()
	completion()

def prepareFloor(target, callback):
	global generationThread
	
	if target in floors:
		return 0
	elif target > 0:
		sectionStart = (target - 1) // SECTION_SIZE * SECTION_SIZE + 1
		iters = (sectionStart - generator.nextFloor) // SECTION_SIZE + 1
		generateFloors(iters, callback)
		
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
	
def newState():
	global START, floors
	
	generator.newState()

	START = (1,) + tuple(generator.nextStart)
	floors = {}
