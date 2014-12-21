__author__ = 'neavemj'

# import data module for coverage, gc, kmer and essential gene files
# Matthew J. Neave 21.12.14

#TODO: import gc content, kmer dist, essential gene stuff - then combine into 1 dict?
#TODO: currently importing coverage and length from same file - when I write the modules could output results differently

def coverageData(cov1, cov2):

    #TODO: might have to make coverage 0 if not present, then change log transform to try / except to avoid error

    cov1Dict = {}
    cov2Dict = {}
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
            cov1Dict[scaffold] = {'cov' : coverage, 'length' : length}
        except:
            continue
            exceptionCov1 += 1


    for line in cov2:
        try:
            cols = line.split(',')
            scaffold = str(cols[0])
            coverage = float(cols[1])
            length = float(cols[2])
            cov2Dict[scaffold] = {'cov' : coverage, 'length' : length}
        except:
            continue
            exceptionCov2 += 1

    # put dictionaries together into a dict for plotting, ensuring coverage is for the correct scaffold
    # the dictionaries are of unequal length because some scaffs have 0 coverage (and no row) for a particular treatment

    for j in cov1Dict:
        if j in cov2Dict:
            coverage = [cov1Dict[j]['cov'], cov2Dict[j]['cov']]
            covDict[j] = coverage
        else:
            covDict[j] = [cov1Dict[j]['cov'], 0.01]


    for j in cov2Dict:
        if j not in covDict:
            covDict[j] = [0.01, cov2Dict[j]['cov']]

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