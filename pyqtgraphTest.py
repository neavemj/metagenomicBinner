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
window1.setLabel(axis='left', text='Hello!!')
window2 = view.addLabel("You have not selected any points")

# data for plots

AHtCov = open("end11AHt.coverage.csv")
AHphCov = open("end43AHpf.coverage.csv")

covDict = {}
scaffsFound = 0
exceptions1 = 0
exceptions2 = 0

#TODO: make numpy array containing scatterplot points
#TODO: subsample data for display

# create dictionaries for the coverage values. Key is scaffold name, value is coverage.

for line in AHtCov:
    try:
        cols = line.split(',')
        scaffold = str(cols[0])
        coverage = float(cols[1])
        covDict[scaffold] = [coverage]
    except:
        exceptions1 += 1
        continue


for line in AHphCov:
    try:
        cols = line.split(',')
        scaffold = str(cols[0])
        coverage = float(cols[1])
        if scaffold in covDict:
            covDict[scaffold].append(coverage)
            scaffsFound += 1
        else:
            covDict[scaffold] = [0.1, coverage]
    except:
        exceptions2 += 1
        continue


# put dictionaries together into an array for plotting, ensuring coverage is for the correct scaffold
# the dictionaries are of unequal length because some scaffs have 0 coverage (and no row) for a particular treatment

#TODO: somehow need to get complete set of scaffolds that are in the dictionaries. Might have to make list of dicts from my overal dict

#mattsArray = np.arange(300)

scatter1 = pg.ScatterPlotItem()
scatter1.addPoints(spots=covDict)
window1.addItem(scatter1)

# add region of interest rectangle

roi = pg.RectROI(pos=[10, 10], size=[20, 20])
roi.addScaleHandle(0,1)
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