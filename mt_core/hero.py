import weakref

from kivy.clock import Clock

from mt_cells import Point
from .floors import dim
from .textures import *

def heroTextureRow(offset = Point(1, 0)):
	if offset == Point(1, 0):
		return 0
	elif offset == Point(-1, 0):
		return 3
	elif offset == Point(0, 1):
		return 2
	elif offset == Point(0, -1):
		return 1

class HeroProperty:
	def __init__(self, value, label):
		self.value = value
		self.label = label
		label.text = str(value)
		
	def update(self, change):
		self.value += change
		self.label.text = str(self.value)

class Hero(TextureDisplay):
	def __init__(self, app, parent, row, col, healthLabel, attackLabel, defenceLabel, moneyLabel, keyLabels):
		super().__init__(pos = (parent.pos[0] + CELL_SIZE * col, parent.pos[1] + CELL_SIZE * (dim - row - 1)), size = (CELL_SIZE, CELL_SIZE))
		
		self.app = weakref.ref(app)
		self.base_pos = parent.pos
		
		self.step = 0
		self.stepTimer = None
		self.location = Point(row, col)
		
		self.health = HeroProperty(100, healthLabel)
		self.attack = HeroProperty(10, attackLabel)
		self.defence = HeroProperty(10, defenceLabel)
		self.money = HeroProperty(0, moneyLabel)
		
		self.keys = dict(map(lambda key: (key, HeroProperty(0, keyLabels[key])), keyLabels))
		self.keys["yellow"].update(100000) # for testing
		
		self.draw(texture(heroTextureRow(), self.step))
		
	def moveBy(self, offset):
		if self.stepTimer:
			self.stepTimer.cancel()
			self.stepTimer = None

		textureRow = heroTextureRow(offset)

		self.location += offset
		self.pos = (self.base_pos[0] + CELL_SIZE * self.location.col, self.base_pos[1] + CELL_SIZE * (dim - self.location.row - 1))
		self.nextStep(textureRow)
	
		app = self.app()
		if app:
			app.blockActions()
		
		def work(dt):
			self.nextStep(textureRow)
			if app:
				app.unblockActions()
		Clock.schedule_once(work, 0.1)
				
	def nextStep(self, textureRow):
		self.step += 1
		self.step %= 4
		self.draw(texture(textureRow, self.step))
		
	def turnTo(self, offset):
		self.draw(texture(heroTextureRow(offset), self.step))