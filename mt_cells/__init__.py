from kivy.clock import Clock

# Required by initialization of mt_core
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

SWORD_TEXTURES = [(22, 0), (23, 0), (24, 0), (22, 2), (23, 2)]
SHIELD_TEXTURES = [(22, 1), (23, 1), (24, 1), (22, 3), (23, 3)]

from mt_core.textures import *

def _animate(texture, keyframes, completion = None):
	for i in range(len(keyframes)):
		def work(i):
			texture.reload(*keyframes[i])
			if i == len(keyframes) - 1 and completion:
				completion()
		def createWork(i):
			return lambda dt: work(i)
		Clock.schedule_once(createWork(i), 0.08 * i)

class Cell:
	def __init__(self, texture):
		self.texture = texture
		
	def placeAt(self, floor, location):
		self.floor = floor
		self.location = location
		
	def initialize(self, display):
		self.texture.initialize(display)
		
	def update(self):
		self.texture.update()
		
	def interact(self, app):
		raise NotImplementedError()
		
	def interactAround(self, app):
		pass
		
class Empty(Cell):
	def __init__(self):
		super().__init__(SingleTexture(*EMPTY_TEXTURE))
	
	def interact(self, app):
		app.hero.moveBy(self.location - app.hero.location)
		
class Impassable(Cell):
	def interact(self, app):
		pass
		
class Wall(Impassable):
	def __init__(self):
		super().__init__(SingleTexture(8, 0))

class Lava(Impassable):
	def __init__(self):
		super().__init__(FourTexture(10, 0))

class Void(Impassable):
	def __init__(self):
		super().__init__(FourTexture(11, 0))
		
class HiddenWall(Impassable):
	def __init__(self):
		super().__init__(SingleTexture(*EMPTY_TEXTURE))
		self.hidden = True
		
	def interact(self, app):
		if self.hidden:
			app.blockActions()
		
			def clearBlock():
				self.hidden = False
				app.unblockActions()
			_animate(self.texture, [EMPTY_TEXTURE] + [(8, 3 - i) for i in range(4)], clearBlock)

class FakeWall(Cell):
	def __init__(self):
		super().__init__(SingleTexture(8, 0))
		
	def interact(self, app):
		app.blockActions()
		
		def clearBlock():
			app.setCell(Empty(), self.location, self.floor)
			app.unblockActions()
		_animate(self.texture, [(8, i) for i in range(4)] + [EMPTY_TEXTURE], clearBlock)

class Door(Cell):
	def __init__(self, textureRow):
		super().__init__(SingleTexture(textureRow, 0))
		self.textureRow = textureRow
	
	def open(self, app):
		app.blockActions()
		def clearBlock():
			app.setCell(Empty(), self.location, self.floor)
			app.unblockActions()
		_animate(self.texture, [(self.textureRow, i) for i in range(4)] + [EMPTY_TEXTURE], clearBlock)

class KeyedDoor(Door):
	def __init__(self, key):
		super().__init__(DOOR_TEXTURE_ROWS[key])
		self.key = key
		
	def interact(self, app):
		if app.hero.keys[self.key].value > 0:
			app.hero.keys[self.key].update(-1)
			self.open(app)
		
class GuardedDoor(Door, Impassable):
	def __init__(self):
		super().__init__(7)
		self.guards = 0
	
	def guard(self):
		self.guards += 1
	
	def unguard(self):
		self.guards -= 1
		if self.guards <= 0:
			self.open(app)
		
class Movement(Cell):
	def interact(self, app):
		app.hero.moveBy(self.location - app.hero.location)
		app.blockActions()
		
		def clearBlock(dt):
			self.move(app)
			app.unblockActions()
		Clock.schedule_once(clearBlock, 0.2)
		
	def move(self, app):
		raise NotImplementedError()
		
class Stair(Movement):
	def __init__(self, texture, direction):
		super().__init__(texture)
		self.direction = direction
		
	def move(self, app):
		app.moveByFloors(self.direction)
		
class Upstair(Stair):
	def __init__(self, floors = 1):
		super().__init__(SingleTexture(24, 2), floors)
		
class Downstair(Stair):
	def __init__(self, floors = 1):
		super().__init__(SingleTexture(24, 3), -floors)
		
class Portal(Movement):
	def __init__(self, row, col):
		super().__init__(SingleTexture(*EMPTY_TEXTURE))
		self.loc = Point(row, col)
		
	def move(self, app):
		app.hero.setLocation(self.loc)

class PropertyImprover(Cell):
	def __init__(self, texture, quantity):
		super().__init__(texture)
		self.quantity = quantity
	
	def property(self, hero):
		raise NotImplementedError()
		
	def interact(self, app):
		self.property(app.hero).update(self.quantity)
		app.hero.moveBy(self.location - app.hero.location)
		app.setCell(Empty(), self.location, self.floor)
		
class Key(PropertyImprover):
	def __init__(self, key):
		super().__init__(SingleTexture(*KEY_TEXTURES[key]), 1)
		self.key = key
		
	def property(self, hero):
		return hero.keys[self.key]
		
class SmallHealthPotion(PropertyImprover):
	def __init__(self, quantity):
		super().__init__(SingleTexture(16, 0), quantity)
	
	def property(self, hero):
		return hero.health
		
class LargeHealthPotion(PropertyImprover):
	def __init__(self, quantity):
		super().__init__(SingleTexture(16, 1), quantity)
	
	def property(self, hero):
		return hero.health
		
class AttackGem(PropertyImprover):
	def __init__(self, quantity):
		super().__init__(SingleTexture(18, 3), quantity)
	
	def property(self, hero):
		return hero.attack
		
class DefenceGem(PropertyImprover):
	def __init__(self, quantity):
		super().__init__(SingleTexture(19, 3), quantity)
	
	def property(self, hero):
		return hero.defence

class Sword(PropertyImprover):
	def __init__(self, textureCoord, quantity):
		super().__init__(SingleTexture(*textureCoord), quantity)
		
	def property(self, hero):
		return hero.attack
		
class Shield(PropertyImprover):
	def __init__(self, textureCoord, quantity):
		super().__init__(SingleTexture(*textureCoord), quantity)
		
	def property(self, hero):
		return hero.defence

class Shop(Cell):
	def __init__(self, contentProvider):
		super().__init__(FourTexture(6, 5, 3))
		self.contentProvider = contentProvider
	
	def interact(self, app):
		if app.hero.location - self.location == Point(1, 0):
			text, hotkeys = self.contentProvider.get(app, self)
			app.showDialog(text, hotkeys)
		
class ShopLeft(Impassable):
	def __init__(self):
		super().__init__(FourTexture(6, 4, 3))

class ShopRight(Impassable):
	def __init__(self):
		super().__init__(FourTexture(6, 6, 3))

# Expose other cells as well
from .monsters import *
