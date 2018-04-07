import random, sys

from mt_cells import *

# override base monster classes with generator's scaled monster data creators
from monsters import *

import award_area, generator

SECTION_SIZE = 10 # Section size must be at least 2, to have 1 shop per section
DEBUG_LOG = True

def generate_section(callback, file = sys.stdout):
    # Meanings of variables, with examples:
    # (when generating levels 11 - 15, where SECTION_SIZE = 5)
    # `i` takes values 0 - 4
    # `index` takes values 11 - 15
    # `nextFloor` is kept as 11 (the first floor's index)
    # `nextStart` is kept as the start position of level 11
    # `start_pos` is constantly updated to be the start position of the next floor
    # `board` is the current floor, represented as a Board object (from generator.py)
    # `floor` is the current floor, represented as an array of Cells (from package mt_cells)
    # `callback` parameter of this function must be called after every round of
    #    generation to update graphics

    global nextFloor, nextStart
    
    currentSection = nextFloor // SECTION_SIZE + 1
    
    shopIndex = random.randint(0, SECTION_SIZE - 2)
    
    start_pos = nextStart
    i = 0
    while i < SECTION_SIZE:
        index = nextFloor + i
        
        if i == SECTION_SIZE - 1:
            board = generator.boss_floor_generate(list(start_pos), dim)
        elif i == shopIndex:
            board = generator.map_generate(dim, list(start_pos), "shop")
        else:
            board = generator.map_generate(dim, list(start_pos))
        award_area.award_area_optimize(board)
        award_area.more_door(board)
        
        empties = [] # Testing
        
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
                    empties.append((ri, ci)) # Testing
                elif item == 2:
                    row.append(Wall())
                elif item == 3:
                    row.append(KeyedDoor(KEY_YELLOW))
                elif item == 5:
                    row.append(Empty()) # TODO: Other special entities
            floor.append(row)
        
        if i == shopIndex:
            for loc, item in zip(sorted(board.special_actual), (ShopLeft(), Shop(), ShopRight())):
                floor[loc[0]][loc[1]] = item
        
        # Testing
        loc = random.choice(empties)
        floor[loc[0]][loc[1]] = GreenSlimeB(currentSection)
        
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
