# Python script to generate board flattening GCode for my CNC.

import argparse
import sys
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

if args.xmax is not None and args.ymax is not None:
    print("x " + str(args.xmax) + "  y " + str(args.ymax))
    print("\n\n")
else:
    parser.print_help()
    print ("\n")
    sys.exit()


print("continue")

script =  """
%%
({0} - Generated via flattenboard.py)
(This cuts {2}mm below Z zero)

N10 G90 G94 G17 G91.1
N15 G21

N20 G53 G0 Z0.

N25 T1 M6
N30 S{4} M3
N35 G54
N40 M8
N45 G0 X0 Y0 Z2

N56 G1 Z{2}  F{3}.
N60

N61 G18 G1 X[#<XMax>] Z{2}
N62 G1 X0
"""

print(script.format(args.name, str(args.xmax),str(args.cutdepth), str(args.feed), str(args.speed)))

# print(script)



"""
N63 G1 Y10
N64 G1 X[#<XMax>]
N66 G1 Y20
N68 G1 X0
N69 G1 Y30
N70 G1 X[#<XMax>]
G1 Y40
G1 X0

G1 Y50
G1 X[#<XMax>]
G1 Y60
G1 X0
G1 Y70
G1 X[#<XMax>]
G1 Y80
G1 X0
G1 Y90
G1 X[#<XMax>]
G1 Y100
G1 X0
G1 Y110
G1 X[#<XMax>]
G1 Y120
G1 X0
G1 Y130
G1 X[#<XMax>]
G1 Y140
G1 X0
G1 Y150
G1 X[#<XMax>]
G1 Y160
G1 X0
G1 Y170
G1 X[#<XMax>]
G1 Y180
G1 X0
G1 Y190
G1 X[#<XMax>]
G1 Y200
G1 X0
G1 Y210
G1 X[#<XMax>]
G1 Y220
G1 X0
G1 Y230
G1 X[#<XMax>]
G1 Y240
G1 X0
G1 Y250
G1 X[#<XMax>]
G1 Y260
G1 X0
G1 Y270
G1 x[#<XMax>]
G1 Y280
G1 X0
G1 Y290
G1 X[#<XMax>]
G1 Y300
G1 X0
G1 Y310
G1 X[#<XMax>]
G1 Y320
G1 X0
G1 Y330
G1 X[#<XMax>]



N365 G1 Z15.
N370 G17
N375 M9
N380  G0 Z5 X0 Y0
N385 M30
# %%
"""
