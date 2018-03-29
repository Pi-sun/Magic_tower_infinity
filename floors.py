import ctypes, datetime, os, random, sys, threading

from kivy.clock import Clock

from cells import *
import award_area, generator

SECTION_SIZE = 20
DEBUG_LOG = True

dim = 11

def genLoc():
    return (random.randint(0, dim - 1), random.randint(0, dim - 1))

start = (1,) + genLoc()
floors = {}

# Used by generation thread
nextFloor = 1
nextStart = start[1:]

class EndGeneration(Exception):
    pass

def generate_section(callback, file = sys.stdout):
    # Meanings of variables, with examples:
    # (when generating levels 11 - 15, where SECTION_SIZE = 5)
    # `i` takes values 0 - 4
    # `index` takes values 11 - 15
    # `nextFloor` is kept as 11 (the first floor's index)
    # `nextStart` is kept as the start position of level 11
    # `start_pos` is constantly updated to be the start position of the next floor
    # `board` is the current floor, represented as a Board object (from generator.py)
    # `floor` is the current floor, represented as an array of Cells (from cells.py)
    # `callback` parameter of this function must be called after every round of
    #    generation to update graphics

    global nextFloor, nextStart
    
    start_pos = nextStart
    i = 0
    while i < SECTION_SIZE:
        index = nextFloor + i
    
        if i == SECTION_SIZE - 1:
            board = generator.boss_floor_generate(list(start_pos), dim)
        else:
            board = generator.map_generate(dim, list(start_pos))
        award_area.award_area_optimize(board)
        
        starts = []
        ends = []
        
        floor = []
        for ri in range(dim):
            row = []
            for ci in range(dim):
                item = board.content[ri][ci]
                if item == -1:
                    if index == 1:
                        row.append(Empty())
                    else:
                        row.append(Downstair())
                elif item == -2:
                    row.append(Upstair())
                elif item == 0 or item == 1:
                    row.append(Empty())
                elif item == 2:
                    row.append(Wall())
                elif item == 3:
                    row.append(KeyedDoor(KEY_YELLOW))
                elif item == 5:
                    row.append(Wall()) # TODO: Special entities
            floor.append(row)
        
        if board.start_position and board.end_position and tuple(board.start_position) == start_pos:
            if DEBUG_LOG:
                board.prettyPrint("Successful generation for #%d" % index, file)
            
            callback(i + 1, index, floor)
            i += 1
            start_pos = tuple(board.end_position)
        else:
            if DEBUG_LOG:
                board.prettyPrint("Failed generation for #%d" % index, file)
                
    nextFloor += SECTION_SIZE
    nextStart = start_pos

def generateFloors(iters, callback):
    for i in range(iters):
        if DEBUG_LOG:
            if not os.path.exists("logs"):
                os.makedirs("logs")
            file = open("logs/generator_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + "_%d-to-%d.log" % (nextFloor, nextFloor + SECTION_SIZE - 1), "w")
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
            generate_section(operate, file)
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
        iters = (sectionStart - nextFloor) // SECTION_SIZE + 1
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
