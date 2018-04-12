import random, sys

DIM = 11
SECTION_SIZE = 10 # Section size must be at least 2, to have 1 shop per section
DEBUG_LOG = True

from mt_cells import *

# Required by npc_content_provider
def floor2section(floor):
    return (floor - 1) // SECTION_SIZE + 1

import award_area, generator
from monsters import monsters_for
import npc_content_provider as provider

class Section:
    def __init__(self,size=10):
        self.small_award=0
        self.big_award=0
        self.size=size
        self.floors=[None]*size
        self.gem_number=10
        self.red_gem=0
        self.blue_gem=0
        self.flask_health=0
        self.monster_count=0
        self.yellow_key=0
        self.blue_key=0
        self.red_key=0
        self.yellow_door=0
        self.blue_door=0
        self.red_door=0
        if self.size>3:
            self.shop_index=random.randint(0,size-3)
            while True:
                self.sword_position=random.randint(0,size-2)
                if self.sword_position!=self.shop_index:
                    break
            while True:
                self.shield_position=random.randint(0,size-2)
                if self.shield_position not in [self.sword_position,self.shop_index]:
                    break
        
def generate_section(callback = None, file = sys.stdout):
    # Meanings of variables, with examples:
    # (when generating levels 11 - 15, where SECTION_SIZE = 5)
    # `i` takes values 0 - 4
    # `index` takes values 11 - 15
    # `nextFloor` is kept as 11 (the first floor's index)
    # `nextStart` is kept as the start position of level 11
    # `start_pos` is constantly updated to be the start position of the next floor
    # `board` is the current floor, represented as a Board object (from generator.py)
    # `floor` is the current floor, represented as an array of Cells (from package mt_cells)
    # `callback` parameter of this function shall be called after every round of
    #    generation to update graphics

    global nextFloor, nextStart
    
    currentSection = nextFloor // SECTION_SIZE + 1
    new_section=Section()
    monsters = monsters_for(currentSection)
    
    start_pos = nextStart
    i = 0

    while i < SECTION_SIZE:
        index = nextFloor + i
        
        if i == SECTION_SIZE - 1:
            new_section.floors[i] = generator.boss_floor_generate(start_pos, DIM)
        elif i == new_section.shop_index:
            new_section.floors[i] = generator.map_generate(DIM, start_pos, "shop")
        else:
            new_section.floors[i] = generator.map_generate(DIM, start_pos)
            
        award_area.award_area_optimize(new_section.floors[i])
        award_area.more_door(new_section.floors[i])
        award_area.key_position(new_section.floors[i])
        
        empties = [] # Testing
        
        floor = []
        for ri in range(DIM):
            row = []
            for ci in range(DIM):
                item = new_section.floors[i].content[ri][ci]
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
        
        if i == new_section.shop_index:
            for loc, item in zip(sorted(new_section.floors[i].special_actual), (ShopLeft(), Shop(provider.sharedShopContentProvider()), ShopRight())):
                floor[loc[0]][loc[1]] = item
        
        # Testing
        loc = random.choice(empties)
        floor[loc[0]][loc[1]] = monsters[0](currentSection)
        
        # Finalize floor arrangement before here
        # The following loop initializes all floor cells
        for ri in range(DIM):
            for ci in range(DIM):
                floor[ri][ci].placeAt(index, Point(ri, ci))
        
        if new_section.floors[i].start_position and new_section.floors[i].end_position and new_section.floors[i].start_position == start_pos:
            if DEBUG_LOG:
                new_section.floors[i].prettyPrint("Successful generation for #%d" % index, file)
            
            if callback:
                callback(i + 1, index, floor)
            
            start_pos = new_section.floors[i].end_position
            i += 1
        else:
            if DEBUG_LOG:
                new_section.floors[i].prettyPrint("Failed generation for #%d" % index, file)
                
    nextFloor += SECTION_SIZE
    nextStart = start_pos

def getState():
    return {
        "nextFloor": nextFloor,
        "nextStart": nextStart,
        "providers": provider.getState()
    }

def setState(state):
    global nextFloor, nextStart
    nextFloor = state["nextFloor"]
    nextStart = state["nextStart"]
    provider.setState(state["providers"])
    
def newState():
    global nextFloor, nextStart
    nextStart = [random.randint(0, DIM - 1), random.randint(0, DIM - 1)]
    nextFloor = 1
    provider.newState()
