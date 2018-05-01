import itertools, random

from mt_cells import *

from . import generator, award_area, floor_arrange
from . import npc_content_provider as provider
from .monsters import monsters_for,boss_for

def to_real_map(section,section_index):
    monsters=monsters_for(section_index)
    
    standard_gem_value = section_index
    standard_small_flask_value = section_index * 25
    standard_large_flask_value = section_index * 100
    
    big_location=[]
    small_location=[]
    for i in range(section.size):
        print('step4',i)
        section.floors[i].map=[[Empty() for j in range(section.floors[i].size)] for k in range(section.floors[i].size)]
        
        vault_loc = random.choice(section.floors[i].vault) if len(section.floors[i].vault)!=0 else None
        _portal=False
        
        for ci in range(section.floors[i].size):
            for ri in range(section.floors[i].size):
                if section.floors[i].content[ci][ri]==-1:
                    if section_index != 1 or i != 0:
                        section.floors[i].map[ci][ri]=Downstair()
                elif section.floors[i].content[ci][ri]==-2:
                    section.floors[i].map[ci][ri]=Upstair()
                elif section.floors[i].content[ci][ri]==2:
                    section.floors[i].map[ci][ri]=Wall()
                
                # basic contend generated

                # portal generation
    
                if section.floors[i].content[ci][ri]==0 and vault_loc != None and _portal==False:
                    if_portal=random.randint(0,10)
                    if if_portal==0:
                        section.floors[i].map[ci][ri]=Portal(*vault_loc)
                        section.floors[i].map[vault_loc[0]][vault_loc[1]] = Portal(ci, ri)
                        _portal=True
                        section.floors[i].portal=vault_loc
                elif section.floors[i].content[ci][ri]==1 or section.floors[i].content[ci][ri]==0 and _portal==False:
                    if_portal=random.randint(0,1000)
                    if if_portal==0:
                        #section.floors[i].map[ci][ri]= portal
                        _portal=True
                        section.floors[i].portal=generator.Board(section.floors[i].size)
                       
                # vault generation

                if [ci,ri] in section.floors[i].vault and [ci,ri] != vault_loc:    
                    luck=random.randint(1,10)
                    if luck>8:
                        section.floors[i].map[ci][ri]=AttackGem(standard_gem_value)
                        section.red_gem+=0.5
                    elif luck>6:
                        section.floors[i].map[ci][ri]=DefenceGem(standard_gem_value)
                        section.blue_gem+=0.5
                    elif luck>4:
                        section.floors[i].map[ci][ri]=Key(KEY_BLUE)
                        section.blue_key+=1
                    elif luck>2:
                        section.floors[i].map[ci][ri]=Key(KEY_YELLOW)
                        section.yellow_key+=1
                
                # begin to generate doors

                if section.floors[i].difficulty[ci][ri]==1.2:
                    section.floors[i].map[ci][ri]=KeyedDoor(KEY_YELLOW)
                    section.yellow_door+=1
                if section.floors[i].difficulty[ci][ri]==5.5:
                    section.floors[i].map[ci][ri]=KeyedDoor(KEY_BLUE)
                    section.blue_door+=1
                if section.floors[i].difficulty[ci][ri]==-2:
                    section.floors[i].map[ci][ri]=FakeWall()
                
                # begin to generate award

                if section.floors[i].difficulty[ci][ri]==-1:
                    small_location.append([i,ci,ri])
                    luck=random.randint(1,section.small_award)
                    if luck <= section.yellow_door*0.8:
                        section.floors[i].map[ci][ri]=Key(KEY_YELLOW)
                        section.yellow_key+=1
                    else:
                        section.floors[i].map[ci][ri]=SmallHealthPotion(standard_small_flask_value)
                        
                if section.floors[i].difficulty[ci][ri]==-5:
                    luck=random.randint(1,section.big_award)
                    big_location.append([i,ci,ri])
                    if luck <= section.blue_door*0.7:
                        section.floors[i].map[ci][ri]=Key(KEY_BLUE)
                        section.blue_key+=1
                    else:
                        section.floors[i].map[ci][ri]=LargeHealthPotion(standard_large_flask_value)
                        
                # to be done
                # generation for special award





                
                # begin to generate monsters


                    
                    
                if section.floors[i].difficulty[ci][ri]>0 and section.floors[i].difficulty[ci][ri]!=1.2 and section.floors[i].difficulty[ci][ri]!=5.5:
                    choices=[]
                    if section.floors[i].content[ci][ri]==1:
                        for m in monsters:
                            if m.difficulty(i+1)[0]<section.floors[i].difficulty[ci][ri]+1 and m.difficulty(i+1)[0]>section.floors[i].difficulty[ci][ri]-1:
                                choices.append(m)
                                
                    else:
                        for m in monsters:
                            if m.difficulty(i+1)[1]<section.floors[i].difficulty[ci][ri]+1 and m.difficulty(i+1)[1]>section.floors[i].difficulty[ci][ri]-1:
                                choices.append(m)
                    interval=2
                    while len(choices)==0:
                        if section.floors[i].content[ci][ri]==1:
                            for m in monsters:
                                if m.difficulty(i+1)[0]<section.floors[i].difficulty[ci][ri]+interval and m.difficulty(i+1)[0]>section.floors[i].difficulty[ci][ri]-interval:
                                    choices.append(m)
                                
                        else:
                            for m in monsters:
                                if m.difficulty(i+1)[1]<section.floors[i].difficulty[ci][ri]+interval and m.difficulty(i+1)[1]>section.floors[i].difficulty[ci][ri]-interval:
                                    choices.append(m)
                        interval+=1

                    section.floors[i].map[ci][ri]=random.choice(choices)(section_index)
                    
         # special generation
        if section.floors[i].special_requirement=='shop':
            for loc, item in zip(sorted(section.floors[i].special_actual), (ShopLeft(), Shop(provider.sharedShopContentProvider()), ShopRight())):
                section.floors[i].map[loc[0]][loc[1]] = item        
        elif section.floors[i].special_requirement=='guarded_area':
            luck=random.randint(0,5)
            fake_choose=None
            if i==section.sword_position:
                item = Sword(SWORD_TEXTURES[(section_index - 1) % len(SWORD_TEXTURES)], standard_gem_value*5)
            elif i==section.shield_position:
                item = Shield(SHIELD_TEXTURES[(section_index - 1) % len(SHIELD_TEXTURES)], standard_gem_value*5)
            
            if luck==0:
                special_map = [[Void() if i in {0, 4} or j in {0, 4} else Empty() for i in range(5)] for j in range(5)]
                special_map[random.randint(1, 3)][random.randint(1, 3)] = item
                special_map[4][2]=KeyedDoor(KEY_BLUE)
            elif luck==1:
                special_map = [[Void() if i in {0, 4} or j in {0, 3} else Empty() for i in range(5)] for j in range(5)]
                special_map[random.randint(1, 2)][random.randint(1, 3)] = item 
                special_map[3][2]=GuardedDoor()
                guard_monster_generator = random.choice(monsters)
                special_map[4][1]=guard_monster_generator(section_index)
                special_map[4][3]=guard_monster_generator(section_index)
                special_map[4][3].guard(special_map[3][2])
                special_map[4][1].guard(special_map[3][2])
            elif luck==2:
                special_map = [[Void() if i in {0, 4} or j in {0, 4} else Empty() for i in range(5)] for j in range(5)]
                special_map[random.randint(1, 3)][random.randint(1, 3)] = item

            elif luck==3:
                special_map = [[Void() if i in {0, 4} or j in {0, 3} else Empty() for i in range(5)] for j in range(5)]
                special_map[random.randint(1, 2)][random.randint(1, 3)] = item
                special_map[3][2]=GuardedDoor()
                guard_monster_generator = monsters[-2]
                special_map[4][1]=guard_monster_generator(section_index)
                special_map[4][3]=guard_monster_generator(section_index)
                special_map[4][3].guard(special_map[3][2])
                special_map[4][1].guard(special_map[3][2])
            elif luck==4:
                special_map = [[Void() if i in {0, 4} or j in {0, 3} else Empty() for i in range(5)] for j in range(5)]
                special_map[random.randint(1, 2)][random.randint(1, 3)] = item 
                special_map[3][2]=GuardedDoor()
                guard_monster_generator = random.choice(monsters)
                special_map[4][0]=guard_monster_generator(section_index)
                special_map[4][1]=guard_monster_generator(section_index)
                special_map[4][3]=guard_monster_generator(section_index)
                special_map[4][2]=guard_monster_generator(section_index)
                special_map[4][4]=guard_monster_generator(section_index)
                special_map[4][3].guard(special_map[3][2])
                special_map[4][1].guard(special_map[3][2])

            else:
                special_map = [[Wall() if i in {0, 4} or j in {0, 4} else Empty() for i in range(5)] for j in range(5)]
                area_walls=[]
                fake_choice=[]
                special_map[random.randint(1, 3)][random.randint(1, 3)] = item 
                for qs in range(0,5):
                    for us in range(0,5):
                        if qs in [0,4] or us in [0,4]:
                            if [qs,us] not in [[0,0],[0,4],[4,4],[4,0]]:
                                area_walls.append([qs+section.floors[i].special_start[0],us+section.floors[i].special_start[1]])
                for cell in area_walls:
                    if cell[0]==0+section.floors[i].special_start[0]:
                        if section.floors[i].check_item([cell[0]-1,cell[1]])==0 and section.floors[i].valid_position([cell[0]-1,cell[1]])==True:
                            fake_choice.append(cell)
                    if cell[0]==4+section.floors[i].special_start[0]:
                        if section.floors[i].check_item([cell[0]+1,cell[1]])==0 and section.floors[i].valid_position([cell[0]+1,cell[1]])==True:
                            fake_choice.append(cell)
                    if cell[1]==4+section.floors[i].special_start[1]:
                        if section.floors[i].check_item([cell[0],cell[1]+1])==0 and section.floors[i].valid_position([cell[0],cell[1]+1])==True:
                            fake_choice.append(cell)
                    else:
                        if section.floors[i].check_item([cell[0],cell[1]-1])==0 and section.floors[i].valid_position([cell[0],cell[1]-1])==True:
                            fake_choice.append(cell)
                print('fake',fake_choice)
                fake_choose=random.choice(fake_choice)
                print('choose',fake_choose)

            
                            
                            
                
            
            for loc, item in zip(sorted(section.floors[i].special_actual), itertools.chain(*special_map)):
                section.floors[i].map[loc[0]][loc[1]] = item
            if fake_choose!= None:
                section.floors[i].map[fake_choose[0]][fake_choose[1]]=FakeWall()
        elif section.floors[i].special_requirement=='boss':
            section.floors[i].map[section.floors[i].special_door[0]][section.floors[i].special_door[1]]=boss_for(section_index)(section_index)
    
    while section.blue_gem<section.size+1:
        for i in big_location:
            luck=random.randint(1,section.big_award)
            if luck<5:
                section.floors[i[0]].map[i[1]][i[2]]=DefenceGem(standard_gem_value)
                section.blue_gem+=1
                big_location.remove(i)
            if section.blue_gem>=section.size:
                break
                
    while section.red_gem<section.size+1:
        for i in big_location:
            luck=random.randint(1,section.big_award)
            if luck<5:
                section.floors[i[0]].map[i[1]][i[2]]=AttackGem(standard_gem_value)
                section.red_gem+=1
                big_location.remove(i)
            if section.red_gem>=section.size:
                break

    while section.yellow_key<0.6*section.yellow_door:
        for i in small_location:
            luck=random.randint(1,section.big_award)
            if luck<5:
                section.floors[i[0]].map[i[1]][i[2]]=Key(KEY_YELLOW)
                section.yellow_key+=1
