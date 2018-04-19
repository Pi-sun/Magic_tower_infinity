import cProfile
import mt_generator as generator

generator.newState()
cProfile.run("for i in range(10):\n\tgenerator.generate_section()")
