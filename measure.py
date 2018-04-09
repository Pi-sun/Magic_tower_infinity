import cProfile
import generate_section as generator

generator.newState()
import random
def work():
	for i in range(100):
		board = generator.generator.map_generate(11, [random.randint(0, 10), random.randint(0, 10)], "shop")

cProfile.run("work()")#("generator.generate_section()")
