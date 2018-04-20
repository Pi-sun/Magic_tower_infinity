from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.uix.label import Label

from mt_cells import *

from . import app, hero
from .floors import DIM as GRID_DIM
from .textures import *

_EMPTY = SingleTexture(*EMPTY_TEXTURE)

_mouseMoveListeners = []
def _mouseMove(*args):
	for listener in _mouseMoveListeners:
		listener.on_mouse_pos(*args)
Window.bind(mouse_pos = _mouseMove)

class HoverButton(Button):
	hovered = BooleanProperty(False)
	border_point= ObjectProperty(None)

	def __init__(self, text, font_size = CELL_SIZE * 0.5, **kwargs):
		global _mouseMoveListeners
		super().__init__(
			background_normal = "",
			background_color = (0, 0, 0, 0),
			**kwargs)
		self.label = Label(
			text = text,
			font_size = font_size,
			color = (0, 0, 0, 1),
			pos = self.pos,
			size = self.size,
			text_size = self.size,
			halign = "center",
			valign = "middle")
		with self.label.canvas.before:
			Color(0, 1, 1, 0.6)
			Rectangle(
				pos = self.pos,
				size = self.size)
		_mouseMoveListeners.append(self)
		
	def on_mouse_pos(self, *args):
		if not self.get_root_window():
			return
		pos = args[1]
		
		inside = self.collide_point(*self.to_widget(*pos))
		if self.hovered == inside:
			return
		self.border_point = pos
		self.hovered = inside
		if inside:
			self.on_enter()
		else:
			self.on_leave()

	def on_enter(self):
		self.add_widget(self.label)

	def on_leave(self):
		self.remove_widget(self.label)

class SpecialItem:
	def __init__(self, texture):
		self.texture = texture
		self.count = 0
		
	def initialize(self, display, key = None):
		global _mouseMoveListeners
	
		self.texture.initialize(display)
		for child in display.children:
			if isinstance(child, HoverButton):
				_mouseMoveListeners.remove(child)
		display.clear_widgets()
		if key:
			self.addButton(display, key)
		
		if self.count == 0:
			_EMPTY.draw(display)
		
	def addButton(self, display, key):
		def work(ins):
			if app().isFree():
				self.tryUse()
	
		btn = HoverButton(key,
			pos = display.pos,
			size = display.size)
		btn.bind(on_press = work)
		display.add_widget(btn)
		
	def refresh(self):
		if self.count == 0:
			_EMPTY.draw(self.texture.display)
		else:
			self.texture.draw(self.texture.display)
		
	def update(self):
		if self.count:
			self.texture.update()
	
	def collect(self, n):
		raise NotImplementedError()
		
	def tryUse(self):
		if self.count > 0:
			self.use()
	
	def use(self):
		raise NotImplementedError()
		
class PersistentSpecialItem(SpecialItem):
	def collect(self, n):
		needRefresh = self.count == 0
		self.count = 1
		if needRefresh:
			self.refresh()
	
	def use(self):
		pass
	
class MonsterHandbook(PersistentSpecialItem):
	def __init__(self):
		super().__init__(SingleTexture(12, 0))

	def initialize(self, hero, display):
		super().initialize(display, "H")
		hero.handbook = self
		
	def use(self):
		super().use()
		app().showHandbook()
				
class FlyingWand(PersistentSpecialItem):
	def __init__(self):
		super().__init__(SingleTexture(13, 0))
	
	def initialize(self, hero, display):
		super().initialize(display)
		self.addButton(display)
		hero.flyingWand = self

	def addButton(self, display):
		def goUp(ins):
			if app().isFree():
				self.tryUp()
				
		btn1 = HoverButton("PageUp", CELL_SIZE * 0.28,
			pos = (display.pos[0], display.pos[1] + display.size[1] / 2),
			size = (display.size[0], display.size[1] / 2))
		btn1.bind(on_press = goUp)
		display.add_widget(btn1) 
				
		def goDown(ins):
			if app().isFree():
				self.tryDown()
	
		btn2 = HoverButton("PageDn", CELL_SIZE * 0.28,
			pos = display.pos,
			size = (display.size[0], display.size[1] / 2))
		btn2.bind(on_press = goDown)
		display.add_widget(btn2)
		
	def tryUp(self):
		if self.count > 0:
			self.up()
		
	def tryDown(self):
		if self.count > 0:
			self.down()
			
	def canMove(self):
		for offset in {Point(0, 0), Point(0, 1), Point(1, 0), Point(-1, 0), Point(0, -1)}:
			loc = app().hero.location + offset
			if loc.row >= 0 and loc.row < GRID_DIM and loc.col >= 0 and loc.col < GRID_DIM and isinstance(app().getCell(loc), Stair):
				return True
		return False
			
	def up(self):
		super().use()
		if self.canMove() and app().currentFloor < app().highestFloor:
			app().blockActions()
			
			def work(dt):
				for r in range(GRID_DIM):
					for c in range(GRID_DIM):
						loc = Point(r, c)
						if isinstance(app().getCell(loc), Upstair) or isinstance(app().getCell(loc, app().currentFloor + 1), Downstair):
							app().hero.setLocation(loc)
				app().moveByFloors(1)
				app().unblockActions()
			Clock.schedule_once(work, 0.2)

	def down(self):
		super().use()
		if self.canMove() and app().currentFloor > 1:
			app().blockActions()
			
			def work(dt):
				for r in range(GRID_DIM):
					for c in range(GRID_DIM):
						loc = Point(r, c)
						if isinstance(app().getCell(loc), Downstair) or isinstance(app().getCell(loc, app().currentFloor - 1), Upstair):
							app().hero.setLocation(loc)
				app().moveByFloors(-1)
				app().unblockActions()
			Clock.schedule_once(work, 0.2)
		
class OneUseSpecialItem(SpecialItem):
	def collect(self, n):
		self.count += n
		if self.count == n:
			self.refresh()
		
	def use(self):
		self.count -= 1
		if self.count == 0:
			self.refresh()

class Mattock(OneUseSpecialItem):
	def __init__(self):
		super().__init__(SingleTexture(15, 0))
	
	def initialize(self, hero, display):
		super().initialize(display, "M")
		hero.mattock = self

	def use(self):
		dir = hero.heroDirections[app().hero.facing]
		next = app().hero.location + dir
		if next.row >= 0 and next.row < GRID_DIM and next.col >= 0 and next.col < GRID_DIM:
			cell = app().getCell(next)
			if isinstance(cell, Wall) or isinstance(cell, FakeWall) or (isinstance(cell, HiddenWall) and cell.hidden == False):
				super().use()
				removeWall(cell)
