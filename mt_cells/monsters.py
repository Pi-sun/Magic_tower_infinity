from kivy.clock import Clock

from . import Cell, Empty
from mt_core.textures import *

class Monster(Cell):
	def __init__(self, name, health, attack, defence, money, texture, menu_texture = None):
		super().__init__(texture)

		self.name = name
		self.health = health
		self.attack = attack
		self.defence = defence
		self.money = money
		if menu_texture:
			self.menu_texture = menu_texture
		else:
			self.menu_texture = texture
		
	def interact(self, app):
		self.combat(app, self.location)
	
	# testing
	def interactAround(self, app):
		print("Around %s" % self.name)
	
	def combat(self, app, attack_location):
		print("Attacking %s <%d, %d, %d, %d>" % (self.name, self.health, self.attack, self.defence, self.money))
		
		heroDamage = max(app.hero.attack.value - self.defence, 0)
		heroStrikes = -1 if heroDamage == 0 else self.health // heroDamage + (self.health % heroDamage > 0)
		
		monsterDamage = max(self.attack - app.hero.defence.value, 0)
		monsterStrikes = -1 if monsterDamage == 0 else app.hero.health.value // monsterDamage + (app.hero.health.value % monsterDamage > 0)
		
		if heroStrikes != -1 and (monsterStrikes == -1 or monsterStrikes >= heroStrikes):
			app.hero.moveBy(attack_location - app.hero.location)
			
			app.blockActions()
			app.showMonster(self)
			
			i = 0
			def strike(dt):
				app.showSpark()
				self.health = max(self.health - heroDamage, 0)
				app.updateMonsterHealth(self.health)
				
				def hide(dt):
					nonlocal i
					
					app.hideSpark()
					if i == heroStrikes - 1:
						def clearBlock(dt):
							app.hero.money.update(self.money)
							app.showMonster(None)
							app.unblockActions()
							self.finish(app)
						Clock.schedule_once(clearBlock, 0.15)
					else:
						app.hero.health.update(-monsterDamage)
						i += 1
						Clock.schedule_once(strike, 0.15)
				Clock.schedule_once(hide, 0.15)
			Clock.schedule_once(strike, 0.15)
			
	def finish(self, app):
		app.setCell(Empty(), self.location, self.floor)
			
class LargeMonster(Monster):
	def __init__(self, name, health, attack, defence, money, texture, menu_texture, parts):
			super().__init__(name, health, attack, defence, money, texture, menu_texture)
			self.parts = parts
			
	def finish(self, app):
		for part in self.parts:
			app.setCell(self.parts[part], self.location + part, self.floor)
			
class LargeMonsterPart(Cell):
	def __init__(self, texture, offset):
		super().__init__(texture)
		
		self.offset = offset

	def interact(self, app):
		app.getCell(self.location + self.offset, self.floor).combat(app, self.location)
			
def _monsterTypeCreator(name, textureCoordinate):
	return lambda health, attack, defence, money: Monster(name, health, attack, defence, money, FourTexture(*textureCoordinate))
			
def _monster3x3TypeCreator(name, textureCoordinate, menuTextureCoordinate = None):
	def create(health, attack, defence, money, gifts = {}):
		parts = {Point(i, j): gifts[(i, j)] if (i, j) in gifts else Empty() for i in range(-1, 2) for j in range(-1, 2)}
		results = []
		for i in range(-1, 2):
			row = []
			for j in range(-1, 2):
				texture = FourTexture(textureCoordinate[0] + i, textureCoordinate[1] + j, 3)
				if i == 0 and j == 0:
					row.append(LargeMonster(name, health, attack, defence, money, texture, FourTexture(*menuTextureCoordinate), parts))
				else:
					row.append(LargeMonsterPart(texture, Point(-i, -j)))
			results.append(row)
		return results
	return create
			
GreenSlimeB = _monsterTypeCreator("Green Slime B", (7, 4))
GreenSlimeA = _monsterTypeCreator("Green Slime A", (8, 4))
RedSlimeB = _monsterTypeCreator("Red Slime B", (9, 4))
RedSlimeA = _monsterTypeCreator("Red Slime A", (10, 4))
BigSlime = _monsterTypeCreator("Big Slime", (11, 4))
Slimelord = _monsterTypeCreator("Slimelord", (12, 4))
BlastSlime = _monsterTypeCreator("Blast Slime", (13, 4))
BombSlime = _monsterTypeCreator("Bomb Slime", (14, 4))
SkeletonC = _monsterTypeCreator("Skeleton C", (15, 4))
SkeletonB = _monsterTypeCreator("Skeleton B", (16, 4))
SkeletonA = _monsterTypeCreator("Skeleton A", (17, 4))
Soldier = _monsterTypeCreator("Soldier", (18, 4))
SwordSoldier = _monsterTypeCreator("Sword Soldier", (19, 4))
GhostSoldier = _monsterTypeCreator("Ghost Soldier", (20, 4))
DarkSoldier = _monsterTypeCreator("Dark Soldier", (21, 4))
GateKeeperC = _monsterTypeCreator("Gate-Keeper C", (22, 4))
GateKeeperB = _monsterTypeCreator("Gate-Keeper B", (23, 4))
GateKeeperA = _monsterTypeCreator("Gate-Keeper A", (24, 4))
Bat = _monsterTypeCreator("Bat", (7, 8))
FireBat = _monsterTypeCreator("Fire Bat", (8, 8))
DarkBat = _monsterTypeCreator("Dark Bat", (9, 8))
BigBat = _monsterTypeCreator("Big Bat", (10, 8))
VampireBatB = _monsterTypeCreator("Vampire Bat B", (11, 8))
VampireBatA = _monsterTypeCreator("Vampire Bat A", (12, 8))
Vampire = _monsterTypeCreator("Vampire", (13, 8))
Priest = _monsterTypeCreator("Priest", (14, 8))
SuperionPriest = _monsterTypeCreator("Superion Priest", (15, 8))
DarkPriest = _monsterTypeCreator("Dark Priest", (16, 8))
MagicianB = _monsterTypeCreator("Magician B", (17, 8))
MagicianA = _monsterTypeCreator("Magician A", (18, 8))
SwordsmanB = _monsterTypeCreator("Swordsman B", (19, 8))
SwordsmanA = _monsterTypeCreator("Swordsman A", (20, 8))
DarkSwordsman = _monsterTypeCreator("Dark Swordsman", (21, 8))
RockHead = _monsterTypeCreator("Rock-Head", (22, 8))
IronHead = _monsterTypeCreator("Iron-Head", (23, 8))
DiamondHead = _monsterTypeCreator("Diamond-Head", (24, 8))
KnightC = _monsterTypeCreator("Knight C", (7, 12))
KnightB = _monsterTypeCreator("Knight B", (8, 12))
KnightA = _monsterTypeCreator("Knight A", (9, 12))
DarkKnightB = _monsterTypeCreator("Dark Knight B", (10, 12))
DarkKnightA = _monsterTypeCreator("Dark Knight A", (11, 12))
SlimeMan = _monsterTypeCreator("Slime Man", (12, 12))
SmokeMan = _monsterTypeCreator("Smoke Man", (13, 12))
SandMan = _monsterTypeCreator("Sand Man", (14, 12))
SnowmanC = _monsterTypeCreator("Snowman C", (15, 12))
SnowmanB = _monsterTypeCreator("Snowman B", (16, 12))
SnowmanA = _monsterTypeCreator("Snowman A", (17, 12))
Zombie = _monsterTypeCreator("Zombie", (18, 12))
ZombieKnight = _monsterTypeCreator("Zombie Knight", (19, 12))
IceZombie = _monsterTypeCreator("Ice Zombie", (20, 12))
MagicSergeantB = _monsterTypeCreator("Magic Sergeant B", (21, 12))
MagicSergeantA = _monsterTypeCreator("Magic Sergeant A", (22, 12))
Devil = _monsterTypeCreator("Devil", (23, 12))
MagicMaster = _monsterTypeCreator("Magic Master", (24, 12))

Dragon = _monster3x3TypeCreator("Dragon", (0, 4), (0, 16))
GiantOctopus = _monster3x3TypeCreator("Giant Octopus", (3, 4), (1, 16))
