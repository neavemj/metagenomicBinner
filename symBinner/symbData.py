__author__ = 'neavemj'

# import data module for coverage, gc, kmer and essential gene files.
# Matthew J. Neave 21.12.14

import symbHelper

#TODO: import gc content, kmer dist, essential gene stuff - then combine into 1 dict?
#TODO: currently importing coverage and length from same file - when I write the modules could output results differently

def coverageData(cov1, cov2):

    #TODO: might have to make coverage 0 if not present, then change log transform to try / except to avoid error

    print "*** Reading Coverage Data ***"
    covDict1 = {}
    covDict2 = {}
    covDict = {}

    # create dictionary containing key as scaffold name, then values are cov dict and length dict
    # skip first line (header) using next

    next(cov1)
    for line in cov1:
        cols = line.split(',')
        scaffold = str(cols[0])
        coverage = float(cols[1])
        length = float(cols[2])
        covDict1[scaffold] = {'cov' : coverage, 'length' : length}


    next(cov2)
    for line in cov2:
            cols = line.split(',')
            scaffold = str(cols[0])
            coverage = float(cols[1])
            length = float(cols[2])
            covDict2[scaffold] = {'cov' : coverage, 'length' : length}

    # put dictionaries together into a dict for plotting, ensuring coverage is for the correct scaffold
    # the dictionaries are of unequal length because some scaffs have 0 coverage (and no row) for a particular treatment

    for j in covDict1:
        if j in covDict2:
            coverage = [covDict1[j]['cov'], covDict2[j]['cov']]
            covDict[j] = {'cov' : coverage, 'length' : covDict1[j]['length']}
        else:
            covDict[j] = {'cov' : [covDict1[j]['cov'], 0.01], 'length' : covDict1[j]['length']}


    for j in covDict2:
        if j not in covDict:
            covDict[j] = {'cov' : [0.01, covDict2[j]['cov']], 'length' : covDict2[j]['length']}

    print 'covDict length', len(covDict)
    return covDict


def gcData(gcFile):
    "get gc contents into dictionary plus record the max/min gc and return for later use in point colouring"

    print "*** Reading GC Content ***"
    gcDict = {}

    next(gcFile)
    for line in gcFile:
        cols = line.split()
        scaffold = str(cols[0])
        gc = float(cols[1])
        gcDict[scaffold] = gc

    maxGCvalue = symbHelper.getMaxDictValue(gcDict)
    minGCvalue = symbHelper.getMinDictValue(gcDict)
    avgGCvalue = symbHelper.getAverageDictValue(gcDict)

    print 'gcDict length', len(gcDict)
    return {'gcDict' : gcDict, 'maxGCvalue' : maxGCvalue, 'minGCvalue' : minGCvalue, 'avGCvalue' : avgGCvalue}

def getCombinedData(cov1, cov2, gcFile):
    covData = coverageData(cov1, cov2)
    returnedGCdata = gcData(gcFile)
    gcInfo = returnedGCdata['gcDict']
    combData = {}
    nonmatches = 0

    for key in gcInfo:
        if key in covData:
            combData[key] = {'cov' : covData[key]['cov'], 'length' : covData[key]['length'], 'gc' : gcInfo[key]}
        else:
            nonmatches += 1

    print 'nonmatches', nonmatches
    print 'combData length', len(combData)
    return combData, returnedGCdata['maxGCvalue'], returnedGCdata['minGCvalue'], returnedGCdata['avGCvalue']
