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
import symbData

## add gui

app = QtGui.QApplication([])
window = QtGui.QMainWindow()
window.resize(1000, 800)
view = pg.GraphicsLayoutWidget()
window.setCentralWidget(view)
window.show()
window.setWindowTitle('metagenomicBinner')

# ## create area for graph and add a label to display the statistics

window1 = view.addPlot()
window1.setDownsampling(ds=3000, mode='subsample')
window1.setClipToView(clip=True)
window1.setLabels(left='physical coverage (log)', bottom='total coverage (log)')
window2 = view.addLabel("You have not selected any points")

# get data and import using symbData.py module

AHtCov = open("/Users/neavemj/PycharmProjects/metagenomicBinner/end11AHt.coverage.csv")
AHphCov = open("/Users/neavemj/PycharmProjects/metagenomicBinner/end43AHpf.coverage.csv")
AHgc = open("/Users/neavemj/PycharmProjects/metagenomicBinner/end43AHt+pf.gc.tab")

covDict = symbData.coverageData(AHtCov, AHphCov)
gcDict = symbData.gcData(AHgc)

#pyqtgraph.examples.run()

# use list comprehension to add my data points to a list of dictionaries as required by pyqtgraph

spots = [{'pos': np.log(j['cov']), 'data': 1, 'brush' : 6, 'size' : j['length']} for j in covDict.itervalues()] + [{'pos': [0,0], 'data': 1}]

# just plotting the first 1,000 points to speed things up but the ROI still selects from all points

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