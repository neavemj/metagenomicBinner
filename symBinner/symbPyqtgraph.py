#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Matt's metagenomic binner using pyqtgraph
Graphical interface module for selecting contigs and checking genome completeness

"""

# imports

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np
import symbData, symbHelper, symbROIselector


# get data and import using symbData.py module

AHtCov = open("../end11AHt.coverage.csv")
AHphCov = open("../end43AHpf.coverage.csv")
AHgc = open("../end43AHt+pf.gc.tab")

dataResults = symbData.getCombinedData(AHtCov, AHphCov, AHgc)
covDict = dataResults[0]
maxGCcontent = dataResults[1]
minGCcontent = dataResults[2]
avgGCcontent = dataResults[3]

#import pyqtgraph.examples
#pyqtgraph.examples.run()

# create a color map gradient for coloring my gc points
#TODO: note this (gradient coloring) seems to take a while to run for some reason. Could round to nearest point to reduce number of computations?
#TODO: could also add key for gc content colors?

#python -m cProfile -s cumulative symbPyqtgraph.py

#give points 10 colours evenly spaced between the calculated max and min gc content

print "*** Generating GC Colour Profiles ***"

point = np.linspace(minGCcontent, maxGCcontent, 10)
print 'gc range:', minGCcontent, avgGCcontent, maxGCcontent
color = np.array([[231,246,189],[102,6,95],[229,82,7],[74,94,20],[249,149,161],[38,241,240],[103,20,27],[253,203,120],[250,77,137],[248,55,66]], dtype=np.ubyte)
colmap = pg.ColorMap(point, color)

# use list comprehension to add my data points to a list of dictionaries as required by pyqtgraph
# divided length by 500 because this looked about right but should come up with something better
# spots to draw is those greater than 1000 (after dividing by 500 in previous step)

print "*** Creating Spot Dictionaries ***"

spots = [{'pos': np.log(j['cov']), 'data': 1, 'brush' : colmap.map(j['gc']), 'size' : (j['length']/500), 'pen' : None} for j in covDict.itervalues()]

size_to_draw = 2000
spots_to_draw = [j for j in spots if j['size'] > (size_to_draw / 500)]

print 'selected %d points larger than %d bps to draw' % (len(spots_to_draw), size_to_draw)

# just plotting larger points to speed things up but the ROI still selects from all points

print "*** Adding Spots to Window ***"

## add gui

#TODO: add a zoom slider

app = QtGui.QApplication([])
window = QtGui.QMainWindow()
window.resize(1000, 800)
window.show()
window.setWindowTitle('metagenomicBinner')

#view = pg.GraphicsLayoutWidget()
cw = QtGui.QWidget()
window.setCentralWidget(cw)

# ## create area for graph and add a label to display the statistics
##???
l = QtGui.QGridLayout()
cw.setLayout(l)
l.setSpacing(0)

v = pg.GraphicsView()
vb = pg.ViewBox()
vb.setAspectLocked()
v.setCentralItem(vb)
l.addWidget(v, 0, 0)

plot = pg.PlotWidget()

w = pg.ScatterPlotItem()
w.addPoints(spots=spots_to_draw)

plot.addItem(w)

l.addWidget(plot, 0, 1)

#window1.setClipToView(clip=True)
#window1.setLabels(left='coverage 1 (log scale)', bottom='coverage 2 (log scale)')

#scatter1 = pg.ScatterPlotItem()
#scatter1.addPoints(spots=spots_to_draw)
#v.addItem(scatter1)

# # add region of interest rectangle
#
# roi = pg.RectROI(pos=[0, 0], size=[2, 2])
# roi.addScaleHandle(0,1)
# window1.addItem(roi)
#
# window2 = view.addLabel("Welcome to symbBinner")
# contig_length_view = view.addLabel()
#
# # get points within ROI
# # first define a function to pull out points from the scatter array
# # function will be called when selection with ROI is finished
#
# def roiSelector():
#     pointCount = 0
#     point_combined_length = 0
#     x_min_bound = roi.pos()[0]
#     y_min_bound = roi.pos()[1]
#     x_max_bound = x_min_bound + roi.size()[0]
#     y_max_bound = y_min_bound + roi.size()[1]
#     ## check which points are within these bounds
#     for pts in spots:
#         if pts['pos'][0] > x_min_bound and pts['pos'][0] < x_max_bound and pts['pos'][1] > y_min_bound and pts['pos'][1] < y_max_bound:
#             pointCount += 1
#             point_combined_length += pts['size']
#     if pts > 0:
#         print 'total points selected:', pointCount
#         print 'length of contigs (bps):', int(point_combined_length)
#         window2.setText('you have selected %s points' % pointCount)
#         contig_length_view.setText('length of contigs (bps):')
#
# #TODO: create module to estimate genome coverage, etc.
#
# # this is a 'signal' in pyqtgraph used to call the function
#
# roi.sigRegionChangeFinished.connect(roiSelector)


# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
