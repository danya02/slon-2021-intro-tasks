from parser import Parser
from turtle_impl import *


# XXX: choose your turtle here
#turtle = DebugTurtle(battery=float('inf'))
#turtle = SimpleTurtle(battery=1000)
#turtle = PygameRenderingTurtle(battery=float('inf'))
turtle = PygameInteractiveTurtle(battery=float('10000'), steps_between_frames=1000)
p = Parser(turtle)

script = open(input('path to script: '))

p.read_file(script)
