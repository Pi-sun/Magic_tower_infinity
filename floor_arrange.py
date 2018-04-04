import generator,random

'difficulty is a two_dimensional vector measuring roughly how much damage the monster can do to hero in the early and later part of the section'
'for example, a mage with average attack and defense will have a balance difficulty of [10,10]'
'on the other hand, a skeleton with high attack and low defense will have lower early_section difficulty and higher late-section difficulty, such as[15,5]'
'and high defense guard may have extremely high early_section difficulty and low late_section one, such as[99,8]'
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
            result[i][1]=i/(section_size/10)/2+2.5
    if design_index==1:
        design_2='less standard'
        for i in range(section_size):
            result[i][1]=(i/section_size*2)**2*2.5/2+2.5
    if design_index==2:
        design_2='half-half'
        for i in range(int(0.5*section_size)):
            result[i][1]=3
        for i in range(int(0.5*section_size),section_size):
            result[i][1]=7
    if design_index==3:
        design_2='haha'
        for i in range(section_size):
            result[i][1]=4
    if design_index==4:
        design_2='hell'
        for i in range(section_size):
            result[i][1]=7.5-i/(section_size/10)/2
    if design_index==5:
        design_2='random'
        for i in range(section_size):
            result[i][1]=random.randint(3.7)
    
    
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
if __name__=='__main__':
    for i in section_design(10):
        print(i)
    
