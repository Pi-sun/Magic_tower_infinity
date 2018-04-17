# as main program it needs to force init its package core
import generator, award_area, floor_arrange,random

from monsters import monsters_for

def to_real_map(section,section_index):
    monsters=monsters_for(section_index)
    big_location=[]
    small_location=[]
    for i in range(section.size):
        print('step4',i)
        section.floors[i].map=list()
        for j in range(section.floors[i].size):
            section.floors[i].map.append([None]*section.floors[i].size)
        new_map=section.floors[i].map
        _portal=False
        for ci in range(section.floors[i].size):
            for ri in range(section.floors[i].size):
                if section.floors[i].content[ci][ri]==-1:
                    new_map[ci][ri]='start'
                if section.floors[i].content[ci][ri]==-2:
                    new_map[ci][ri]='end'
                if section.floors[i].content[ci][ri]==2:
                    new_map[ci][ri]='wall'
                if section.floors[i].content[ci][ri]==5:
                    new_map[ci][ri]='special'

                # basic contend generated

                # portal generation
    
                if section.floors[i].content[ci][ri]==0 and len(section.floors[i].vault)!=0 and _portal==False:
                    if_portal=random.randint(0,10)
                    if if_portal==0:
                        new_map[ci][ri]='portal'
                        _portal=True
                        random_position=random.randint(0,len(section.floors[i].vault)-1)
                        section.floors[i].portal=section.floors[i].vault[random_position]
                    
                elif section.floors[i].content[ci][ri]==1 or section.floors[i].content[ci][ri]==0 and _portal==False:
                    if_portal=random.randint(0,1000)
                    if if_portal==0:
                        new_map[ci][ri]='portal'
                        _portal=True
                        section.floors[i].portal=generator.Board(section.floors[i].size)
                # special generation

                if section.floors[i].content[ci][ri]==5:
                    new_map[ci][ri]=section.floors[i].special_requirement
                # vault generation

                if [ci,ri] in section.floors[i].vault:
                    luck=random.randint(1,10)
                    if luck>8:
                        new_map[ci][ri]='red gem'
                        section.red_gem+=0.5
                    elif luck>6:
                        new_map[ci][ri]='blue gem'
                        section.blue_gem+=0.5
                    elif luck>4:
                        new_map[ci][ri]='blue key'
                        section.blue_key+=1
                    elif luck>2:
                        new_map[ci][ri]='yellow key'
                        section.yellow_key+=1
                # begin to generate doors

                if section.floors[i].difficulty[ci][ri]==1.2:
                    new_map[ci][ri]='yellow door'
                    section.yellow_door+=1
                if section.floors[i].difficulty[ci][ri]==5.5:
                    section.blue_door+=1
                    new_map[ci][ri]='blue door'
                if section.floors[i].difficulty[ci][ri]==-2:
                    new_map[ci][ri]='hidden door'
                # begin to generate award

                if section.floors[i].difficulty[ci][ri]==-1:
                    small_location.append([i,ci,ri])
                    luck=random.randint(1,section.small_award)
                    if luck <= section.yellow_door*1.05:
                        new_map[ci][ri]='yellow key'
                        section.yellow_key+=1
                    else:
                        new_map[ci][ri]='small flask'
                        
                if section.floors[i].difficulty[ci][ri]==-5:
                    luck=random.randint(1,section.big_award)
                    big_location.append([i,ci,ri])
                    if luck <= section.blue_door:
                        new_map[ci][ri]='blue key'
                    else:
                        new_map[ci][ri]='big flask'
                        
                # to be done
                # generation for special award





                
                # begin to generate monsters


                    
                    
                if section.floors[i].difficulty[ci][ri]>0 and section.floors[i].difficulty[ci][ri]!=1.2 and section.floors[i].difficulty[ci][ri]!=5.5:
                    choices=[]
                    if section.floors[i].content[ci][ri]==1:
                        for j in range(len(monsters)):


                            if monsters[j].difficulty(i+1)[0]<section.floors[i].difficulty[ci][ri]+1 and monsters[j].difficulty(i+1)[0]>section.floors[i].difficulty[ci][ri]-1:
                                choices.append(j)
                                
                    else:
                        for j in range(len(monsters)):

                            if monsters[j].difficulty(i+1)[1]<section.floors[i].difficulty[ci][ri]+1 and monsters[j].difficulty(i+1)[1]>section.floors[i].difficulty[ci][ri]-1:
                                choices.append(j)
                    interval=2
                    while len(choices)==0:
                 
                        if section.floors[i].content[ci][ri]==1:
                            for j in range(len(monsters)):


                                if monsters[j].difficulty(i+1)[0]<section.floors[i].difficulty[ci][ri]+interval and monsters[j].difficulty(i+1)[0]>section.floors[i].difficulty[ci][ri]-interval:
                                    choices.append(j)
                                
                        else:
                            for j in range(len(monsters)):

                                if monsters[j].difficulty(i+1)[1]<section.floors[i].difficulty[ci][ri]+interval and monsters[j].difficulty(i+1)[1]>section.floors[i].difficulty[ci][ri]-interval:
                                    choices.append(j)
                        interval+=1
                        

                    monster_chosen=random.choice(choices)

                    new_map[ci][ri]='level'+str(section_index)+ 'monster'+ str(monster_chosen)

            # award adjustment
        if section.floors[i].special_requirement=='boss':
            new_map[section.floors[i].special_door[0]][section.floors[i].special_door[0]]='red door'
    section.difficulty_present()
    section.present()
    print(big_location)
    print(small_location)
    while section.blue_gem<section.size+1:
        for i in big_location:
            luck=random.randint(1,section.big_award)
            if luck<5:
                section.floors[i[0]].map[i[1]][i[2]]='blue gem'
                section.blue_gem+=1
                big_location.remove(i)
                
    while section.red_gem<section.size+1:
        for i in big_location:
            luck=random.randint(1,section.big_award)
            if luck<5:
                section.floors[i[0]].map[i[1]][i[2]]='red gem'
                section.red_gem+=1
                big_location.remove(i)

    while section.yellow_key<0.9*section.yellow_door:
        for i in small_location:
            luck=random.randint(1,section.big_award)
            if luck<5:
                section.floors[i[0]].map[i[1]][i[2]]='yellow key'
                section.yellow_key+=1




