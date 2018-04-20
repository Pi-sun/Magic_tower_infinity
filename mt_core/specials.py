import weakref

from kivy.uix.button import Button

from . import app
from .textures import *

_EMPTY = SingleTexture(*EMPTY_TEXTURE)

class SpecialItem:
	def __init__(self, texture):
		self.texture = texture
		self.count = 0
		
	def initialize(self, display):
		self.texture.initialize(display)
		self.addButton(display)
		
		if self.count == 0:
			_EMPTY.draw(display)
		
	def addButton(self, display):
		btn = Button(
			pos = display.pos,
			size = display.size,
			opacity = 0)
		btn.bind(on_press = lambda ins: self.tryUse())
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
		super().initialize(display)
		hero.handbook = weakref.ref(self)
		
	def use(self):
		super().use()
		app().showHandbook()

class OneUseSpecialItem(SpecialItem):
	def collect(self, n):
		self.count += n
		if self.count == n:
			self.refresh()
		
	def use(self):
		self.count -= 1
		if self.count == 0:
			self.refresh()
