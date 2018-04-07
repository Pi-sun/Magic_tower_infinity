import mt_cells as mons

def _monster_creator(cls, baseHealth, baseAttack, baseDefence, baseMoney, baseSection):
	def create(section):
		standard_attack=10+section*25*(section-1)/2
		standard_defence=standard_attack

		origin_index=baseSection*(baseSection-1)/2
		origin_attack=origin_index*25+10
		ratio=standard_attack/origin_attack

		actual_health=int(round(baseHealth*(ratio)*1.02**((section-baseSection)/5)))
		actual_attack=int(round((standard_attack+(baseAttack-origin_attack)/ratio)*1.02**((section-baseSection)/5)))
		actual_defence=int(round((standard_defence+(baseDefence-origin_attack)/ratio)*1.02**((section-baseSection)/5)))
		actual_money=int(round(baseMoney*8**((section-baseSection)/5)))))# TODO: calculate monster money increment
		return cls(actual_health, actual_attack, actual_defence, actual_money)
	return create

#difficulty in main/side route on xth floor in a section is calculated as such:
# early_difficulty*(1-0.3*x)+end_difficulty*(0.3*x)

# difficulty in award area on xth floor in a section is calculated as such
# early_difficulty*(1-0.6x)+end_difficulty*0.6x

GreenSlimeB = _monster_creator(mons.GreenSlimeB,35,18,1,1,1)
RedSlimeB = _monster_creator(mons.RedSlimeB,45,20,2,2,1)
Bat = _monster_creator(mons.Bat,35,38,3,3,1)
Priest = _monster_creator(mons.Priest,60,32,8,5,1)
SkeletonC = _monster_creator(mons.SkeletonC,50,42,6,6,1)
SkeletonB = _monster_creator(mons.SkeletonB,55,52,12,8,1)
GateKeeperC = _monster_creator(mons.GateKeeperC,50,48,22,12,1)
SkeletonA = _monster_creator(mons.SkeletonA,100,65,15,30,1)
BigSlime = _monster_creator(mons.BigSlime,130,60,3,8,2)
BigBat = _monster_creator(mons.BigBat,60,100,8,12,2)
SuperionPriest = _monster_creator(mons.SuperionPriest,100,95,30,18,2)
Zombie = _monster_creator(mons.Zombie,260,85,5,22,2)
RockHead = _monster_creator(mons.RockHead,20,100,68,28,2)
ZombieKnight = _monster_creator(mons.ZombieKnight,320,120,15,30,2)
Vampire = _monster_creator(mons.Vampire,444,199,66,144,2)
SlimeMan = _monster_creator(mons.SlimeMan,320,120,20,30,3)
GhostSoldier = _monster_creator(mons.GhostSoldier,210,150,30,35,3)
Soldier = _monster_creator(mons.Soldier,200,190,55,45,3)
GateKeeperB = _monster_creator(mons.GateKeeperB,100,180,110,50,3)
SwordsmanB = _monster_creator(mons.SwordsmanB,90,680,50,55,3)
KnightB = _monster_creator(mons.KnightB,180,210,100,65,3)
Slimelord = _monster_creator(mons.Slimelord,320,270,10,40,4)
VampireBatB = _monster_creator(mons.VampireBatB,190,360,80,50,4)
MagicianB = _monster_creator(mons.MagicianB,210,350,100,80,4)
MagicianA = _monster_creator(mons.MagicianA,190,370,120,90,4)
MagicSergeantB = _monster_creator(mons.MagicSergeantB,230,440,75,100,4)
DarkKnightB = _monster_creator(mons.DarkKnightB,180,410,190,120,4)
GateKeeperA = _monster_creator(mons.GateKeeperA,160,390,230,170,4)
GreenSlimeA = _monster_creator(mons.GreenSlimeA,550,330,120,120,5)
RedSlimeA = _monster_creator(mons.RedSlimeA,500,360,140,140,5)
DarkPriest = _monster_creator(mons.DarkPriest,250,420,200,180,5)
KnightA = _monster_creator(mons.KnightA,400,400,210,190,5)
SmokeMan = _monster_creator(mons.SmokeMan,480,450,165,190,5)
FireBat = _monster_creator(mons.FireBat,300,600,70,195,5)
IceZombie = _monster_creator(mons.IceZombie,1000,560,60,220,5)
IronHead = _monster_creator(mons.IronHead,100,500,350,240,5)
