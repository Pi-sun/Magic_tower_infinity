import math, threading, wx
from textures import *

def silent(lam):
	try:
		lam()
	except RuntimeError:
		pass

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
		super().__init__(SingleTextureDisplay(-1, -1))
	
	def interact(self, app):
		app.hero.moveBy(self.location - app.hero.location)
		
class Impassable(Cell):
	def __init__(self, texture):
		super().__init__(texture)
	
	def interact(self, app):
		pass
		
class Wall(Impassable):
	def __init__(self):
		super().__init__(SingleTextureDisplay(8, 0))
		
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
			bitmap = wx.StaticBitmap(app.hero, -1, Texture.spark)
			bitmap.Hide()
			
			print("Hit", heroStrikes)
			
			for i in range(heroStrikes):
				def strike(i):
					silent(lambda: bitmap.Show())
					threading.Timer(0.15, lambda: silent(lambda: bitmap.Hide())).start()
					if i != heroStrikes - 1:
						app.hero.updateHealth(-monsterDamage)
				def createStrike(i):
					return lambda: strike(i)
				threading.Timer(0.3 * i + 0.15, lambda: wx.CallAfter(createStrike(i))).start()
				
			def clearBlock():
				bitmap.Destroy()
				app.setCell(Empty(), self.location)
				app.unblockActions()
			threading.Timer(0.3 * heroStrikes, lambda: wx.CallAfter(clearBlock)).start()
		
class GreenSlime(Monster):
	def __init__(self):
		super().__init__(20, 15, 5, FourTextureDisplay(0, 4))
		
class SlimeKing(Monster):
	def __init__(self):
		super().__init__(20, 100, 0, FourTextureDisplay(3, 4))
		
class PropertyImprover(Cell):
	def __init__(self, texture):
		super().__init__(texture)
		
	def interact(self, app):
		app.hero.moveBy(self.location - app.hero.location)
		app.setCell(Empty(), self.location)
		
class AttackCrystal(PropertyImprover):
	def __init__(self, quantity):
		super().__init__(SingleTextureDisplay(11, 2))
		self.quantity = quantity
		
	def interact(self, app):
		app.hero.updateAttack(self.quantity)
		super().interact(app)
		
class DefenceCrystal(PropertyImprover):
	def __init__(self, quantity):
		super().__init__(SingleTextureDisplay(11, 3))
		self.quantity = quantity
		
	def interact(self, app):
		app.hero.updateDefence(self.quantity)
		super().interact(app)
		
class SmallHealthPotion(PropertyImprover):
	def __init__(self, quantity):
		super().__init__(SingleTextureDisplay(11, 0))
		self.quantity = quantity
		
	def interact(self, app):
		app.hero.updateHealth(self.quantity)
		super().interact(app)