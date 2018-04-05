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
	KEY_YELLOW: (18, 0),
	KEY_BLUE: (18, 1),
	KEY_RED: (18, 2)
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
		if app.hero.keys[self.key].value > 0:
			app.hero.keys[self.key].update(-1)
			
			app.blockActions()
		
			def clearBlock():
				app.setCell(Empty(), self.location)
				app.unblockActions()
			animate(self.texture, [(DOOR_TEXTURE_ROWS[self.key], i) for i in range(4)] + [EMPTY_TEXTURE], clearBlock)
		
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
		super().__init__(SingleTexture(24, 2), 1)
		
class Downstair(Stair):
	def __init__(self):
		super().__init__(SingleTexture(24, 3), -1)
		
class PropertyImprover(Cell):
	def __init__(self, texture, property, quantity):
		super().__init__(texture)
		self.property = property
		self.quantity = quantity
		
	def interact(self, app):
		self.property(app.hero).update(self.quantity)
		app.hero.moveBy(self.location - app.hero.location)
		app.setCell(Empty(), self.location)
		
class Key(PropertyImprover):
	def __init__(self, key):
		super().__init__(SingleTexture(*KEY_TEXTURES[key]), lambda hero: hero.keys[key], 1)
		
class SmallHealthPotion(PropertyImprover):
	def __init__(self, quantity):
		super().__init__(SingleTexture(16, 0), lambda hero: hero.health, quantity)
		
class LargeHealthPotion(PropertyImprover):
	def __init__(self, quantity):
		super().__init__(SingleTexture(16, 1), lambda hero: hero.health, quantity)
		
class AttackCrystal(PropertyImprover):
	def __init__(self, quantity):
		super().__init__(SingleTexture(18, 3), lambda hero: hero.attack, quantity)
		
class DefenceCrystal(PropertyImprover):
	def __init__(self, quantity):
		super().__init__(SingleTexture(19, 3), lambda hero: hero.defence, quantity)

class Shop(Cell):
	def __init__(self):
		super().__init__(FourTexture(6, 5, 3))
	
	def interact(self, app):
		if app.hero.location - self.location == Point(1, 0):
			print("Shopping!") # TODO: Add shop interactions
		
class ShopLeft(Impassable):
	def __init__(self):
		super().__init__(FourTexture(6, 4, 3))

class ShopRight(Impassable):
	def __init__(self):
		super().__init__(FourTexture(6, 6, 3))
