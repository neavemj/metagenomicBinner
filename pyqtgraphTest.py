#!/usr/bin/env python

# -*- coding: utf-8 -*-
"""
Matt's metagenomic binner using pyqtgraph
Graphical interface for selecting contigs and checking genome completeness

"""

# imports

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

## add gui

app = QtGui.QApplication([])
window = QtGui.QMainWindow()
window.resize(1000, 800)
view = pg.GraphicsLayoutWidget()
window.setCentralWidget(view)
window.show()
window.setWindowTitle('metagenomicBinner')

## create area for graph and add a label to display the statistics

window1 = view.addPlot()
window2 = view.addLabel("You have not selected any points")

# data for plots

mattsArray = np.arange(300)

scatter1 = pg.ScatterPlotItem()
scatter1.addPoints(mattsArray, mattsArray)
window1.addItem(scatter1)

# add region of interest rectangle

roi = pg.RectROI(pos=[10, 10], size=[20, 20])
window1.addItem(roi)

# get points within ROI
# first define a function to pull out points from the scatter array
# function will be called when selection with ROI is finished

def matts_function():
    pointCount = 0
    x_min_bound = roi.pos()[0]
    y_min_bound = roi.pos()[1]
    x_max_bound = x_min_bound + roi.size()[0]
    y_max_bound = y_min_bound + roi.size()[1]
    ## check which points are within these bounds
    for pts in mattsArray:
        if pts > x_min_bound and pts < x_max_bound and pts > y_min_bound and pts < y_max_bound:
            pointCount += 1
    if pts > 0:
        print 'total points selected:', pointCount
        window2.setText('you have selected %s points' % pointCount)

# this is a 'signal' in pyqtgraph used to call the function

roi.sigRegionChangeFinished.connect(matts_function)


# Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()