from kivy.core.image import Image as TextureImage
from kivy.graphics import Rectangle
from kivy.uix.widget import Widget

TEXTURE_SIZE = 32
CELL_SIZE = 50

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
	def initialize(self, display):
		self.display = display
		
	def update(self):
		pass

class SingleTexture(Texture):
	def __init__(self, textureRow, textureCol):
		self.textureRow = textureRow
		self.textureCol = textureCol
		
	def initialize(self, display):
		super().initialize(display)
		
		if self.textureRow == -1 and self.textureCol == -1:
			display.draw(None)
		else:
			display.draw(texture(self.textureRow, self.textureCol))
		
class FourTexture(Texture):
	def __init__(self, textureRow, textureCol):
		self.textureRow = textureRow
		self.textureCol = textureCol
		self.currentTexture = 0
		
	def initialize(self, display):
		super().initialize(display)
		
		self.display.draw(texture(self.textureRow + self.currentTexture, self.textureCol))

	def update(self):
		super().update()
		self.currentTexture += 1
		self.currentTexture %= 4
		self.display.draw(texture(self.textureRow, self.textureCol + self.currentTexture))
