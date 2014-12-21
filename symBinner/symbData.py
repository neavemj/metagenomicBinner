__author__ = 'neavemj'

# import data module for coverage, gc, kmer and essential gene files
# Matthew J. Neave 21.12.14


def coverageData(cov1, cov2):

    cov1Dict = {}
    cov2Dict = {}
    covDict = {}

    # create dictionaries for the coverage values. Key is scaffold name, value is coverage.

    for line in cov1:
        try:
            cols = line.split(',')
            scaffold = str(cols[0])
            coverage = float(cols[1])
            cov1Dict[scaffold] = coverage
        except:
            continue


    for line in cov2:
        try:
            cols = line.split(',')
            scaffold = str(cols[0])
            coverage = float(cols[1])
            cov2Dict[scaffold] = coverage
        except:
            continue


    # put dictionaries together into a dict for plotting, ensuring coverage is for the correct scaffold
    # the dictionaries are of unequal length because some scaffs have 0 coverage (and no row) for a particular treatment

    for j in cov1Dict:
        if j in cov2Dict:
            coverage = [cov1Dict[j], cov2Dict[j]]
            covDict[j] = coverage
        else:
            covDict[j] = [cov1Dict[j], 0.01]


    for j in cov2Dict:
        if j not in covDict:
            covDict[j] = [0.01, cov2Dict[j]]

    print 'covDict length', len(covDict)
    return covDict