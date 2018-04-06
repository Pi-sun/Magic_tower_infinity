import floors
from textures import *

GRID_DIM = floors.dim
START_FLOOR, START_ROW, START_COL = floors.start

# Set these as early as possible,
# otherwise Kivy may not register these settings
from kivy.config import Config
Config.set("graphics", "resizable", 0)
Config.set("graphics", "width", CELL_SIZE * (GRID_DIM + 9))
Config.set("graphics", "height", CELL_SIZE * (GRID_DIM + 1))
Config.set("kivy", "exit_on_escape", "0")

import os, sys

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget

from mt_cells import Point, KEYS
from hero import Hero

LOADING_MAX_LENGTH = 5

def StatusLabel(**kwargs):
	return Label(
		valign = "middle",
		color = (1, 1, 1, 1),
		text_size = kwargs["size"],
		**kwargs)
 
class ColorWidget(Widget):
	def __init__(self, color, **kwargs):
		super().__init__(**kwargs)
		self.color = color
		
	def resize(self, width, height):
		self.size = (width, height)
		self.canvas.clear()
		with self.canvas:
			Color(*self.color)
			Rectangle(
				pos = self.pos,
				size = self.size)

class MagicTowerApp(App):
	def build(self):
		self.root = Widget()
		
		self.root.add_widget(Image(
			source = "res/fullbg.png",
			allow_stretch = True,
			size = Window.size))
		
		self.grid = Widget(pos = (CELL_SIZE * 4.5, CELL_SIZE * 0.5))
		self.root.add_widget(self.grid)
		
		# Cells are enlarged on each side to avoid gaps showing between the tiles
		self.cellDisplays = [[TextureDisplay(
			pos = (self.grid.pos[0] + CELL_SIZE * col - 0.3, self.grid.pos[1] + CELL_SIZE * (GRID_DIM - row - 1) - 0.2),
			size = (CELL_SIZE + 0.6, CELL_SIZE + 0.4)) for col in range(GRID_DIM)] for row in range(GRID_DIM)]
		for row in self.cellDisplays:
			for cell in row:
				self.grid.add_widget(cell)
		
		statusLabels = [StatusLabel(
			font_size = CELL_SIZE * 0.4,
			halign = "right",
			pos = (CELL_SIZE * 1.4375, CELL_SIZE * (9.21875 - 0.75 * i)),
			size = (CELL_SIZE * 1.96875, CELL_SIZE * 0.53125)) for i in range(4)]
		for label in statusLabels:
			self.root.add_widget(label)
		
		keyLabels = dict(zip(KEYS, (StatusLabel(
			font_size = CELL_SIZE * 0.4,
			halign = "right",
			pos = (CELL_SIZE * (6.40625 + GRID_DIM), CELL_SIZE * (7.125 - 0.75 * i)),
			size = (CELL_SIZE * 2.03125, CELL_SIZE * 0.53125)) for i in range(len(KEYS)))))
		for key in KEYS:
			self.root.add_widget(keyLabels[key])
		
		self.hero = Hero(self, self.grid, START_ROW, START_COL, *statusLabels, keyLabels)
		self.grid.add_widget(self.hero)
		
		self.spark = TextureDisplay(size = (CELL_SIZE, CELL_SIZE))
		
		self.levelLabel = StatusLabel(
			font_size = CELL_SIZE * 0.5,
			halign = "center",
			pos = (CELL_SIZE * 0.59375, CELL_SIZE * 10.125),
			size = (CELL_SIZE * 2.8125, CELL_SIZE * 0.65625))
		self.root.add_widget(self.levelLabel)
		
		self.monsterDisplay = TextureDisplay(
			pos = (CELL_SIZE * (6.5 + GRID_DIM), CELL_SIZE * 3.8125),
			size = (CELL_SIZE, CELL_SIZE))
		self.root.add_widget(self.monsterDisplay)
		
		self.monsterTexture = SingleTexture(-1, -1)
		self.monsterTexture.initialize(self.monsterDisplay)
		
		self.monsterNameLabel = StatusLabel(
			font_size = CELL_SIZE * 0.36,
			halign = "center",
			pos = (CELL_SIZE * (5.53125 + GRID_DIM), CELL_SIZE * 3.15625),
			size = (CELL_SIZE * 2.9375, CELL_SIZE * 0.53125))
		self.root.add_widget(self.monsterNameLabel)
		
		monsterStatusLabels = [StatusLabel(
			font_size = CELL_SIZE * 0.4,
			halign = "right",
			pos = (CELL_SIZE * (6.4375 + GRID_DIM), CELL_SIZE * (2.53125 - 0.625 * i)),
			size = (CELL_SIZE * 1.9375, CELL_SIZE * 0.53125)) for i in range(3)]
		for label in monsterStatusLabels:
			self.root.add_widget(label)
		self.monsterHealthLabel, self.monsterAttackLabel, self.monsterDefenceLabel = monsterStatusLabels
		
		self.loading = Widget(pos = (CELL_SIZE * 4.5, CELL_SIZE * 0.5))
		borderWidth = round(CELL_SIZE * 0.06)
		with self.loading.canvas:
			Color(204 / 255, 204 / 255, 204 / 255)
			Rectangle(
				pos = (self.loading.pos[0] + CELL_SIZE * (GRID_DIM / 2 - LOADING_MAX_LENGTH / 2) - borderWidth, self.loading.pos[1] + CELL_SIZE * (GRID_DIM / 2 - 0.65) - borderWidth),
				size = (borderWidth, CELL_SIZE * 0.5 + borderWidth * 2))
			Rectangle(
				pos = (self.loading.pos[0] + CELL_SIZE * (GRID_DIM / 2 + LOADING_MAX_LENGTH / 2), self.loading.pos[1] + CELL_SIZE * (GRID_DIM / 2 - 0.65) - borderWidth),
				size = (borderWidth, CELL_SIZE * 0.5 + borderWidth * 2))
			Rectangle(
				pos = (self.loading.pos[0] + CELL_SIZE * (GRID_DIM / 2 - LOADING_MAX_LENGTH / 2) - borderWidth, self.loading.pos[1] + CELL_SIZE * (GRID_DIM / 2 - 0.65) - borderWidth),
				size = (CELL_SIZE * LOADING_MAX_LENGTH + borderWidth * 2, borderWidth))
			Rectangle(
				pos = (self.loading.pos[0] + CELL_SIZE * (GRID_DIM / 2 - LOADING_MAX_LENGTH / 2) - borderWidth, self.loading.pos[1] + CELL_SIZE * (GRID_DIM / 2 - 0.15)),
				size = (CELL_SIZE * LOADING_MAX_LENGTH + borderWidth * 2, borderWidth))
		
		self.loading.add_widget(Label(
			text = "Preparing levels...",
			font_size = CELL_SIZE * 0.5,
			color = (204 / 255, 204 / 255, 204 / 255, 1),
			center = (self.loading.pos[0] + CELL_SIZE * GRID_DIM / 2, self.loading.pos[1] + CELL_SIZE * (GRID_DIM / 2 + 0.4))))
		
		self.loadingBar = ColorWidget((204 / 255, 204 / 255, 204 / 255), pos = (self.loading.pos[0] + CELL_SIZE * (GRID_DIM / 2 - LOADING_MAX_LENGTH / 2), self.loading.pos[1] + CELL_SIZE * (GRID_DIM / 2 - 0.65)))
		self.loading.add_widget(self.loadingBar)
		
		return self.root
		
	def on_start(self):
		self.floors = floors.floors
		self.showFloor(START_FLOOR)
		
		self.blockedActions = 0
				
		self.keyboard = Window.request_keyboard(lambda: None, self)
		self.keyboard.bind(on_key_down = self.onKeyDown)
		
		self.updateEvent = Clock.schedule_interval(self.update, 0.3)

	def on_stop(self):
		self.updateEvent.cancel()
		
	def showFloor(self, floor):
		self.root.remove_widget(self.grid)
		self.root.add_widget(self.loading)
		
		self.levelLabel.text = "Level %d" % floor
		
		self.floorsLoading = floors.prepareFloor(floor, self.handleFloorPrepared)
		self.targetFloorLoading = floor
		self.handleFloorPrepared(0)
		
	def handleFloorPrepared(self, amount):
		if self.floorsLoading:
			self.loadingBar.resize(amount / self.floorsLoading * CELL_SIZE * LOADING_MAX_LENGTH, CELL_SIZE * 0.5)
			
		if amount == self.floorsLoading:
			self.root.add_widget(self.grid)
			self.root.remove_widget(self.loading)
			
			self.floorsLoading = 0
			self.currentFloor = self.targetFloorLoading
			for row in range(GRID_DIM):
				for col in range(GRID_DIM):
					self.floors[self.currentFloor][row][col].initialize(Point(row, col), self.cellDisplays[row][col])					
		
	def update(self, dt):
		if not self.floorsLoading:
			for row in range(GRID_DIM):
				for col in range(GRID_DIM):
					self.floors[self.currentFloor][row][col].update()
		self.monsterTexture.update()
	
	def onKeyDown(self, keyboard, keycode, text, modifiers):
		print("Pressed", keycode[1], ("with " + ", ".join(modifiers)) if modifiers else "")
	
		if not self.floorsLoading and not self.blockedActions:
			if keycode[1] == "down":
				self.interactBy(Point(1, 0))
			elif keycode[1] == "up":
				self.interactBy(Point(-1, 0))
			elif keycode[1] == "right":
				self.interactBy(Point(0, 1))
			elif keycode[1] == "left":
				self.interactBy(Point(0, -1))
			elif keycode[1] == "a":
				self.moveByFloors(1)
			elif keycode[1] == "z":
				self.moveByFloors(-1)
	
	def blockActions(self):
		self.blockedActions += 1
			
	def unblockActions(self):
		self.blockedActions -= 1
		
	def showSpark(self):
		self.spark.pos = self.hero.pos
		self.spark.draw(texture(24, 16))
		self.grid.add_widget(self.spark)
		
	def hideSpark(self):
		self.grid.remove_widget(self.spark)
		
	def showMonster(self, monster):
		if monster:
			self.monsterTexture = monster.texture.copy()
			self.monsterNameLabel.text = monster.name
			self.monsterHealthLabel.text = str(monster.health)
			self.monsterAttackLabel.text = str(monster.attack)
			self.monsterDefenceLabel.text = str(monster.defence)
		else:
			self.monsterTexture = SingleTexture(*EMPTY_TEXTURE)
			self.monsterNameLabel.text = ""
			self.monsterHealthLabel.text = ""
			self.monsterAttackLabel.text = ""
			self.monsterDefenceLabel.text = ""
		self.monsterTexture.initialize(self.monsterDisplay)
				
	def updateMonsterHealth(self, health):
		self.monsterHealthLabel.text = str(health)
				
	def moveByFloors(self, change):
		if self.currentFloor + change > 0:
			self.showFloor(self.currentFloor + change)
			
	def setCell(self, cell, location):
		cell.initialize(location, self.cellDisplays[location.row][location.col])
		self.floors[self.currentFloor][location.row][location.col] = cell

	def interactBy(self, offset):
		self.hero.turnTo(offset)
	
		target = self.hero.location + offset
		if 0 <= target.row < GRID_DIM and 0 <= target.col < GRID_DIM:
			self.floors[self.currentFloor][target.row][target.col].interact(self)

if __name__ == '__main__':
	dir = os.path.dirname(sys.argv[0])
	if dir:
		os.chdir(dir)
	
	init_textures()
	try:
		MagicTowerApp().run()
	except KeyboardInterrupt:
		pass
	floors.stopPreparation()
