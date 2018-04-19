from mt_cells import *

class _MonsterCreator:
    def __init__(self, cls, baseHealth, baseAttack, baseDefence, baseMoney, baseSection, earlyDifficulty = None, endDifficulty = None):
        def create(section):
            origin_attack=10+baseSection*(baseSection-1)/2*25
            ratio=section/baseSection
            power=(section-baseSection)//5
            standard_attack=(10+section*(section-1)/2*25)*1.03**power
            actual_health=round(baseHealth*ratio)
            actual_attack=round(standard_attack+(baseAttack-origin_attack)*ratio)
            actual_defence=round(standard_attack+(baseDefence-origin_attack)*ratio)
            actual_money=round(baseMoney*8**power)
            return cls(actual_health, actual_attack, actual_defence, actual_money)
    
        self.__create = create
        self.early_difficulty = earlyDifficulty
        self.end_difficulty = endDifficulty
    
    def __call__(self, section):
        return self.__create(section)

    def difficulty(self,level):
        return (self.early_difficulty*(1-0.03*level)+self.end_difficulty*0.03*level,self.early_difficulty*(1-0.06*level)+self.end_difficulty*0.06*level)

# difficulty in main/side route on xth floor in a section is calculated as such:
# early_difficulty*(1-0.3*x)+end_difficulty*(0.3*x)

# difficulty in award area on xth floor in a section is calculated as such
# early_difficulty*(1-0.6x)+end_difficulty*0.6x

monsters = [
    [ # section 1
        _MonsterCreator(GreenSlimeB,35,18,1,8,1,1,0),
        _MonsterCreator(RedSlimeB,45,20,2,9,1,2,1),
        _MonsterCreator(Bat,35,38,3,13,1,3,3),
        _MonsterCreator(Priest,60,32,8,22,1,6,4),
        _MonsterCreator(SnowmanC,80,32,12,27,1,7,6),
        _MonsterCreator(SkeletonC,50,42,6,24,1,5,5),
        _MonsterCreator(SkeletonB,55,52,12,32,1,7,8),
        _MonsterCreator(GateKeeperC,50,48,22,42,1,10,8),
    ],
    [ # section 2
        _MonsterCreator(BigSlime,130,60,3,20,2,1,1),
        _MonsterCreator(SnowmanB,170,94,40,48,2,9,7),
        _MonsterCreator(BigBat,60,100,8,24,2,2,2),
        _MonsterCreator(SuperionPriest,100,95,30,33,2,5,4),
        _MonsterCreator(Zombie,260,90,5,38,2,4,6),
        _MonsterCreator(RockHead,20,100,68,40,2,10,3),
        _MonsterCreator(ZombieKnight,320,120,15,50,2,7,8),
    ],
    [ # section 3
        _MonsterCreator(SlimeMan,320,120,20,35,3,2,1),
        _MonsterCreator(GhostSoldier,210,150,30,40,3,3,3),
        _MonsterCreator(SandMan,400,180,10,50,3,5,6),
        _MonsterCreator(Soldier,200,190,55,49,3,5,5),
        _MonsterCreator(GateKeeperB,100,180,110,57,3,8,6),
        _MonsterCreator(SwordsmanB,90,680,50,60,3,7,4),
        _MonsterCreator(KnightB,180,210,100,75,3,9,8),
    ],
    [ # section 4
        _MonsterCreator(GreenSlimeA,320,270,10,52,4,1,2),
        _MonsterCreator(VampireBatB,190,360,80,58,4,2,2),
        _MonsterCreator(MagicianB,210,350,100,78,4,4,3),
        _MonsterCreator(MagicianA,250,370,110,92,4,6,5),
        _MonsterCreator(MagicSergeantB,230,440,75,95,4,5,6),
        _MonsterCreator(DarkKnightB,180,410,190,110,4,8,7),
        _MonsterCreator(GateKeeperA,160,380,230,160,4,10,9),
    ],
    [ # section 5
        _MonsterCreator(RedSlimeA,550,310,100,90,5,1,0),
        _MonsterCreator(Slimelord,500,360,140,100,5,3,2),
        _MonsterCreator(DarkPriest,250,420,200,110,5,5,4),
        _MonsterCreator(KnightA,400,400,210,125,5,6,4),
        _MonsterCreator(SmokeMan,480,450,165,133,5,5,5),
        _MonsterCreator(FireBat,300,600,70,130,5,3,5),
        _MonsterCreator(IceZombie,1000,560,60,152,5,7,8),
        _MonsterCreator(IronHead,100,500,350,180,5,10,8),
    ],
]

bosses = [
    _MonsterCreator(SkeletonA,100,65,15,100,1),
    _MonsterCreator(Vampire,444,199,66,216,2),
    _MonsterCreator(KnightC,165,300,10,500,3),
    _MonsterCreator(MagicMaster,800,420,200,233,4),
    _MonsterCreator(Devil,2500,800,100,500,5),
]

def monsters_for(section):
    return monsters[section % len(monsters) - 1]

def boss_for(section):
    return bosses[section % len(bosses) - 1]
