from monsters import monster_for
import generator

def to_real_map(section,section_index):
    monsters=monster_for(section_index)
    big_location=[]
    small_location=[]
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

                if section.floors[i].difficulty[ci][ri]==1:
                    small_location.append([i,ci,ri])
                    luck=random.randint(1,section.small_award)
                    if luck <= section.yellow_door*1.05:
                        new_map[ci][ri]='yellow key'
                        section.yellow_key+=1
                    else:
                        new_map[ci][ri]='small flask'
                        
                if section.floors[i].difficulty[ci][ri]==5:
                    luck=random.randint(1,section.big_award)
                    big_location.append([i,ci,ri])
                    if luck <= section.blue_door:
                        new_map[ci][ri]='blue key'
                    else:
                        new_map[ci][ri]='big flask'
                        
                    
                # begin to generate monsters


                    
                    
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

            # award adjustment
    while section.blue_gem<11:
        for i in big_location:
            luck=random.randint(1,section.big_award)
            if luck<5:
                section.floors[i[0]].map[i[1]][i[2]]='blue gem'
                section.blue_gem+=1
                
    while section.red_gem<11:
        for i in big_location:
            luck=random.randint(1,section.big_award)
            if luck<5:
                section.floors[i[0]].map[i[1]][i[2]]='red gem'
                section.blue_gem+=1

    while section.yellow_key<0.9*section.yellow_door:
        for i in small_location:
            luck=random.randint(1,section.big_award)
            if luck<5:
                section.floors[i[0]].map[i[1]][i[2]]='yellow key'
                section.yellow_key+=1

