from kivy.clock import Clock

from textures import *

class Point:
	def __init__(self, row, col):
		self.row = row
		self.col = col
		
	def __eq__(self, other):
		return self.row == other.row and self.col == other.col
		
	def __add__(self, other):
		return Point(self.row + other.row, self.col + other.col)
		
	def __sub__(self, other):
		return Point(self.row - other.row, self.col - other.col)

KEY_YELLOW = "yellow"
KEY_BLUE = "blue"
KEY_RED = "red"

KEY_TEXTURES = {
	KEY_YELLOW: (10, 0),
	KEY_BLUE: (10, 1),
	KEY_RED: (10, 2)
}

DOOR_TEXTURE_ROWS = {
	KEY_YELLOW: 4,
	KEY_BLUE: 5,
	KEY_RED: 6
}

class Cell:
	def __init__(self, texture):
		self.texture = texture
		
	def initialize(self, location, display):
		self.location = location
		self.texture.initialize(display)
		
	def update(self):
		self.texture.update()
		
	def interact(self, app):
		raise NotImplementedError()
		
class Empty(Cell):
	def __init__(self):
		super().__init__(SingleTexture(-1, -1))
	
	def interact(self, app):
		app.hero.moveBy(self.location - app.hero.location)
		
class Impassable(Cell):
	def __init__(self, texture):
		super().__init__(texture)
	
	def interact(self, app):
		pass
		
class Wall(Impassable):
	def __init__(self):
		super().__init__(SingleTexture(8, 0))
		
class KeyedDoor(Cell):
	def __init__(self, key):
		super().__init__(SingleTexture(DOOR_TEXTURE_ROWS[key], 0))
		self.key = key
		
	def interact(self, app):
		pass
		
class Monster(Cell):
	def __init__(self, health, attack, defence, texture):
		super().__init__(texture)
		
		self.health = health
		self.attack = attack
		self.defence = defence
		
	def interact(self, app):
		heroDamage = max(app.hero.attack - self.defence, 0)
		heroStrikes = -1 if heroDamage == 0 else self.health // heroDamage + (self.health % heroDamage > 0)
		
		monsterDamage = max(self.attack - app.hero.defence, 0)
		monsterStrikes = -1 if monsterDamage == 0 else app.hero.health // monsterDamage + (app.hero.health % monsterDamage > 0)
		
		if heroStrikes != -1 and (monsterStrikes == -1 or monsterStrikes >= heroStrikes):
			app.hero.moveBy(self.location - app.hero.location)
			
			app.blockActions()
			
			for i in range(heroStrikes):
				def strike(i):
					app.showSpark()
					Clock.schedule_once(lambda dt: app.hideSpark(), 0.15)
					if i != heroStrikes - 1:
						app.hero.updateHealth(-monsterDamage)
				def createStrike(i):
					return lambda dt: strike(i)
				Clock.schedule_once(createStrike(i), 0.3 * i + 0.15)
				
			def clearBlock(dt):
				app.setCell(Empty(), self.location)
				app.unblockActions()
			Clock.schedule_once(clearBlock, 0.3 * heroStrikes)
		
class GreenSlime(Monster):
	def __init__(self):
		super().__init__(20, 15, 5, FourTexture(0, 4))
		
class SlimeKing(Monster):
	def __init__(self):
		super().__init__(20, 100, 0, FourTexture(3, 4))

class PropertyImprover(Cell):
	def __init__(self, texture):
		super().__init__(texture)
		
	def interact(self, app):
		app.hero.moveBy(self.location - app.hero.location)
		app.setCell(Empty(), self.location)
		
class AttackCrystal(PropertyImprover):
	def __init__(self, quantity):
		super().__init__(SingleTexture(11, 2))
		self.quantity = quantity
		
	def interact(self, app):
		app.hero.updateAttack(self.quantity)
		super().interact(app)
		
class DefenceCrystal(PropertyImprover):
	def __init__(self, quantity):
		super().__init__(SingleTexture(11, 3))
		self.quantity = quantity
		
	def interact(self, app):
		app.hero.updateDefence(self.quantity)
		super().interact(app)
		
class SmallHealthPotion(PropertyImprover):
	def __init__(self, quantity):
		super().__init__(SingleTexture(11, 0))
		self.quantity = quantity
		
	def interact(self, app):
		app.hero.updateHealth(self.quantity)
		super().interact(app)
