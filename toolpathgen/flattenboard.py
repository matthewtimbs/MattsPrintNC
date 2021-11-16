# Python script to generate board flattening GCode for my CNC.

import argparse
import sys


line_number = 0

def get_next_line_number():
    global line_number
    line_number += 5
    return line_number
# MJT add comment optional param.
def add_gcode_lines(command):
    global gcode

    for line in command.split('\n'):
        if not line:
            gcode.append(line)
        else:
            gcode.append("N" + str(get_next_line_number()) + " " + line)

parser = argparse.ArgumentParser()
parser.add_argument('--xmax', type=float, help='Max X travel')
parser.add_argument('--ymax', type=float, help='Max Y travel')
parser.add_argument('--bitwidth', type=float, help='Bit Width - defaults to 25.4mm', default=25.4)
parser.add_argument('--overlap', type=float, help='Overlap percentage - defaults to 0.5', default=0.5)
parser.add_argument('--name',type=str, help='file Name - defaults to flatten', default='flatten')
parser.add_argument('--feed', type=int, help='feed rate in mm/min.  defaults to 2500', default=2500)
parser.add_argument('--speed', type=int, help='spindle speed in rpms. defaults to 9000', default=9000)
parser.add_argument('--cutdepth', type=float, help='cut depth in mm, s/b less than zero. zero is top of surface.  default is .25mm', default=-0.2)

args = parser.parse_args()

if args.xmax is None or args.ymax is None:
    parser.print_help()
    print ("\n")
    sys.exit()


gcode = []
# add prefix
gcode.append("%")
gcode.append("({0} - Generated via flattenboard.py)".format(args.name))
gcode.append("(Use the {0} mm diameter bit)".format(args.bitwidth))
gcode.append("(This cuts {0} mm below Z zero)".format(args.cutdepth))

# Setup, with feed, speed etc then do first out-and-back pass  on Y0
script =  """

G90 G94 G17 G91.1
G21

G53 G0 Z0.

T1 M6
S{0} M3
G54
M8
G0 X0 Y0 Z2

G1 Z{1}  F{2}.

G1 X{3} Z{1}
G1 X0
"""

add_gcode_lines(script.format(args.speed, str(args.cutdepth),str(args.feed), str(args.xmax), str(args.speed)))



y_position = 0
y_advance_distance = args.bitwidth * args.overlap
num_trips = args.ymax / y_advance_distance

y_trip_index = 0
while y_trip_index < num_trips:
    # Each loop does an outbound trip and an inbound trip, thus the 2x increment of the index.
    y_position+=y_advance_distance
    add_gcode_lines("G1 Y{0}".format(y_position)) #Advance for outbound trip
    y_trip_index+=1

    add_gcode_lines("G1 X{0}".format(args.xmax)) #Do outbound trip (x0 to xmax)

    y_position+=y_advance_distance
    add_gcode_lines("G1 Y{0}".format(y_position)) #Advance for outbound trip
    y_trip_index+=1

    add_gcode_lines("G1 X0") #Do inbound trip (x0 to xmax)


add_gcode_lines("""
G1 Z15.
G17
M9
G0 Z5 X0 Y0
M30
""")

gcode.append("%")

for line in gcode:
    print(line)
