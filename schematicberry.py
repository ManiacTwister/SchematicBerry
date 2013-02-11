#!/usr/bin/env python

from numpy import swapaxes, uint8
import sys, getopt, numpy
sys.path.append("./")

from mcpi import minecraft
import nbt

## Argument handling
debug = bool(0)
try:
    opts, args = getopt.getopt(sys.argv[1:],"i:d",["ifile=", "debug"])
except getopt.GetoptError:
    print 'schematicberry.py -i <inputfile>'
    sys.exit(2)
for opt, arg in opts:
    if opt in ("-i", "--ifile"):
    	ifile = arg
    elif opt in ("-d", "--debug"):
        debug = bool(1)

try:
    ifile
except:
    ifile = None

if ifile is None:
    print 'schematicberry.py -i <inputfile>'
    sys.exit()

try:
 level = nbt.load(ifile)
except IOError:
    print 'Could not open schematic file: ', ifile
    sys.exit(2)

## Load schematic
w = level["Width"].value
l = level["Length"].value
h = level["Height"].value

blocks = swapaxes(swapaxes(level["Blocks"].value.astype('uint16').reshape(h, l, w),0,2), 1,2) # yzx -> xzy -> xyz
datas = swapaxes(swapaxes(level["Data"].value.reshape(h, l, w),0,2), 1,2)

if debug:
    print l # z
    print h # y
    print w # x
    print len(blocks)
    print len(blocks[1])
    print len(blocks[1][1])

## Connect to server and send blocks
mc = minecraft.Minecraft.create()

for z in range(l):
    for y in range(h):
    	for x in range(w):
    		block = blocks[x][y][z]
    		data = datas[x][y][z]
    		mc.setBlock(x,y,z,block, data)