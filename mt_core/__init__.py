import gzip, os, pickle

# Set these as early as possible,
# otherwise Kivy may not register these settings
from kivy.config import Config
Config.set("graphics", "resizable", 0)
Config.set("kivy", "exit_on_escape", 0)
Config.set("input", "mouse", "mouse,disable_on_activity,disable_multitouch")

from kivy.app import App
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.widget import Widget

_app = None
def app():
	return _app

from mt_cells import Point, KEYS

from .textures import *

# Required by initialization of mt_core.floors
REF_KEY_ANY = "__any__"
LARGE_TEXT_GAP = "[size=%d]\n\n[/size]" % round(CELL_SIZE * 0.7)
SMALL_TEXT_GAP = "[size=%d]\n\n[/size]" % round(CELL_SIZE * 0.3)

from . import floors, handbook, saveload
from .hero import Hero

GRID_DIM = floors.DIM

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
	def __init__(self):
		init_textures()
		super().__init__()

	def run(self):
		Window.size = (CELL_SIZE_RAW * (GRID_DIM + 9), CELL_SIZE_RAW * (GRID_DIM + 1))
		try:
			super().run()
		except KeyboardInterrupt:
			pass
		floors.stopPreparation()

	def build(self):
		self.root = Widget()
		
		self.root.add_widget(Image(
			source = "res/fullbg.png",
			allow_stretch = True,
			size = (CELL_SIZE * (GRID_DIM + 9), CELL_SIZE * (GRID_DIM + 1))))
				
		self.grid = Widget(pos = (CELL_SIZE * 4.5, CELL_SIZE * 0.5))
		
		# Cells are enlarged on each side to avoid gaps showing between the tiles
		self.cellDisplays = [[TextureDisplay(
			pos = (self.grid.pos[0] + CELL_SIZE * col, self.grid.pos[1] + CELL_SIZE * (GRID_DIM - row - 1)),
			size = (CELL_SIZE, CELL_SIZE)) for col in range(GRID_DIM)] for row in range(GRID_DIM)]
		for row in self.cellDisplays:
			for cell in row:
				self.grid.add_widget(cell)
		
		statusLabels = [StatusLabel(
			font_size = CELL_SIZE * 0.4,
			halign = "right",
			pos = (CELL_SIZE * 1.4375, CELL_SIZE * (3.71875 + GRID_DIM / 2 - 0.75 * i)),
			size = (CELL_SIZE * 1.96875, CELL_SIZE * 0.53125)) for i in range(4)]
		for label in statusLabels:
			self.root.add_widget(label)
		
		keyLabels = dict(zip(KEYS, (StatusLabel(
			font_size = CELL_SIZE * 0.4,
			halign = "right",
			pos = (CELL_SIZE * (6.40625 + GRID_DIM), CELL_SIZE * (1.625 + GRID_DIM / 2 - 0.75 * i)),
			size = (CELL_SIZE * 2.03125, CELL_SIZE * 0.53125)) for i in range(len(KEYS)))))
		for key in KEYS:
			self.root.add_widget(keyLabels[key])
		
		specialItemDisplays = [[TextureDisplay(
			pos = (CELL_SIZE * (0.5 + col), CELL_SIZE * (GRID_DIM / 2 - 0.25 - row)),
			size = (CELL_SIZE, CELL_SIZE)) for col in range(3)] for row in range(5)]
		for row in specialItemDisplays:
			for cell in row:
				self.root.add_widget(cell)
		
		self.hero = Hero(self.grid, *statusLabels, keyLabels, specialItemDisplays)
		self.grid.add_widget(self.hero)
		
		self.spark = TextureDisplay(size = (CELL_SIZE, CELL_SIZE))
		
		self.floorLabel = StatusLabel(
			font_size = CELL_SIZE * 0.5,
			halign = "center",
			pos = (CELL_SIZE * 0.59375, CELL_SIZE * (4.625 + GRID_DIM / 2)),
			size = (CELL_SIZE * 2.8125, CELL_SIZE * 0.65625))
		self.root.add_widget(self.floorLabel)
		
		self.monsterDisplay = TextureDisplay(
			pos = (CELL_SIZE * (6.5 + GRID_DIM), CELL_SIZE * (GRID_DIM / 2 - 1.6875)),
			size = (CELL_SIZE, CELL_SIZE))
		self.root.add_widget(self.monsterDisplay)
		
		self.monsterTexture = SingleTexture(-1, -1)
		self.monsterTexture.initialize(self.monsterDisplay)
		
		self.monsterNameLabel = StatusLabel(
			font_size = CELL_SIZE * 0.36,
			halign = "center",
			pos = (CELL_SIZE * (5.53125 + GRID_DIM), CELL_SIZE * (GRID_DIM / 2 - 2.34375)),
			size = (CELL_SIZE * 2.9375, CELL_SIZE * 0.53125))
		self.root.add_widget(self.monsterNameLabel)
		
		monsterStatusLabels = [StatusLabel(
			font_size = CELL_SIZE * 0.4,
			halign = "right",
			pos = (CELL_SIZE * (6.4375 + GRID_DIM), CELL_SIZE * (GRID_DIM / 2 - 2.96875 - 0.625 * i)),
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
			text = "Preparing floors...",
			font_size = CELL_SIZE * 0.5,
			color = (204 / 255, 204 / 255, 204 / 255, 1),
			center = (self.loading.pos[0] + CELL_SIZE * GRID_DIM / 2, self.loading.pos[1] + CELL_SIZE * (GRID_DIM / 2 + 0.4))))
		
		self.loadingBar = ColorWidget((204 / 255, 204 / 255, 204 / 255), pos = (self.loading.pos[0] + CELL_SIZE * (GRID_DIM / 2 - LOADING_MAX_LENGTH / 2), self.loading.pos[1] + CELL_SIZE * (GRID_DIM / 2 - 0.65)))
		self.loading.add_widget(self.loadingBar)
		
		self.dialog = Label(
			font_size = CELL_SIZE * 0.5,
			color = (0, 0, 0),
			halign = "center",
			valign = "middle",
			markup = True,
			pos = (CELL_SIZE * 5.3, CELL_SIZE * 2.5),
			size = (CELL_SIZE * (GRID_DIM - 1.6), CELL_SIZE * (GRID_DIM - 4)))
		with self.dialog.canvas.before:
			Color(0, 1, 1, 0.8)
			Rectangle(
				pos = self.dialog.pos,
				size = self.dialog.size)
		self.dialog.bind(on_ref_press = self.onDialogPress)
		
		self.handbook = handbook.HandbookDisplay(pos = (CELL_SIZE * 4.5, CELL_SIZE * 0.5))
		
		return self.root
		
	def on_start(self):
		global _app
		_app = self
	
		self.blockedActions = 0
		self.floorsLoading = 0
		self.currentFloor = None
		self.highestFloor = None
		
		self.saved = True
		self.filepath = None
		
		self.keyboard = Window.request_keyboard(lambda: None, self.root)
		self.keyboard.bind(on_key_down = self.onKeyDown)
		
		self.showStartDialog()
		
		self.updateEvent = Clock.schedule_interval(self.update, 0.3)

	def on_stop(self):
		self.updateEvent.cancel()
		
	def onKeyDown(self, keyboard, keycode, text, modifiers):
		print("Pressed", keycode[1], ("with " + ", ".join(modifiers)) if modifiers else "")
	
		if self.dialogHotkeys != None:
			self.handleDialog(keycode[1])	
		elif self.isFree():
			if keycode[1] == "down":
				self.interactBy(Point(1, 0))
			elif keycode[1] == "up":
				self.interactBy(Point(-1, 0))
			elif keycode[1] == "right":
				self.interactBy(Point(0, 1))
			elif keycode[1] == "left":
				self.interactBy(Point(0, -1))
			elif keycode[1] == "l":
				self.loadGame()
			elif keycode[1] == "s":
				self.saveGame()
			elif keycode[1] == "h":
				self.hero.handbook.tryUse()
			elif keycode[1] == "pageup":
				self.hero.flyingWand.tryUp()
			elif keycode[1] == "pagedown":
				self.hero.flyingWand.tryDown()
			# cheats
			elif keycode[1] == "a" and "alt" in modifiers:
				self.moveByFloors(1)
			elif keycode[1] == "z" and "alt" in modifiers:
				self.moveByFloors(-1)
		
	def onDialogPress(self, instance, value):
		print("Pressed ref", value)
		
		if self.dialogHotkeys != None:
			self.handleDialog(value)
		
	def isFree(self):
		return self.currentFloor != None and (not self.floorsLoading) and (not self.blockedActions)
		
	def showStartDialog(self):
		text = "Magic Tower!" + LARGE_TEXT_GAP + "[ref=n][u]N[/u]ew Game[/ref]" + \
					 SMALL_TEXT_GAP + "[ref=l][u]L[/u]oad Game[/ref]"
		actions = {"n": lambda: self.newGame() or True,
							 "l": lambda: self.loadFile() or True}
		self.showDialog(text, actions)
		
	def showFloor(self, floor, completion = None):
		self.root.remove_widget(self.grid)
		self.root.add_widget(self.loading)
		
		self.floorLabel.text = "Floor %d" % floor
		
		self.floorsLoading = floors.prepareFloor(floor, self.handleFloorPrepared)
		self.floorsLoadingCompletion = completion
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
			if self.currentFloor > self.highestFloor:
				self.highestFloor = self.currentFloor
			for row in range(GRID_DIM):
				for col in range(GRID_DIM):
					floors.floors[self.currentFloor][row][col].initialize(self.cellDisplays[row][col])
			
			if self.floorsLoadingCompletion:
				self.floorsLoadingCompletion()
				self.floorsLoadingCompletion = None
					
	def update(self, dt):
		if not self.floorsLoading and self.currentFloor != None:
			for row in range(GRID_DIM):
				for col in range(GRID_DIM):
					floors.floors[self.currentFloor][row][col].update()
		self.hero.updateSpecials()
		self.monsterTexture.update()
	
	def saveGame(self):
		def save(path):
			data = {
				"hero": self.hero.getState(),
				"floors": floors.getState(),
				"currentFloor": self.currentFloor,
				"highestFloor": self.highestFloor
			}
			with gzip.open(path, "wb") as f:
				pickle.dump(data, f)
		
			self.filepath = path
			self.saved = True
		
		if self.filepath:
			save(self.filepath)
		else:
			self.blockActions()
			def saveAfterGetPath(path):
				save(path)
				self.unblockActions()
			saveload.showSave(saveAfterGetPath, self.unblockActions)
	
	def loadGame(self):
		if self.filepath:
			def work():
				with gzip.open(self.filepath, "rb") as f:
					data = pickle.load(f)

				floors.setState(data["floors"])
				self.highestFloor = data["highestFloor"]
				self.showFloor(data["currentFloor"])
				self.hero.setState(data["hero"])
		
				self.saved = True
				return True
			
			if self.saved:
				work()
			else:
				text = "Your current progress will be lost!\nStill loading previous save?" + LARGE_TEXT_GAP + \
							 "[ref=y]<  Y  > Yes" + " " * 21 + "[/ref]" + SMALL_TEXT_GAP + "[ref=" + REF_KEY_ANY + "]<Any> Return to game[/ref]"
				actions = {"y": work,
									 REF_KEY_ANY: lambda: True}
				self.showDialog(text, actions)
	
	def loadFile(self):
		self.blockActions()
		def loadAfterGetPath(path):
			self.filepath = path
			self.loadGame()
			self.unblockActions()
		def loadCancel():
			self.showStartDialog()
			self.unblockActions()
		saveload.showLoad(loadAfterGetPath, loadCancel)
		
	def newGame(self):
		floors.newState()
		
		START_FLOOR, START_ROW, START_COL = floors.START
		self.highestFloor = START_FLOOR
		self.showFloor(START_FLOOR)
		self.hero.newState()
		self.hero.setLocation(Point(START_ROW, START_COL))
		
		self.saved = False
		
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
			self.monsterTexture = monster.menu_texture.copy()
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
			self.showFloor(self.currentFloor + change, lambda: self.interactAround())
			
	def getCell(self, location, floor = None):
		if floor == None:
			return floors.floors[self.currentFloor][location.row][location.col]
		else:
			return floors.floors[floor][location.row][location.col]
			
	def setCell(self, cell, location, floor = None):
		if floor == None or floor == self.currentFloor:
			cell.initialize(self.cellDisplays[location.row][location.col])
			floors.floors[self.currentFloor][location.row][location.col] = cell
		else:
			floors.floors[floor][location.row][location.col] = cell
		cell.placeAt(self.currentFloor if floor == None else floor, location)

	def interactBy(self, offset):
		self.hero.turnTo(offset)
	
		target = self.hero.location + offset
		if 0 <= target.row < GRID_DIM and 0 <= target.col < GRID_DIM:
			floors.floors[self.currentFloor][target.row][target.col].interact()
		
		self.saved = False

	def interactAround(self):
		for offset in (Point(r, c) for r, c in ((0, 1), (1, 0), (0, -1), (-1, 0))):
			target = self.hero.location + offset
			if 0 <= target.row < GRID_DIM and 0 <= target.col < GRID_DIM:
				floors.floors[self.currentFloor][target.row][target.col].interactAround()

	def showDialog(self, text, hotkeys, custom = False):
		self.dialogHotkeys = hotkeys
		self.dialogCustom = custom
		if not custom:
			self.dialog.text = text
			self.root.add_widget(self.dialog)
		
	def handleDialog(self, key):
		if key in self.dialogHotkeys:
			action = self.dialogHotkeys[key]
		elif REF_KEY_ANY in self.dialogHotkeys:
			action = self.dialogHotkeys[REF_KEY_ANY]
		else:
			return
		
		if action():
			if not self.dialogCustom:
				self.root.remove_widget(self.dialog)
			self.dialogHotkeys = None
			
	def showHandbook(self):
		self.handbook.show(floors.floors[self.currentFloor])
