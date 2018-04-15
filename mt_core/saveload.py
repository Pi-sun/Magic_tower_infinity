import os

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup

Builder.load_string("""
<LoadDialog>:
	BoxLayout:
		size: root.size
		pos: root.pos
		orientation: "vertical"
		FileChooserListView:
			id: filechooser
			filters: ["*.mts"]
			on_selection: btn_load.disabled = not root.verify(self.selection)

		BoxLayout:
			size_hint_y: None
			height: 30
			Button:
				text: "Cancel <esc>"
				on_release: root.cancel()

			Button:
				id: btn_load
				text: "Load <enter>"
				on_release: root.submit()

<SaveDialog>:
	BoxLayout:
		size: root.size
		pos: root.pos
		orientation: "vertical"
		FileChooserListView:
			id: filechooser
			filters: ["*.mts"]
			on_selection: root.update(self.selection)

		TextInput:
			id: text_input
			text: "game.mts"
			size_hint_y: None
			height: 30
			multiline: False

		BoxLayout:
			size_hint_y: None
			height: 30
			Button:
				text: "Cancel <esc>"
				on_release: root.cancel()

			Button:
				id: btn_save
				text: "Save <enter>"
				on_release: root.submit()
""")

_popup = None

def _dismiss(cancel = True):
	if _popup:
		_popup.dismiss(cancel)

class ResponsivePopup(Popup):
	def __init__(self, cancelCallback, **kwargs):
		super().__init__(**kwargs)
		self.cancelCallback = cancelCallback
	
	def dismiss(self, cancel = True):
		if cancel and self.cancelCallback:
			self.cancelCallback()
		self.content.finalize()
		super().dismiss()

class Dialog(FloatLayout):
	def __init__(self):
		super().__init__()
		
		self.keyboard = Window.request_keyboard(lambda: None, self)
		self.keyboard.bind(on_key_down = self.onKeyDown)

	def finalize(self):
		self.keyboard.unbind(on_key_down = self.onKeyDown)
	
	def onKeyDown(self, keyboard, keycode, text, modifiers): 
		if keycode[1] == "escape":
			self.cancel()
		elif keycode[1] == "enter":
			self.submit()

class LoadDialog(Dialog):
	def __init__(self, callback):
		super().__init__()
		self.load = callback
		self.cancel = _dismiss
		
		self.ids.btn_load.disabled = True
		
	def submit(self):
		self.load(self.ids.filechooser.path, self.ids.filechooser.selection)
		
	def verify(self, selection):
		return selection and selection[0] and os.path.splitext(selection[0])[1] == ".mts" and os.path.isfile(selection[0])

class SaveDialog(Dialog):
	def __init__(self, callback):
		super().__init__()
		self.save = callback
		self.cancel = _dismiss

		def refreshBtn(ins, text):
			self.ids.btn_save.disabled = not text
		self.ids.text_input.bind(text = refreshBtn)

	def submit(self):
		self.save(self.ids.filechooser.path, self.ids.text_input.text)

	def update(self, selection):
		if selection and selection[0]:
			name = os.path.split(selection[0])[1]
			if name:
				self.ids.text_input.text = name
				self.ids.filechooser.selection = []

def showLoad(callback, cancelCallback = None):
	def work(path, filename):
		if filename and filename[0]:
			callback(filename[0])
			_dismiss(False)
	
	global _popup
	content = LoadDialog(work)
	content.ids.filechooser.path = os.path.expanduser("~")
	_popup = ResponsivePopup(cancelCallback, 
		title = "Load file",
		content = content,
		size_hint = (0.8, 0.9))
	_popup.open()

def showSave(callback, cancelCallback = None):
	def work(path, filename):
		if filename:
			file = os.path.join(path, filename)
			if os.path.splitext(file)[1] != ".mts":
				file += append(".mts")
			callback(file)
			_dismiss(False)
	
	global _popup
	content = SaveDialog(work)
	content.ids.filechooser.path = os.path.expanduser("~")
	_popup = ResponsivePopup(cancelCallback,
		title = "Save file",
		content = content,
		size_hint = (0.8, 0.9))
	_popup.open()
