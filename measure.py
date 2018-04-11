import cProfile
import generate_section as generator

generator.newState()
cProfile.run("for i in range(10):\n\tgenerator.generate_section()")
