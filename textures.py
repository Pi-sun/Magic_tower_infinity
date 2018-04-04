from kivy.core.image import Image as TextureImage
from kivy.graphics import Rectangle
from kivy.uix.widget import Widget

TEXTURE_SIZE = 32
CELL_SIZE = 50

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
	def __init__(self, textureRow, textureCol):
		super().__init__()
		
		self.textureRow = textureRow
		self.textureCol = textureCol
		self.currentTexture = 0
		
	def initialize(self, display):
		super().initialize(display)
		self.display.draw(texture(self.textureRow, self.textureCol + self.currentTexture))

	def update(self):
		super().update()
		self.currentTexture += 1
		self.currentTexture %= 4
		self.display.draw(texture(self.textureRow, self.textureCol + self.currentTexture))

	def copy(self):
		texture = FourTexture(self.textureRow, self.textureCol)
		texture.currentTexture = self.currentTexture
		return texture
