import logging, threading, wx

import floors
from hero import Hero
from textures import *

GRID_DIM = floors.dim
START_FLOOR, START_ROW, START_COL = floors.start

LOADING_MAX_LENGTH = 5

WHITE = (204, 204, 204)

def callRepeatedly(interval, func):
	stopped = threading.Event()
	def loop():
		while not stopped.wait(interval): # the first call is in `interval` secs
			wx.CallAfter(func)
	threading.Thread(target = loop).start()    
	return stopped.set

class GameFrame(wx.Frame):
	def __init__(self):
		super().__init__(None, title = "Magic Tower", style = wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))
		
		self.floors = floors.floors
		
		size = (CELL_SIZE * (GRID_DIM + 9), CELL_SIZE * (GRID_DIM + 1))
		base = wx.Panel(self, -1, pos = (0, 0), size = size)
		
		bgBitmap = wx.Image("res/fullbg.png", wx.BITMAP_TYPE_ANY).Rescale(*size).ConvertToBitmap()
		bg = wx.StaticBitmap(base, -1, bgBitmap, pos = (0, 0))

		self.loading = wx.Panel(base, -1, pos = (CELL_SIZE * 4.5 + 1, CELL_SIZE * 0.5 + 1), size = (CELL_SIZE * GRID_DIM, CELL_SIZE * GRID_DIM))
		
		loadingLabel = wx.StaticText(self.loading, -1)
		loadingLabel.SetFont(wx.Font(CELL_SIZE / 2, wx.DEFAULT, wx.NORMAL, wx.NORMAL))
		loadingLabel.SetForegroundColour(WHITE)
		loadingLabel.SetLabelText("Preparing levels...")
		size = loadingLabel.GetSize()
		loadingLabel.SetPosition((CELL_SIZE * GRID_DIM / 2 - size[0] / 2, CELL_SIZE * (GRID_DIM / 2 - 0.1) - size[1]))
		
		borderWidth = round(CELL_SIZE * 0.06)
		loadingBorders = [
			wx.Panel(self.loading, -1, pos = (CELL_SIZE * (GRID_DIM / 2 - LOADING_MAX_LENGTH / 2) - borderWidth, CELL_SIZE * (GRID_DIM / 2 + 0.12)), size = (borderWidth, CELL_SIZE * 0.5 + borderWidth * 2)),
			wx.Panel(self.loading, -1, pos = (CELL_SIZE * (GRID_DIM / 2 + LOADING_MAX_LENGTH / 2), CELL_SIZE * (GRID_DIM / 2 + 0.12)), size = (borderWidth, CELL_SIZE * 0.5 + borderWidth * 2)),
			wx.Panel(self.loading, -1, pos = (CELL_SIZE * (GRID_DIM / 2 - LOADING_MAX_LENGTH / 2) - borderWidth, CELL_SIZE * (GRID_DIM / 2 + 0.12)), size = (CELL_SIZE * LOADING_MAX_LENGTH + borderWidth * 2, borderWidth)),
			wx.Panel(self.loading, -1, pos = (CELL_SIZE * (GRID_DIM / 2 - LOADING_MAX_LENGTH / 2) - borderWidth, CELL_SIZE * (GRID_DIM / 2 + 0.62) + borderWidth), size = (CELL_SIZE * LOADING_MAX_LENGTH + borderWidth * 2, borderWidth))
		]
		for border in loadingBorders:
			border.SetBackgroundColour(WHITE)
		
		self.loadingBar = wx.Panel(self.loading, -1, pos = (CELL_SIZE * (GRID_DIM / 2 - LOADING_MAX_LENGTH / 2), CELL_SIZE * (GRID_DIM / 2 + 0.12) + borderWidth), size = (0, CELL_SIZE * 0.5))
		self.loadingBar.SetBackgroundColour(WHITE)
		
		self.loading.Hide()
		
		self.image = wx.Image("res/mttexture.png", wx.BITMAP_TYPE_ANY)
		
		self.grid = wx.Panel(base, -1, pos = (CELL_SIZE * 4.5 + 1, CELL_SIZE * 0.5 + 1), size = (CELL_SIZE * GRID_DIM, CELL_SIZE * GRID_DIM))
		self.cellDisplays = [[wx.StaticBitmap(self.grid, -1, Texture.none, (col * CELL_SIZE, row * CELL_SIZE)) for col in range(GRID_DIM)] for row in range(GRID_DIM)]
		
		self.hero = Hero(self.grid, START_ROW, START_COL)
		
		self.Fit()
		
		self.showFloor(START_FLOOR)
		
		self.blockedActions = 0
		
		self.cancelUpdate = callRepeatedly(0.3, self.update)
		
		self.Bind(wx.EVT_CHAR_HOOK, self.onKeyPress)
		
	def Destroy(self):
		self.cancelUpdate()
		return super().Destroy()
		
	def showFloor(self, floor):
		self.grid.Hide()
		self.loading.Show()
		self.loadingBar.SetSize((0, CELL_SIZE * 0.5))
		
		self.floorsLoading = floors.prepareFloor(floor, self.handleFloorPrepared)
		self.targetFloorLoading = floor
		if not self.floorsLoading:
			self.handleFloorPrepared(0)
		
	def handleFloorPrepared(self, amount):
		if self.floorsLoading:
			self.loadingBar.SetSize((amount / self.floorsLoading * CELL_SIZE * LOADING_MAX_LENGTH, CELL_SIZE * 0.5))
		
		if amount == self.floorsLoading:
			print("Loaded")
			self.grid.Show()
			self.loading.Hide()
			
			self.floorsLoading = 0
			self.currentFloor = self.targetFloorLoading
			for row in range(GRID_DIM):
				for col in range(GRID_DIM):
					self.floors[self.currentFloor][row][col].initialize(wx.Point(row, col), self.cellDisplays[row][col])					
		
	def update(self):
		if not self.floorsLoading:
			for row in range(GRID_DIM):
				for col in range(GRID_DIM):
					self.floors[self.currentFloor][row][col].update()
		
	def onKeyPress(self, event):
		if not self.floorsLoading and not self.blockedActions:
			keycode = event.GetKeyCode()
			print("Keyed", keycode)
			if keycode == wx.WXK_DOWN:
				self.interactBy((1, 0))
			elif keycode == wx.WXK_UP:
				self.interactBy((-1, 0))
			elif keycode == wx.WXK_RIGHT:
				self.interactBy((0, 1))
			elif keycode == wx.WXK_LEFT:
				self.interactBy((0, -1))
			elif keycode == ord("A"):
				self.moveByFloors(1)
			elif keycode == ord("Z"):
				self.moveByFloors(-1)
			else:
				event.Skip()
			
	def blockActions(self):
		self.blockedActions += 1
			
	def unblockActions(self):
		self.blockedActions -= 1
			
	def moveByFloors(self, change):
		print(change)
		if self.currentFloor + change > 0:
			self.showFloor(self.currentFloor + change)
			
	def setCell(self, cell, location):
		location = wx.Point(location)
		
		cell.initialize(location, self.cellDisplays[location.x][location.y])
		self.floors[self.currentFloor][location.x][location.y] = cell
			
	def interactBy(self, offset):
		self.hero.turnTo(offset)
	
		target = self.hero.location + offset
		if 0 <= target.x < GRID_DIM and 0 <= target.y < GRID_DIM:
			self.floors[self.currentFloor][target.x][target.y].interact(self)
			
if __name__ == "__main__":
	app = wx.App()
	Texture.init()
	
	frame = GameFrame()
	frame.Show()
	app.MainLoop()
