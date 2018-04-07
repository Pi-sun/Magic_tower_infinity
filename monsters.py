from mt_cells import *

def _monster_creator(cls, baseHealth, baseAttack, baseDefence, baseMoney, baseSection):
    def create(section):
        standard_attack=10+section*25*(section-1)//2
        
        origin_index=baseSection*(baseSection-1)//2
        origin_attack=origin_index*25+10
        ratio=standard_attack/origin_attack
        
        power=(section-baseSection)/5

        actual_health=round(baseHealth*(ratio)*1.05**power)
        actual_attack=round((standard_attack+(baseAttack-origin_attack)/ratio)*1.05**power)
        actual_defence=round((standard_attack+(baseDefence-origin_attack)/ratio)*1.05**power)
        actual_money=round(baseMoney*8**power)
        return cls(actual_health, actual_attack, actual_defence, actual_money)
    return create

# difficulty in main/side route on xth floor in a section is calculated as such:
# early_difficulty*(1-0.3*x)+end_difficulty*(0.3*x)

# difficulty in award area on xth floor in a section is calculated as such
# early_difficulty*(1-0.6x)+end_difficulty*0.6x

monsters = [
	{ # section 1
		(1,1): _monster_creator(GreenSlimeB,35,18,1,8,1),
		(2,1): _monster_creator(RedSlimeB,45,20,2,9,1),
		(2,2): _monster_creator(Bat,35,38,3,13,1),
		(5,3): _monster_creator(Priest,60,32,8,22,1),
		(4,4): _monster_creator(SkeletonC,50,42,6,24,1),
		(6,7): _monster_creator(SkeletonB,55,52,12,32,1),
		(10,8): _monster_creator(GateKeeperC,50,48,22,42,1),
	},
	{ # section 2
		(1,1): _monster_creator(BigSlime,130,60,3,20,2),
		(2,2): _monster_creator(BigBat,60,100,8,24,2),
		(5,4): _monster_creator(SuperionPriest,100,95,30,33,2),
		(4,6): _monster_creator(Zombie,260,85,5,38,2),
		(10,3): _monster_creator(RockHead,20,100,68,40,2),
		(7,8): _monster_creator(ZombieKnight,320,120,15,50,2),
	},
	{ # section 3
		(2,2): _monster_creator(SlimeMan,320,120,20,35,3),
		(3,3): _monster_creator(GhostSoldier,210,150,30,40,3),
		(5,5): _monster_creator(Soldier,200,190,55,49,3),
		(8,6): _monster_creator(GateKeeperB,100,180,110,57,3),
		(7,4): _monster_creator(SwordsmanB,90,680,50,60,3),
		(9,8): _monster_creator(KnightB,180,210,100,75,3),
	},
	{ # section 4
		(1,2): _monster_creator(GreenSlimeA,320,270,10,52,4),
		(2,2): _monster_creator(VampireBatB,190,360,80,58,4),
		(4,3): _monster_creator(MagicianB,210,350,100,78,4),
		(6,5): _monster_creator(MagicianA,190,370,120,92,4),
		(5,6): _monster_creator(MagicSergeantB,230,440,75,95,4),
		(8,7): _monster_creator(DarkKnightB,180,410,190,110,4),
		(10,9): _monster_creator(GateKeeperA,160,380,230,160,4),
	},
	{ # section 5
		(1,1): _monster_creator(RedSlimeA,550,310,100,90,5),
		(3,2): _monster_creator(Slimelord,500,360,140,100,5),
		(5,4): _monster_creator(DarkPriest,250,420,200,110,5),
		(6,4): _monster_creator(KnightA,400,400,210,125,5),
		(5,5): _monster_creator(SmokeMan,480,450,165,133,5),
		(3,5): _monster_creator(FireBat,300,600,70,130,5),
		(7,8): _monster_creator(IceZombie,1000,560,60,152,5),
		(10,8): _monster_creator(IronHead,100,500,350,180,5),
	},
]

def monsters_for(section):
	return monsters[section % len(monsters) - 1]
