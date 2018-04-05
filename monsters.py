from kivy.clock import Clock

from cells import Cell, Empty
from textures import *

class Monster(Cell):
	def __init__(self, name, health, attack, defence, money, texture):
		super().__init__(texture)
		
		self.name = name
		self.health = health
		self.attack = attack
		self.defence = defence
		self.money = money
		
	def interact(self, app):
		heroDamage = max(app.hero.attack.value - self.defence, 0)
		heroStrikes = -1 if heroDamage == 0 else self.health // heroDamage + (self.health % heroDamage > 0)
		
		monsterDamage = max(self.attack - app.hero.defence.value, 0)
		monsterStrikes = -1 if monsterDamage == 0 else app.hero.health.value // monsterDamage + (app.hero.health.value % monsterDamage > 0)
		
		if heroStrikes != -1 and (monsterStrikes == -1 or monsterStrikes >= heroStrikes):
			app.hero.moveBy(self.location - app.hero.location)
			
			app.blockActions()
			app.showMonster(self)
			
			for i in range(heroStrikes):
				def strike(i):
					app.showSpark()
					self.health -= heroDamage
					app.updateMonsterHealth(self.health)
					
					def hide(dt):
						app.hideSpark()
						if i != heroStrikes - 1:
							app.hero.health.update(-monsterDamage)
					Clock.schedule_once(hide, 0.15)
				def createStrike(i):
					return lambda dt: strike(i)
				Clock.schedule_once(createStrike(i), 0.3 * i + 0.15)
				
			def clearBlock(dt):
				app.hero.money.update(self.money)
				app.setCell(Empty(), self.location)
				app.showMonster(None)
				app.unblockActions()
			Clock.schedule_once(clearBlock, 0.3 * heroStrikes)
			
def monsterTypeCreator(name, textureCoordinate):
	return lambda health, attack, defence, money: Monster(name, health, attack, defence, money, FourTexture(*textureCoordinate))
			
GreenSlimeB = monsterTypeCreator("Green Slime B", (7, 4))
GreenSlimeA = monsterTypeCreator("Green Slime A", (8, 4))
RedSlimeB = monsterTypeCreator("Red Slime B", (9, 4))
RedSlimeA = monsterTypeCreator("Red Slime A", (10, 4))
BigSlime = monsterTypeCreator("Big Slime", (11, 4))
Slimelord = monsterTypeCreator("Slimelord", (12, 4))
BlastSlime = monsterTypeCreator("Blast Slime", (13, 4))
BombSlime = monsterTypeCreator("Bomb Slime", (14, 4))
SkeletonC = monsterTypeCreator("Skeleton C", (15, 4))
SkeletonB = monsterTypeCreator("Skeleton B", (16, 4))
SkeletonA = monsterTypeCreator("Skeleton A", (17, 4))
Soldier = monsterTypeCreator("Soldier", (18, 4))
SwordSoldier = monsterTypeCreator("Sword Soldier", (19, 4))
GhostSoldier = monsterTypeCreator("Ghost Soldier", (20, 4))
DarkSoldier = monsterTypeCreator("Dark Soldier", (21, 4))
GateKeeperC = monsterTypeCreator("Gate-Keeper C", (22, 4))
GateKeeperB = monsterTypeCreator("Gate-Keeper B", (23, 4))
GateKeeperA = monsterTypeCreator("Gate-Keeper A", (24, 4))
Bat = monsterTypeCreator("Bat", (7, 8))
FireBat = monsterTypeCreator("Fire Bat", (8, 8))
DarkBat = monsterTypeCreator("Dark Bat", (9, 8))
BigBat = monsterTypeCreator("Big Bat", (10, 8))
VampireBatB = monsterTypeCreator("Vampire Bat B", (11, 8))
VampireBatA = monsterTypeCreator("Vampire Bat A", (12, 8))
Vampire = monsterTypeCreator("Vampire", (13, 8))
Priest = monsterTypeCreator("Priest", (14, 8))
SuperionPriest = monsterTypeCreator("Superion Priest", (15, 8))
DarkPriest = monsterTypeCreator("Dark Priest", (16, 8))
MagicianB = monsterTypeCreator("Magician B", (17, 8))
MagicianA = monsterTypeCreator("Magician A", (18, 8))
SwordsmanB = monsterTypeCreator("Swordsman B", (19, 8))
SwordsmanA = monsterTypeCreator("Swordsman A", (20, 8))
DarkSwordsman = monsterTypeCreator("Dark Swordsman", (21, 8))
RockHead = monsterTypeCreator("Rock-Head", (22, 8))
IronHead = monsterTypeCreator("Iron-Head", (23, 8))
DiamondHead = monsterTypeCreator("Diamond-Head", (24, 8))
KnightC = monsterTypeCreator("Knight C", (7, 12))
KnightB = monsterTypeCreator("Knight B", (8, 12))
KnightA = monsterTypeCreator("Knight A", (9, 12))
DarkKnightB = monsterTypeCreator("Dark Knight B", (10, 12))
DarkKnightA = monsterTypeCreator("Dark Knight A", (11, 12))
SlimeMan = monsterTypeCreator("Slime Man", (12, 12))
SmokeMan = monsterTypeCreator("Smoke Man", (13, 12))
SandMan = monsterTypeCreator("Sand Man", (14, 12))
SnowmanC = monsterTypeCreator("Snowman C", (15, 12))
SnowmanB = monsterTypeCreator("Snowman B", (16, 12))
SnowmanA = monsterTypeCreator("Snowman A", (17, 12))
Zombie = monsterTypeCreator("Zombie", (18, 12))
ZombieKnight = monsterTypeCreator("Zombie Knight", (19, 12))
IceZombie = monsterTypeCreator("Ice Zombie", (20, 12))
MagicSergeantA = monsterTypeCreator("Magic Sergeant A", (21, 12))
MagicSergeantB = monsterTypeCreator("Magic Sergeant B", (22, 12))
Devil = monsterTypeCreator("Devil", (23, 12))
MagicMaster = monsterTypeCreator("Magic Master", (24, 12))
