__author__ = 'neavemj'

# import data module for coverage, gc, kmer and essential gene files
# Matthew J. Neave 21.12.14

#TODO: import gc content, kmer dist, essential gene stuff - then combine into 1 dict?
#TODO: currently importing coverage and length from same file - when I write the modules could output results differently

def coverageData(cov1, cov2):

    #TODO: might have to make coverage 0 if not present, then change log transform to try / except to avoid error

    covDict1 = {}
    covDict2 = {}
    covDict = {}
    exceptionCov1 = 0
    exceptionCov2 = 0

    # create dictionary containing key as scaffold name, then values are cov dict and length dict

    for line in cov1:
        try:
            cols = line.split(',')
            scaffold = str(cols[0])
            coverage = float(cols[1])
            length = float(cols[2])
            covDict1[scaffold] = {'cov' : coverage, 'length' : length}
        except:
            continue
            exceptionCov1 += 1


    for line in cov2:
        try:
            cols = line.split(',')
            scaffold = str(cols[0])
            coverage = float(cols[1])
            length = float(cols[2])
            covDict2[scaffold] = {'cov' : coverage, 'length' : length}
        except:
            continue
            exceptionCov2 += 1

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

    print 'covDict1 exceptions', exceptionCov1
    print 'covDict2 exceptions', exceptionCov2
    print 'covDict length', len(covDict)
    return covDict


def gcData(gcFile):

    gcException = 0
    gcDict = {}

    for line in gcFile:
        try:
            cols = line.split()
            scaffold = str(cols[0])
            gc = float(cols[1])
            gcDict[scaffold] = gc
        except:
            continue
            gcException += 1

    print 'gcExceptions', gcException
    print 'gcDict length', len(gcDict)
    return gcDict

def getCombinedData(cov1, cov2, gcFile):
    covData = coverageData(cov1, cov2)
    gcInfo = gcData(gcFile)
    combData = {}
    nonmatches = 0

    for key in gcInfo:
        if key in covData:
            combData[key] = {'cov' : covData[key]['cov'], 'length' : covData[key]['length'], 'gc' : gcInfo[key]}
        else:
            nonmatches += 1

    print 'nonmatches', nonmatches
    print 'combData length', len(combData)
    return combData