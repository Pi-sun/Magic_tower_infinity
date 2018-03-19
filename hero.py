import threading, wx

from textures import *

def heroTextureRow(offset):
	offset = wx.Point(offset)
	if offset == (1, 0):
		return 0
	elif offset == (-1, 0):
		return 3
	elif offset == (0, 1):
		return 2
	elif offset == (0, -1):
		return 1

class Hero(wx.StaticBitmap):
	def __init__(self, grid, row, col):
		super().__init__(grid, -1, Texture.texture(0, 0), pos = (col * CELL_SIZE, row * CELL_SIZE))
		
		self.step = 0
		self.stepTimer = threading.Timer(1, lambda: None)
		self.location = wx.Point(row, col)
		
		self.health = 100
		self.attack = 10
		self.defence = 10
		
	def updateHealth(self, change):
		self.health += change
		
	def updateAttack(self, change):
		self.attack += change
		
	def updateDefence(self, change):
		self.defence += change
		
	def moveBy(self, offset):
		self.stepTimer.cancel()

		textureRow = heroTextureRow(offset)

		self.location += offset
		self.SetPosition((self.location.y * CELL_SIZE, self.location.x * CELL_SIZE))
		self.nextStep(textureRow)
	
		if self.step % 2 != 0:
			self.stepTimer = threading.Timer(0.15, lambda: wx.CallAfter(self.nextStep, textureRow))
			self.stepTimer.start()
			
	def nextStep(self, textureRow):
		self.step += 1
		self.step %= 4
		self.SetBitmap(Texture.texture(textureRow, self.step))
		
	def turnTo(self, offset):
		self.SetBitmap(Texture.texture(heroTextureRow(offset), self.step))
