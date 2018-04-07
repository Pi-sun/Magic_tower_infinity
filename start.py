import os, sys

from app import MagicTowerApp as App

if __name__ == '__main__':
	dir = os.path.dirname(sys.argv[0])
	if dir:
		os.chdir(dir)
	
	App().run()
