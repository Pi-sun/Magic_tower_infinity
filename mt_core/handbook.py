from kivy.uix.widget import Widget

from mt_cells import *

from .floors import DIM as GRID_DIM
from .textures import CELL_SIZE

class HandbookDisplay(Widget):
	def getMonsters(self, map):
		monsters = {}
		for row in map:
			for cell in row:
				if isinstance(cell, Monster):
					if cell.name not in monsters:
						monsters[cell.name] = cell
		return sorted(monsters.values(), key = lambda m: m.name)
	
	def show(self, map):
		monsters = self.getMonsters(map)
		print()
		for monster in monsters:
		  print("%s: %d/%d/%d/%d" % (monster.name, monster.health, monster.attack, monster.defence, monster.money))
		  analysis = CombatAnalysis(monster)
		  if analysis.monsterTotalDamage == -1:
		  	print("    Cannot attack")
		  elif analysis.monsterTotalDamage == 0:
		  	print("    No damage")
		  else:
		  	print("    Incur %d damage" % analysis.monsterTotalDamage)
		print()
