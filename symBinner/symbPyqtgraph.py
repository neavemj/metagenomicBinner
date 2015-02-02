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
import symbData, symbHelper

## add gui

#TODO: add a zoom slider

app = QtGui.QApplication([])
window = QtGui.QMainWindow()
window.resize(1000, 800)
view = pg.GraphicsLayoutWidget()
window.setCentralWidget(view)
window.show()
window.setWindowTitle('metagenomicBinner')

# ## create area for graph and add a label to display the statistics

window1 = view.addPlot()
window1.setClipToView(clip=True)
window1.setLabels(left='coverage 1 (log scale)', bottom='coverage 2 (log scale)')
window2 = view.addLabel("Welcome to symbBinner")

# get data and import using symbData.py module

AHtCov = open("../end11AHt.coverage.csv")
AHphCov = open("../end43AHpf.coverage.csv")
AHgc = open("../end43AHt+pf.gc.tab")

dataResults = symbData.getCombinedData(AHtCov, AHphCov, AHgc)
covDict = dataResults[0]
maxGCcontent = dataResults[1]
minGCcontent = dataResults[2]
avgGCcontent = dataResults[3]

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

print "*** Creating Spot Dictionaries ***"

spots = [{'pos': np.log(j['cov']), 'data': 1, 'brush' : colmap.map(j['gc']), 'size' : (j['length']/500), 'pen' : None} for j in covDict.itervalues()]

# just plotting the first 1,000 points to speed things up but the ROI still selects from all points

#TODO: draw points according to length. At the moment they are being randomly pulled from a dictionary

print "*** Adding Spots to Window ***"

scatter1 = pg.ScatterPlotItem()
scatter1.addPoints(spots=spots[:1000])
window1.addItem(scatter1)

# add region of interest rectangle

roi = pg.RectROI(pos=[0, 0], size=[2, 2])
roi.addScaleHandle(0,1)
window1.addItem(roi)

# get points within ROI
# first define a function to pull out points from the scatter array
# function will be called when selection with ROI is finished

#TODO: create module to estimate genome coverage, etc.

def roiSelector():
    pointCount = 0
    x_min_bound = roi.pos()[0]
    y_min_bound = roi.pos()[1]
    x_max_bound = x_min_bound + roi.size()[0]
    y_max_bound = y_min_bound + roi.size()[1]
    ## check which points are within these bounds
    for pts in spots:
        if pts['pos'][0] > x_min_bound and pts['pos'][0] < x_max_bound and pts['pos'][1] > y_min_bound and pts['pos'][1] < y_max_bound:
            pointCount += 1
    if pts > 0:
        print 'total points selected:', pointCount
        window2.setText('you have selected %s points' % pointCount)

#TODO: make use of sigClicked? To give info about specific point?

# this is a 'signal' in pyqtgraph used to call the function

roi.sigRegionChangeFinished.connect(roiSelector)


# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
