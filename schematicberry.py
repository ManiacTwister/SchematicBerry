#!/usr/bin/env python
from numpy import swapaxes, uint8
import sys, getopt, numpy
sys.path.append("./")
from mcpi import minecraft
import nbt
import time

## Argument handling
debug = bool(0)
xOffset = 0
yOffset = 0
zOffset = 0

try:
    opts, args = getopt.getopt(sys.argv[1:],"i:c:d",["ifile=", "coordinates=", "debug"])
except getopt.GetoptError:
    print 'schematicberry.py -i <inputfile>'
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-i", "--ifile"):
        ifile = arg
    elif opt in ("-c", "--coordinates"):
        coords = arg.split(",")
        if len(coords) == 3:
            xOffset = coords[0]
            yOffset = coords[1]
            zOffset = coords[2]
        else:
            print "Coordinates have to be x,y,z"
            sys.exit(2)
    elif opt in ("-d", "--debug"):
        debug = bool(1)

try:
    ifile
except:
    ifile = None

if ifile is None:
    print 'schematicberry.py -i <inputfile> [-c <x,y,z>]'
    sys.exit()

try:
 level = nbt.load(ifile)
except IOError:
    print 'Could not open schematic file: ', ifile
    sys.exit(2)

def progress(i):
    sys.stdout.write("\rPlacing blocks ... %d%% done" % i)
    sys.stdout.flush()

## Load schematic
w = level["Width"].value
l = level["Length"].value
h = level["Height"].value
total = float(w * l * h)

blocks = swapaxes(swapaxes(level["Blocks"].value.astype('uint16').reshape(h, l, w),0,2), 1,2) # yzx -> xzy -> xyz
datas = swapaxes(swapaxes(level["Data"].value.reshape(h, l, w),0,2), 1,2)

print "Loaded %s " % ifile

if debug:
    print l # z
    print h # y
    print w # x
    print len(blocks)
    print len(blocks[1])
    print len(blocks[1][1])

## Connect to server and send blocks
mc = minecraft.Minecraft.create()

cur = 0.0
for z in range(l):
    for y in range(h):
        for x in range(w):
            block = blocks[x][y][z]
            data = datas[x][y][z]
            mc.setBlock(xOffset + x, yOffset + y, zOffset + z, block, data)
            cur = cur + 1.0
            progress(cur / total * 100)

print "\nGoodbye."