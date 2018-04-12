from monsters import *
import generator

def to_real_map(section,section_index):
    for i in range(len(section.size)):
        section.floors[i].map=list()
        for j in range(section.floors[i].size):
            section.floors[i].map.append([None]*section.floors[i].size)
        new_map=section.floors[i].map
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

                if 
                # begin to generate monsters

                monsters=monster_for(section_index)

                    
                    
                if section.floors[i].difficulty[ci][ri]>0 and section.floors[i].difficulty[ci][ri]!=1.2 and section.floors[i].difficulty[ci][ri]!=5.5:
                    choices=[]
                    if section.floors[i].content[ci][ri]==1:
                        for j in range(len(monsters)):

                            if monsters[j].difficulty[0]<section.floors[i].difficulty[ci][ri]+1 and monsters[j].difficulty[0]>section.floors[i].difficulty[ci][ri]-1:
                                choices.append(j)
                                
                    else:
                        for j in range(len(monsters)):

                            if monsters[j].difficulty[1]<section.floors[i].difficulty[ci][ri]+1 and monsters[j].difficulty[1]>section.floors[i].difficulty[ci][ri]-1:
                                choices.append(j)

                    monster_chosen=random.randint(0,len(choices))

                    new_map[ci][ri]='level'+str(section_index)+ 'monster'+ str(monster_chosen)

