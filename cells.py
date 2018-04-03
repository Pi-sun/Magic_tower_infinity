from kivy.clock import Clock

from textures import *

def animate(texture, keyframes, completion = None):
	for i in range(len(keyframes)):
		def work(i):
			texture.reload(*keyframes[i])
			if i == len(keyframes) - 1 and completion:
				completion()
		def createWork(i):
			return lambda dt: work(i)
		Clock.schedule_once(createWork(i), 0.1 * i)

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

KEYS = [KEY_YELLOW, KEY_BLUE, KEY_RED]

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
		if app.hero.keys[self.key] > 0:
			app.hero.updateKey(self.key, -1)
			
			app.blockActions()
		
			def clearBlock():
				app.setCell(Empty(), self.location)
				app.unblockActions()
			animate(self.texture, [(DOOR_TEXTURE_ROWS[self.key], i) for i in range(4)] + [(-1, -1)], clearBlock)
		
class Stair(Cell):
	def __init__(self, texture, direction):
		super().__init__(texture)
		self.direction = direction
		
	def interact(self, app):
		app.hero.moveBy(self.location - app.hero.location)
		
		app.blockActions()
		
		def clearBlock(dt):
			app.moveByFloors(self.direction)
			app.unblockActions()
		Clock.schedule_once(clearBlock, 0.2)
		
class Upstair(Stair):
	def __init__(self):
		super().__init__(SingleTexture(17, 2), 1)
		
class Downstair(Stair):
	def __init__(self):
		super().__init__(SingleTexture(17, 3), -1)
		
class Monster(Cell):
	def __init__(self, health, attack, defence, texture):
		super().__init__(texture)
		
		self.health = health
		self.attack = attack
		self.defence = defence
		
	def interact(self, app):
		heroDamage = max(app.hero.attack.value - self.defence, 0)
		heroStrikes = -1 if heroDamage == 0 else self.health // heroDamage + (self.health % heroDamage > 0)
		
		monsterDamage = max(self.attack - app.hero.defence.value, 0)
		monsterStrikes = -1 if monsterDamage == 0 else app.hero.health.value // monsterDamage + (app.hero.health.value % monsterDamage > 0)
		
		if heroStrikes != -1 and (monsterStrikes == -1 or monsterStrikes >= heroStrikes):
			app.hero.moveBy(self.location - app.hero.location)
			
			app.blockActions()
			
			for i in range(heroStrikes):
				def strike(i):
					app.showSpark()
					Clock.schedule_once(lambda dt: app.hideSpark(), 0.15)
					if i != heroStrikes - 1:
						app.hero.health.update(-monsterDamage)
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
		
class Key(PropertyImprover):
	def __init__(self, key):
		super().__init__(SingleTexture(*KEY_TEXTURES[key]))
		self.key = key
		
	def interact(self, app):
		app.hero.updateKey(self.key, 1)
		super().interact(app)
		
class AttackCrystal(PropertyImprover):
	def __init__(self, quantity):
		super().__init__(SingleTexture(11, 2))
		self.quantity = quantity
		
	def interact(self, app):
		app.hero.attack.update(self.quantity)
		super().interact(app)
		
class DefenceCrystal(PropertyImprover):
	def __init__(self, quantity):
		super().__init__(SingleTexture(11, 3))
		self.quantity = quantity
		
	def interact(self, app):
		app.hero.defence.update(self.quantity)
		super().interact(app)
		
class SmallHealthPotion(PropertyImprover):
	def __init__(self, quantity):
		super().__init__(SingleTexture(11, 0))
		self.quantity = quantity
		
	def interact(self, app):
		app.hero.health.update(self.quantity)
		super().interact(app)
		
class LargeHealthPotion(PropertyImprover):
	def __init__(self, quantity):
		super().__init__(SingleTexture(11, 1))
		self.quantity = quantity
		
	def interact(self, app):
		app.hero.health.update(self.quantity)
		super().interact(app)
