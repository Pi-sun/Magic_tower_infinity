import wx

TEXTURE_SIZE = 32
CELL_SIZE = 50

class Texture:
	@classmethod
	def init(self):
		self.textureMap = wx.Image("res/mttexture.png", wx.BITMAP_TYPE_ANY)
		self.none = wx.Bitmap.FromRGBA(CELL_SIZE, CELL_SIZE, alpha = 0)
		
		self.spark = wx.Image("res/spark.png", wx.BITMAP_TYPE_ANY).Rescale(CELL_SIZE, CELL_SIZE).ConvertToBitmap()
	
	@classmethod
	def texture(self, row, col):
		return self.textureMap.GetSubImage((col * TEXTURE_SIZE, row * TEXTURE_SIZE, TEXTURE_SIZE, TEXTURE_SIZE)).Rescale(CELL_SIZE, CELL_SIZE).ConvertToBitmap()

class TextureDisplay:
	def initialize(self, display):
		self.display = display

class SingleTextureDisplay(TextureDisplay):
	def __init__(self, textureRow, textureCol):
		self.textureRow = textureRow
		self.textureCol = textureCol
		
	def initialize(self, display):
		super().initialize(display)
		
		if self.textureRow == -1 and self.textureCol == -1:
			display.SetBitmap(Texture.none)
		else:
			display.SetBitmap(Texture.texture(self.textureRow, self.textureCol))

	def update(self):
		pass
		
class FourTextureDisplay(TextureDisplay):
	def __init__(self, textureRow, textureCol):
		self.textureRow = textureRow
		self.textureCol = textureCol
		self.currentTexture = 0
		
	def initialize(self, display):
		super().initialize(display)
		
		self.display.SetBitmap(Texture.texture(self.textureRow + self.currentTexture, self.textureCol))

	def update(self):
		self.currentTexture += 1
		self.currentTexture %= 4
		self.display.SetBitmap(Texture.texture(self.textureRow, self.textureCol + self.currentTexture))
