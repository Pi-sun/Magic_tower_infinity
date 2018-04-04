import generator

'difficulty is a two_dimensional vector measuring roughly how much damage the monster can do to hero in the early and later part of the section'
'for example, a mage with average attack and defense will have a balance difficulty of [10,10]'
'on the other hand, a skeleton with high attack and low defense will have lower early_section difficulty and higher late-section difficulty, such as[15,5]'
'and high defense guard may have extremely high early_section difficulty and low late_section one, such as[99,8]'
'difficulty will only be measured within a setion, meaning that all sections will have a similar difficulty'

'award is also measured in two ways, health/defense and attack'

'difficulty of a floor is measured by two index between 0 and 10'
'pass difficulty is calculated by an unknown algorithm taking into account the difficulty and award on the main/side route'
'end section difficulty is calculated based on difficulty/award in the award_area of the floor'

def section_design(section_size):
    'return the difficulty of each floor using different designs'
    'pass-difficulty-design includes standard, less_standard, half-half'
    result=[0]*section_size
    design_index=random.randint(0,2)
    if design_index==0:
        design='standard'
        for i in range(section_size):
            result[i]=i/(size/10)
    if design_index==1:
        design='less standard'
        for i in range(section_size):
            result[i]=(i/size*2)**2*2.5
    if design_index==2:
        design='half-half'
        for i in range(int(0.5*section_size)):
            result[i]=i/size*9
        for i in range(int(0.5*section_size),section_size):
            result[1]=10-(section_size-i)/section_size*9

    
    return result

def fluctuate(section):
