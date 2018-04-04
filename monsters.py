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
			
GreenSlime = monsterTypeCreator("Green Slime", (0, 4))
RedSlime = monsterTypeCreator("Red Slime", (1, 4))
BigSlime = monsterTypeCreator("Big Slime", (2, 4))
Slimelord = monsterTypeCreator("Slimelord", (3, 4))
SkeletonC = monsterTypeCreator("Skeleton C", (4, 4))
SkeletonB = monsterTypeCreator("Skeleton B", (5, 4))
SkeletonA = monsterTypeCreator("Skeleton A", (6, 4))
GhostSoldier = monsterTypeCreator("Ghost Soldier", (7, 4))
Bat = monsterTypeCreator("Bat", (0, 8))
BigBat = monsterTypeCreator("Big Bat", (1, 8))
VampireBat = monsterTypeCreator("Vampire Bat", (2, 8)) 
Vampire = monsterTypeCreator("Vampire", (3, 8))
Swordsman = monsterTypeCreator("Swordsman", (4, 8)) 
GateKeeperC = monsterTypeCreator("Gate-Keeper C", (5, 8))
GateKeeperB = monsterTypeCreator("Gate-Keeper B", (6, 8))
GateKeeperA = monsterTypeCreator("Gate-Keeper A", (7, 8)) 
Priest = monsterTypeCreator("Priest", (8, 8))
SuperionPriest = monsterTypeCreator("Superion Priest", (9, 8))
MagicianB = monsterTypeCreator("Magician B", (10, 8)) 
MagicianA = monsterTypeCreator("Magician A", (0, 12))
GoldenKnight = monsterTypeCreator("Golden Knight", (1, 12))
Knight = monsterTypeCreator("Knight", (2, 12))
MagicSergeant = monsterTypeCreator("Magic Sergeant", (3, 12)) 
Zeno = monsterTypeCreator("Zeno", (4, 12)) 
Zombie = monsterTypeCreator("Zombie", (5, 12))
ZombieKnight = monsterTypeCreator("Zombie Knight", (6, 12))
Rock = monsterTypeCreator("Rock", (7, 12))
SlimeMan = monsterTypeCreator("Slime Man", (8, 12))

# Not found in the current texture atlas:
# Soldier
# Dark Knight
