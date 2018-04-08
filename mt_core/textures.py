from kivy.core.image import Image as TextureImage
from kivy.graphics import Rectangle
from kivy.metrics import dp
from kivy.uix.widget import Widget

TEXTURE_SIZE = 32

CELL_SIZE_RAW = 48
CELL_SIZE = dp(CELL_SIZE_RAW) # Convert for ratina screens

EMPTY_TEXTURE = (-1, -1)

def init_textures():
	global atlas
	atlas = TextureImage("res/mttexture.png").texture

def texture(row, col):
	return atlas.get_region(TEXTURE_SIZE * col, atlas.size[1] - TEXTURE_SIZE * (row + 1), TEXTURE_SIZE, TEXTURE_SIZE)

class TextureDisplay(Widget):
	def draw(self, texture):
		self.canvas.clear()
		if texture:
			with self.canvas:
				Rectangle(
					texture = texture,
					pos = self.pos,
					size = self.size)

class Texture:
	def __init__(self):
		self.display = None

	def __getstate__(self):
		return {i[0]: i[1] for i in self.__dict__.items() if i[0] != "display"}
		
	def __setstate__(self, state):
		self.__dict__.update(state)
		self.display = None

	def initialize(self, display):
		self.display = display
		
	def update(self):
		pass
		
	def copy(self):
		return Texture()

class SingleTexture(Texture):
	def __init__(self, textureRow, textureCol):
		super().__init__()
		
		self.textureRow = textureRow
		self.textureCol = textureCol
		
	def initialize(self, display):
		super().initialize(display)
		self.draw()
		
	def reload(self, textureRow, textureCol):
		self.textureRow = textureRow
		self.textureCol = textureCol
		self.draw()
		
	def draw(self):
		if self.display:
			if (self.textureRow, self.textureCol) == EMPTY_TEXTURE:
				self.display.draw(None)
			else:
				self.display.draw(texture(self.textureRow, self.textureCol))
		
	def copy(self):
		return SingleTexture(self.textureRow, self.textureCol)
		
class FourTexture(Texture):
	def __init__(self, textureRow, textureCol, step = 1):
		super().__init__()
		
		self.textureRow = textureRow
		self.textureCol = textureCol
		self.step = step
		self.currentTexture = 0
		
	def initialize(self, display):
		super().initialize(display)
		self.display.draw(texture(self.textureRow, self.textureCol + self.currentTexture * self.step))

	def update(self):
		super().update()
		self.currentTexture += 1
		self.currentTexture %= 4
		self.display.draw(texture(self.textureRow, self.textureCol + self.currentTexture * self.step))

	def copy(self):
		texture = FourTexture(self.textureRow, self.textureCol, self.step)
		texture.currentTexture = self.currentTexture
		return texture
