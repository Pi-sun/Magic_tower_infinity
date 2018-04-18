import random

modifier=1

'difficulty is a two_dimensional vector measuring roughly how much damage the monster can do to hero in the early and later part of the section'
'for example, a mage with average attack and defense will have a balance difficulty of [10,10]'
'on the other hand, a skeleton with high attack and low defense will have lower early_section difficulty and higher late-section difficulty, such as [15,5]'
'and high defense guard may have extremely high early_section difficulty and low late_section one, such as [99,8]'
'difficulty will only be measured within a setion, meaning that all sections will have a similar difficulty'

'award is also measured in two ways, health/defense and attack'

'difficulty of a floor is measured by two index between 0 and 10'
'pass difficulty is calculated by an unknown algorithm taking into account the difficulty and award on the main/side route'
'end section difficulty is calculated based on difficulty/award in the award_area of the floor'

'for the ease of camparison, all difficulty and award level will be measured with a index from 0 to 10'

def section_design(section_size):
    'return the difficulty of each floor using different designs'
    'pass-difficulty-design includes standard, less_standard, half-half'
    result=list()
    for i in range(section_size):
        result.append([0,0])
    design_index=random.randint(0,5)
    if design_index==0:
        design='standard'
        for i in range(section_size):
            result[i][0]=i/(section_size/10)
    if design_index==1:
        design='less standard'
        for i in range(section_size):
            result[i][0]=(2*i/section_size)**2*2.5
    if design_index==2:
        design='half-half'
        for i in range(int(0.5*section_size)):
            result[i][0]=i/section_size*9
        for i in range(int(0.5*section_size),section_size):
            result[i][0]=10-(section_size-i)/section_size*9
    if design_index==3:
        design='hill'
        for i in range(section_size):
            result[i][0]=i/(section_size/10)
        result[int(0.5*section_size)][0]=8.5
    if design_index==4:
        design='bad'
        for i in range(section_size):
            result[i][0]=(i/section_size*100)**0.5
    if design_index==5:
        design='restart'
        for i in range(int(0.5*section_size)):
            result[i][0]=i/section_size*16
        for i in range(int(0.5*section_size),section_size):
            result[i][0]=(i+1-0.5*section_size)/section_size*16
    print(design)
    'generation of second difficulty index'        
    design_index=random.randint(0,5)
    if design_index==0:
        design_2='standard'
        for i in range(section_size):
            result[i][1]=i/(section_size/10)/2+3.5
    if design_index==1:
        design_2='less standard'
        for i in range(section_size):
            result[i][1]=(i/section_size*2)**2*2.5/2+4
    if design_index==2:
        design_2='half-half'
        for i in range(int(0.5*section_size)):
            result[i][1]=3
        for i in range(int(0.5*section_size),section_size):
            result[i][1]=7
    if design_index==3:
        design_2='haha'
        for i in range(section_size):
            result[i][1]=5
    if design_index==4:
        design_2='hell'
        for i in range(section_size):
            result[i][1]=8-i/(section_size/10)/2
    if design_index==5:
        design_2='random'
        for i in range(section_size):
            result[i][1]=random.randint(3,8)
    
    
    result=fluctuate(result)
    return result

def fluctuate(section):
    'input a series of difficulty(dipole) which do no need to be integers and return the final_difficulty'
    for i in range(len(section)):
        change_1=random.randint(0,20)
        change=change_1**2/200
        direction=random.randint(0,1)
        if direction==1:
            section[i][0]=int(section[i][0]+change)
        else:
            section[i][0]=int(section[i][0]-change)
        if section[i][0]>10:
            section[i][0]=10
        if section[i][0]<0:
            section[i][0]=0
    for i in range(len(section)):
        change_1=random.randint(0,20)
        change=change_1**2/200
        direction=random.randint(0,1)
        if direction==1:
            section[i][1]=int(section[i][1]+change)
        else:
            section[i][1]=int(section[i][1]-change)
        if section[i][1]>10:
            section[i][1]=10
        if section[i][1]<0:
            section[i][1]=0
    return section

def floor_monster_main(board,difficulty):
    'return the difficulty of monster on the board'
    board.difficulty=list()
    for i in range(board.size):
        board.difficulty.append([0]*board.size)
    real_difficulty=2*difficulty
    key=[]
    trial=0
    for i in board.key_main:
        key.append(i)
    while True:
        for i in key:
            if_mon=random.randint(0,2)
            'there is mon'
            if if_mon==0:
                mon_diff=random.randint(0,real_difficulty)
                if mon_diff>=1.2*difficulty:
                    if_ultra=random.randint(0,10)
                    if if_ultra==0:
                        board.difficulty[i[0]][i[1]]=mon_diff
                        real_difficulty-=mon_diff
                        key.remove(i)
                else:
                    board.difficulty[i[0]][i[1]]=mon_diff
                    real_difficulty-=mon_diff
                    key.remove(i)
        if real_difficulty==0 or len(key)==0:
            break
        else:
            trial+=1
        if trial==30:
            board.difficulty=list()
            for i in range(board.size):
                board.difficulty.append([0]*board.size)
            real_difficulty=2*difficulty
            key=[]
            for i in board.key_main:
                key.append(i)
        if trial==60:
            break

        
    real_difficulty=2*difficulty
    key=[]
    trial=0
    for i in board.key_side:
        key.append(i)
    while True:
        for i in key:
            if_mon=random.randint(0,2)
            'there is mon'
            if if_mon==0:
                mon_diff=random.randint(0,real_difficulty)
                if mon_diff>=1.2*difficulty:
                    if_ultra=random.randint(0,10)
                    if if_ultra==0:
                        board.difficulty[i[0]][i[1]]=mon_diff
                        real_difficulty-=mon_diff
                        key.remove(i)
                else:
                    board.difficulty[i[0]][i[1]]=mon_diff
                    real_difficulty-=mon_diff
                    key.remove(i)
        if real_difficulty==0 or len(key)==0:
            break
        else:
            trial+=1
        if trial==30:
            for i in board.side_route:
                board.difficulty[i[0]][i[1]]=0

            real_difficulty=2*difficulty
            key=[]
            for i in board.key_side:
                key.append(i)
        if trial==60:
            break

    for i in board.main_route:
        if board.difficulty[i[0]][i[1]]!=0:
            heh=random.randint(0,5)
            if heh==1:
                board.difficulty[i[0]][i[1]]=-1
    print(board.key_main,board.key_side)
    
def floor_monster_award(section):
    # -1 difficulty refer to small flask, yellow key
    # -5 difficulty refer to blue key, big flask, and gems
    # -10 difficulty refer to ability item
    for i in range(section.size):
        section.floors[i].present()
        section.floors[i].award_present()
        print(section.floors[i].award_listing)
        for j in section.floors[i].award_listing:
            door=random.randint(0,100)
            if door==100:
                section.floors[i].difficulty[j[1][0]][j[1][1]]=20

            #red door
            elif door>90:
                section.floors[i].difficulty[j[1][0]][j[1][1]]=5.5
            #intended as blue door
            elif door>10:
                section.floors[i].difficulty[j[1][0]][j[1][1]]=1.2
            #intended as yellow door
            elif door>3:
                section.floors[i].difficulty[j[1][0]][j[1][1]]=random.randint(0,int(section.difficulty[i][1]+0.8))
            elif door>0:
                section.floors[i].difficulty[j[1][0]][j[1][1]]=random.randint(0,10)
            else:
                section.floors[i].difficulty[j[1][0]][j[1][1]]=-2
                
                'hidden wall'
        for k in section.floors[i].area_key:
            for j in k:
                if_mon=random.randint(0,4)
                if if_mon<1:
                    section.floors[i].difficulty[j[0]][j[1]]=random.randint(0,10)
                elif if_mon<4:
                    section.floors[i].difficulty[j[0]][j[1]]=random.randint(0,int(section.difficulty[i][1]+0.8))
        end_area=find_end_area(section.floors[i])

        for k in end_area:
            j=k
            difficulty_level=0
            while True:
            
            
                if section.floors[i].award_listing[j][0]==-1:
                    # handle the area directly connected to the main/side route
                    net_award=random.randint(-3,3)+int(section.difficulty[i][1])-difficulty_level-5+modifier

                    _continue=False
                else:
                    #handle the other area
                    net_award=random.randint(-5,3)+int(section.difficulty[i][1])-difficulty_level-5+modifier
                    print('mdzz',net_award)
                    _continue=True
                current_difficulty=section.floors[i].difficulty[(section.floors[i].award_listing[j][1][0])][(section.floors[i].award_listing[j][1][1])]
                # hahahahhahah
                for m in section.floors[i].area_key[j]:
                    current_difficulty+=section.floors[i].difficulty[m[0]][m[1]]

                # avoid tooo few monster
                if current_difficulty<3:
                    for m in section.floors[i].award_area[j]:
                        small_mon=random.randint(1,10)
                        if small_mon<3:
                            section.floors[i].difficulty[m[0]][m[1]]=1
                        elif small_mon<6:
                            section.floors[i].difficulty[m[0]][m[1]]=-1
                            
                    
                award=net_award-current_difficulty
                difficulty_level=current_difficulty+award_award_area(section.floors[i],j,award)

                if _continue:
                    j=section.floors[i].award_listing[j][0]

                else:
                    break
        # then dealing with more doors

        all_door=[]
        parrelel_door=[]
        for ii in section.floors[i].award_listing:
            all_door.append(ii)
        for iii in section.floors[i].parrelel_door:
            for ii in iii:
                if ii not in all_door:
                    parrelel_door.append(ii)
        for j in parrelel_door:
            what=random.randint(0,3)
            if what==0:
                section.floors[i].difficulty[j[0]][j[1]]=-2
            else:
                section.floors[i].difficulty[j[0]][j[1]]=5.5

        for ri in section.floors[i].difficulty:
            for ci in ri:
                if ci==-1:
                    section.small_award+=1
                if ci==-5:
                    section.big_award+=1
                if ci>0 and ci!=1.2 and ci!= 5.5:
                    section.monster_count+=1
                if ci==5.5:
                    section.blue_door+=1
                if ci==1.2:
                    section.yellow_door+=1

                
            
    return None

def award_award_area(board,index,award):
    empty_position=[]
    for position in board.award_area[index]:
        if board.difficulty[position[0]][position[1]]==0:
            empty_position.append(position)
    net_difficulty=0
    for i in empty_position:
        board.difficulty[i[0]][i[1]]=-1
        net_difficulty-=1
    for i in range(1):
        for i in empty_position:
            if net_difficulty>award:
                board.difficulty[i[0]][i[1]]=-5
                net_difficulty-=4
            if net_difficulty<award:
                heh=random.randint(1,10)
                if heh>2:
                    board.difficulty[i[0]][i[1]]=0
                    net_difficulty+=1
    return net_difficulty

def find_end_area(board):
    non_end_area=set()
    end_area=set()

    for i in board.award_listing:
        non_end_area.add(i[0])
    for i in range(len(board.award_area)):
        if i not in non_end_area:
            end_area.add(i)
    return end_area
    
def section_difficulty(section):
    'manage the difficulty of the section'
    section.difficulty=section_design(section.size)
    for i in len(section.size):
        floor_monster_main(section.floor[i],section.difficulty[i][0])
    floor_monster_award(section)

        
    return section
    

if __name__=='__main__':
    import generate_section, generator, award_area

    a=generate_section.Section(5)
    a.difficulty=section_design(5)
    
    prev_end=[1,2]
    for i in range(5):
        a.floors[i]=generator.map_generate(11,prev_end)
        award_area.award_area_optimize(a.floors[i])
        award_area.more_door(a.floors[i])
        award_area.key_position(a.floors[i])
        floor_monster_main(a.floors[i],a.difficulty[i][0])
        
        prev_end=a.floors[i].end_position

    floor_monster_award(a)
    for floor in a.floors:
        floor.prettyPrint()

    print('small',a.small_award)
    print('large',a.big_award)
    print('monster',a.monster_count)
    print('yellow',a.yellow_door)
    print('blue',a.blue_door)
