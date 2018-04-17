import random, sys, map_generate, floor_arrange

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
    def present(self):
        print('presented')
        for j in self.floors:
            print('\n')
            for i in j.map:
                    print(i)
    def difficulty_present(self):
        for i in self.floors:
            print('\n')
            for j in i.difficulty:
                print(j)
        
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
    #   (the last call to `callback` should pass a function that finalizes the generator state
    #    as a second parameter, which returns maps for a complete section represented by dict)
    
    currentSection = nextFloor // SECTION_SIZE + 1
    start_pos = nextStart    
    new_section=create_section(10,11,currentSection,start_pos)
    new_section.maps = {}
    

    i = 0

    while i < SECTION_SIZE:
        index=nextFloor + i
        
        #if i == SECTION_SIZE - 1:
         #   new_section.floors[i] = generator.boss_floor_generate(start_pos, DIM)
        #elif i == new_section.shop_index:
        #    new_section.floors[i] = generator.map_generate(DIM, start_pos, "shop")
        #else:
        #    new_section.floors[i] = generator.map_generate(DIM, start_pos)
            
        #award_area.award_area_optimize(new_section.floors[i])
        #award_area.more_door(new_section.floors[i])
        #award_area.key_position(new_section.floors[i])
        
        #empties = [] # Testing
        
        new_section.maps[index] = []
        for ri in range(DIM):
            row = []
            for ci in range(DIM):
                item = new_section.floors[i].map[ri][ci]
                if item == 'start':
                    if index == 1:
                        row.append(Empty())
                    else:
                        row.append(Downstair())
                elif item == 'end':
                    row.append(Upstair())
                elif item == None or item == 'portal':
                    row.append(Empty())
                    #empties.append((ri, ci)) # Testing
                elif item == 'wall':
                    row.append(Wall())
                elif item == 'yellow door':
                    row.append(KeyedDoor(KEY_YELLOW))
                elif item == 'blue door':
                    row.append(KeyedDoor(KEY_BLUE))
                elif item == 'special':
                    row.append(Empty()) # TODO: Other special entities
                elif len(item)==14:
                    row.append(monsters_for(currentSection)[int(item[13])](int(item[5])))
                else:
                    row.append(Empty())
            new_section.maps[index].append(row)
        print('step6')
        if i == new_section.shop_index:
            for loc, item in zip(sorted(new_section.floors[i].special_actual), (ShopLeft(), Shop(provider.sharedShopContentProvider()), ShopRight())):
                new_section.maps[index][loc[0]][loc[1]] = item
        print('step7')
        # Testing
        #loc = random.choice(empties)
        #new_section.maps[index][loc[0]][loc[1]] = monsters_for(currentSection)[0](currentSection)
        
        # Finalize floor arrangement before here
        # The following loop initializes all floor cells
        for ri in range(DIM):
            for ci in range(DIM):
                new_section.maps[index][ri][ci].placeAt(index, Point(ri, ci))
        
        if new_section.floors[i].start_position and new_section.floors[i].end_position and new_section.floors[i].start_position == start_pos:
            if DEBUG_LOG:
                print('hahaha')
                new_section.floors[i].prettyPrint("Successful generation for #%d" % index, file)
            
            if callback and i != SECTION_SIZE - 1:
                callback(i + 1)
            
            start_pos = new_section.floors[i].end_position
            i += 1
        else:
            if DEBUG_LOG:
                new_section.floors[i].prettyPrint("Failed generation for #%d" % index, file)
    print('step8')
    def finialize():
        global nextFloor, nextStart
        nextFloor += SECTION_SIZE
        nextStart = start_pos
        return new_section.maps
    if callback:
        callback(SECTION_SIZE, finialize)
    else:
        finialize()

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

def create_section(section_size,map_size,section_index,start):
    section=Section(section_size)
    starting_position=start
    for i in range(section_size):
        if i == section.shop_index:
            section.floors[i]=generator.map_generate(map_size,starting_position,'shop')
        elif i == section.size-1:
            section.floors[i]=generator.boss_floor_generate(starting_position,map_size)          
        else:
            section.floors[i]=generator.map_generate(map_size,starting_position)
        starting_position=section.floors[i].end_position

        award_area.award_area_optimize(section.floors[i])
        award_area.more_door(section.floors[i])
        award_area.key_position(section.floors[i])
    print('step1')

    section.difficulty=floor_arrange.section_design(section_size)
    print('step2')
    for i in range(section_size):
        floor_arrange.floor_monster_main(section.floors[i],section.difficulty[i][0])
    print('step3')
    floor_arrange.floor_monster_award(section)
    print('step4')
    map_generate.to_real_map(section,section_index)
    print('step5')

    return section
