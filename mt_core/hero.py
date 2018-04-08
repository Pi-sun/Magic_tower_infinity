import weakref

from kivy.clock import Clock

from mt_cells import Point, KEYS
from mt_cells.textures import *
from .floors import DIM

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
		self.label = label
		self.set(value)
	
	def set(self, value):
		self.value = value
		self.label.text = str(self.value)
		
	def update(self, change):
		self.set(self.value + change)

class Hero(TextureDisplay):
	def __init__(self, app, parent, healthLabel, attackLabel, defenceLabel, moneyLabel, keyLabels):
		super().__init__(pos = (0, 0), size = (CELL_SIZE, CELL_SIZE))
		
		self.app = weakref.ref(app)
		self.base_pos = parent.pos
		
		self.step = 0
		self.stepTimer = None
		self.location = Point(0, 0)
		
		self.health = HeroProperty(100, healthLabel)
		self.attack = HeroProperty(10, attackLabel)
		self.defence = HeroProperty(10, defenceLabel)
		self.money = HeroProperty(0, moneyLabel)
		
		self.keys = dict((key, HeroProperty(0, keyLabels[key])) for key in KEYS)
		self.keys["yellow"].set(100000) # for testing
		
		self.draw(texture(heroTextureRow(), self.step))
		
	def getState(self):
		return {
			"location": self.location,
			"health": self.health.value,
			"attack": self.attack.value,
			"defence": self.defence.value,
			"money": self.money.value,
			"keys": dict((key, self.keys[key].value) for key in KEYS)
		}
	
	def setState(self, state):
		self.health.set(state["health"])
		self.attack.set(state["attack"])
		self.defence.set(state["defence"])
		self.money.set(state["money"])
		for key in KEYS:
			self.keys[key].set(state["keys"][key])
		
		if self.stepTimer:
			self.stepTimer.cancel()
			self.stepTimer = None
		
		self.step = 0
		self.setLocation(state["location"])
		
	def setLocation(self, location):
		self.location = location
		self.draw(texture(heroTextureRow(), self.step))
		
	def draw(self, texture):
		self.pos = (self.base_pos[0] + CELL_SIZE * self.location.col, self.base_pos[1] + CELL_SIZE * (DIM - self.location.row - 1))
		super().draw(texture)
		
	def moveBy(self, offset):
		if self.stepTimer:
			self.stepTimer.cancel()
			self.stepTimer = None

		textureRow = heroTextureRow(offset)

		self.location += offset		
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
