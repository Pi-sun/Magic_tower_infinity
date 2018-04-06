import mt_cells
def monster_data_trans(monster,section):
    standard_attack=10+section*25*(section-1)/2
    standard_defence=standard_attack

    a=(monster.origin)
    origin_index=a*(a-1)/2
    origin_attack=origin_index*25+10
    ratio=standard_attack/origin_attack


    monster.attack=(standard_attack+(monster.attack-origin_attack)/ratio)*1.02**((section-monster.origin)/5)
    monster.defence=(standard_defence+(monster.defence-origin_attack)/ratio)*1.02**((section-monster.origin)/5)
    monster.health*=(ratio)*1.02**((section-monster.origin)/5)
    return monster
GreenSlimeB = mt_cells.monsters._monsterTypeCreator("Green Slime B", (7, 4))
print(monster_data_trans(GreenSlimeB(50,10,10,4),6).attack)
