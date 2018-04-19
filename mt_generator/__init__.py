import random, sys

DIM = 11
SECTION_SIZE = 10 # Section size must be at least 2, to have 1 shop per section
DEBUG_LOG = True

from mt_cells import Point

# Required by npc_content_provider
def floor2section(floor):
    return (floor - 1) // SECTION_SIZE + 1

from . import award_area, floor_arrange, generator, map_generate
from . import npc_content_provider as provider

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
                if self.shield_position != self.sword_position and self.shield_position != self.shop_index:
                    break
        print('shop',self.shop_index)
        print('sword',self.sword_position)
        print('shield',self.shield_position)
    
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
    
    section=Section(SECTION_SIZE)
    if currentSection==1:
        section.difficulty=floor_arrange.section_design(SECTION_SIZE,True)
    else:
        section.difficulty=floor_arrange.section_design(SECTION_SIZE)
    
    start_pos = nextStart    
    i = 0

    while i < SECTION_SIZE:
        index=nextFloor + i
        
        if i == section.shop_index:
            section.floors[i]=generator.map_generate(DIM,start_pos,'shop')
        elif i == section.sword_position or i == section.shield_position:
            section.floors[i]=generator.map_generate(DIM,start_pos,'guarded_area')
        elif i == SECTION_SIZE - 1:
            section.floors[i]=generator.boss_floor_generate(start_pos,DIM)          
        else:
            section.floors[i]=generator.map_generate(DIM,start_pos)
        print('step1')

        award_area.award_area_optimize(section.floors[i])
        award_area.more_door(section.floors[i])
        award_area.key_position(section.floors[i])
        print('step2')
    
        if section.floors[i].start_position and section.floors[i].end_position and section.floors[i].start_position == start_pos:
            floor_arrange.floor_monster_main(section.floors[i],section.difficulty[i][0])
            print('step3')
        
            if callback and i != SECTION_SIZE - 1:
                callback(i + 1)
            
            start_pos = section.floors[i].end_position
            i += 1
        else:
            if DEBUG_LOG:
                section.floors[i].prettyPrint("Failed generation for #%d" % index, file)
    
    floor_arrange.floor_monster_award(section)
    print('step4')
    map_generate.to_real_map(section,currentSection)
    print('step5')
    
    # Finalize floor arrangement before here
    # The following loop initializes all floor cells
    for i in range(SECTION_SIZE):
        index = nextFloor + i
        
        if DEBUG_LOG:
            section.floors[i].prettyPrint("Successful generation for #%d" % index, file)
    
        for ri in range(DIM):
            for ci in range(DIM):
                section.floors[i].map[ri][ci].placeAt(index, Point(ri, ci))
    maps = {(nextFloor + i): section.floors[i].map for i in range(SECTION_SIZE)}
    
    def finialize():
        global nextFloor, nextStart
        nextFloor += SECTION_SIZE
        nextStart = start_pos
        return maps
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
