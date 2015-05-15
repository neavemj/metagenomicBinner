#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Matt's metagenomic binner using pyqtgraph
Graphical interface module for selecting contigs and checking genome completeness

"""
from __future__ import absolute_import
from __future__ import print_function

# imports

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
from symBinner import symbData
from symBinner import symbHelper
import argparse
import six

# use argparse to get commmand line arguments for coverage files, gc, etc.

parser = argparse.ArgumentParser("Metagenome binner")

parser.add_argument('coverage_files', type = argparse.FileType("r"),
                    nargs = "+", help = "tab delimited coverage files")
parser.add_argument('--gc_file', '-g', type = argparse.FileType("r"),
                    nargs = "?", help = "tab delimited gc content file")
parser.add_argument('--min_size_to_draw', '-s', type = int,
                    nargs = "?", help = "indicate minimum contig length for drawing (default: 1000). Note all contigs are still captured in the selection.",
                    default = 1000)
parser.add_argument('--coverage_col', '-c', type = int,
                    nargs = "+", help = "indicate coverage column in file (default: 2)",
                    default = 2)

args = parser.parse_args()

# get data and import using symbData.py module

sample1_file = args.coverage_files[0]
sample2_file = args.coverage_files[1]
gc_file = args.gc_file

dataResults = symbData.getCombinedData(cov1 = sample1_file, cov2 = sample2_file, gc_content = gc_file)
covDict = dataResults[0]
maxGCcontent = dataResults[1]
minGCcontent = dataResults[2]
avgGCcontent = dataResults[3]

# covDict data structure:
# covDict[scaffold] = {'cov' : , 'length' : , 'gc' : }


# create a color map gradient for coloring my gc points
# TODO: could also add key for gc content colors?

#python -m cProfile -s cumulative metaBinner.py

#give points 10 colours evenly spaced between the calculated max and min gc content

print("*** Generating GC Colour Profiles ***")

point = np.linspace(minGCcontent, maxGCcontent, 10)
print('gc range:', minGCcontent, avgGCcontent, maxGCcontent)
color = np.array([[231,246,189],[102,6,95],[229,82,7],[74,94,20],[249,149,161],[38,241,240],
                  [103,20,27],[253,203,120],[250,77,137],[248,55,66]], dtype=np.ubyte)
colmap = pg.ColorMap(point, color)

# use list comprehension to add my data points to a list of dictionaries as required by pyqtgraph
# divided length by 500 because this looked about right but should come up with something better
# spots to draw means only contigs bigger than this length will be drawn

print("*** Creating Spot Dictionaries ***")

size_to_draw = args.min_size_to_draw

spots_to_draw = [{'pos': np.log(j['cov']), 'data': 1, 'brush' : colmap.map(j['gc']), 'size' : (j['length']/500),
                  'pen' : None} for j in six.itervalues(covDict) if j['length'] > size_to_draw]

print('selected %d points larger than %d bps to draw' % (len(spots_to_draw), size_to_draw))

# just plotting larger points to speed things up but the ROI still selects from all points

print("*** Adding Spots to Window ***")

##########################################################################################
## add gui
##########################################################################################

#TODO: add a zoom slider


#import pyqtgraph.examples
#pyqtgraph.examples.run()

# start by initializing Qt
app = QtGui.QApplication([])

# define a top-level widget to hold everything
window = QtGui.QWidget()

# create a grid layout to manage widgets
layout = QtGui.QGridLayout()
window.setLayout(layout)

# create some plot and text widgets
textItem = QtGui.QLabel("Select some contigs using the selection box")
layout.addWidget(textItem, 1, 0)

button = QtGui.QPushButton("write contigs")
layout.addWidget(button, 0, 0)

plot = pg.PlotWidget()
scatter = pg.ScatterPlotItem()
scatter.addPoints(spots=spots_to_draw)

plot.addItem(scatter)
layout.addWidget(plot, 0, 1, 3, 1)

window.show()


# add region of interest rectangle

roi = pg.RectROI(pos=[0, 0], size=[2, 2])
roi.addScaleHandle(0,1)
plot.addItem(roi)


# get points within ROI
# first define a function to pull out points from the scatter array
# function will be called when selection with ROI is finished

# def roiSelector():
#     pointCount = 0
#     point_combined_length = 0
#     x_min_bound = roi.pos()[0]
#     y_min_bound = roi.pos()[1]
#     x_max_bound = x_min_bound + roi.size()[0]
#     y_max_bound = y_min_bound + roi.size()[1]
#     ## check which points are within these bounds
#     for scaffold in covDict:
#         if covDict[scaffold]['cov'][0] > x_min_bound and covDict[scaffold]['cov'][0] < x_max_bound and covDict[scaffold]['cov'][1] > y_min_bound and covDict[scaffold]['cov'][1] < y_max_bound:
#             pointCount += 1
#             point_combined_length += covDict[scaffold]['length']
#     if len(scaffold) > 0:
#         print('total points selected:', pointCount)
#         print('length of contigs (bps):', int(point_combined_length))
#         textItem.setText('you have selected %s contigs' % pointCount)
#         #contig_length_view.setText('length of contigs (bps):')

def roiSelector():
    # roiShape = roi.mapToItem(scatter, roi.shape())
    # selected = [pt for pt in spots_to_draw["pos"] if roiShape.contains(pt)]
    # print(selected)
    print('hi')

#TODO: create module to estimate genome coverage, etc.

# this is a 'signal' in pyqtgraph used to call the function

roi.sigRegionChangeFinished.connect(roiSelector)

# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
