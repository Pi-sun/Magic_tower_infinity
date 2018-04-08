import cProfile
import generate_section as generator

generator.newState()
cProfile.run("generator.generate_section()")