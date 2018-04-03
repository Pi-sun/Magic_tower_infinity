import generator

'difficulty is a two_dimensional vector measuring roughly how many damage the monster can do to hero in the early and later part of the section'
'for example, a mage with average attack and defense will have a balance difficulty of [10,10]'
'on the other hand, a skeleton with high attack and low defense will have lower early_section difficulty and higher late-section difficulty, such as[15,5]'
'and high defense guard may have extremely high early_section difficulty and low late_section one, such as[99,8]'
'difficulty will only be measured within a setion, meaning that all sections will have a similar difficulty'

