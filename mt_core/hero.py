from kivy.clock import Clock

from mt_cells import Point, KEYS, KEY_YELLOW, KEY_BLUE, KEY_RED

from . import app
from .floors import DIM
from .textures import *
from .specials import *

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
	def __init__(self, label, value = None):
		self.label = label
		self.set(value)
	
	def set(self, value):
		self.value = value
		if value == None:
			self.label.text = ""
		else:
			self.label.text = str(self.value)
		
	def update(self, change):
		self.set(self.value + change)

class Hero(TextureDisplay):
	def __init__(self, parent, healthLabel, attackLabel, defenceLabel, moneyLabel, keyLabels, specialDisplays):
		super().__init__(pos = (0, 0), size = (CELL_SIZE, CELL_SIZE))
		
		self.base_pos = parent.pos
		
		self.step = 0
		self.stepTimer = None
		self.location = Point(0, 0)
		
		self.health = HeroProperty(healthLabel)
		self.attack = HeroProperty(attackLabel)
		self.defence = HeroProperty(defenceLabel)
		self.money = HeroProperty(moneyLabel)
		
		self.keys = dict((key, HeroProperty(keyLabels[key])) for key in KEYS)
		
		self.specialDisplays = specialDisplays
		self.specials = {}
		
		self.draw(texture(heroTextureRow(), self.step))
		
	def getState(self):
		return {
			"location": self.location,
			"health": self.health.value,
			"attack": self.attack.value,
			"defence": self.defence.value,
			"money": self.money.value,
			"keys": dict((key, self.keys[key].value) for key in KEYS),
			"specials": self.specials
		}
	
	def setState(self, state):
		self.health.set(state["health"])
		self.attack.set(state["attack"])
		self.defence.set(state["defence"])
		self.money.set(state["money"])
		for key in KEYS:
			self.keys[key].set(state["keys"][key])
		
		self.specials = state["specials"]
		for r, c in self.specials:
			self.specials[(r, c)].initialize(self, self.specialDisplays[r][c])
		
		if self.stepTimer:
			self.stepTimer.cancel()
			self.stepTimer = None
		
		self.step = 0
		self.setLocation(state["location"])
		
	def newState(self):
		self.health.set(200)
		self.attack.set(10)
		self.defence.set(10)
		self.money.set(0)
		
		self.keys[KEY_YELLOW].set(3)
		self.keys[KEY_BLUE].set(1)
		self.keys[KEY_RED].set(0)
		
		self.specials = {
			(0, 0): MonsterHandbook(),
			(0, 2): FlyingWand()}
		for r, c in self.specials:
			self.specials[(r, c)].initialize(self, self.specialDisplays[r][c])
			
		# Testing
		self.handbook.collect(1)
		self.flyingWand.collect(1)
			
	def setLocation(self, location):
		self.location = location
		self.draw(texture(heroTextureRow(), self.step))
	
	def updateSpecials(self):
		for loc in self.specials:
			self.specials[loc].update()
		
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
	
		app().blockActions()
		
		def work(dt):
			self.nextStep(textureRow)
			app().unblockActions()
			app().interactAround()
		Clock.schedule_once(work, 0.1)
				
	def nextStep(self, textureRow):
		self.step += 1
		self.step %= 4
		self.draw(texture(textureRow, self.step))
		
	def turnTo(self, offset):
		self.draw(texture(heroTextureRow(offset), self.step))
