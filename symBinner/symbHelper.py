__author__ = 'neave'

# helper functions
# Matthew J. Neave 21.1.15

def getMaxDictValue(targetDict):
    "use this to get max gc value for figuring out range of point colours"
    targetValues = list(targetDict.values())
    return max(targetValues)

def getMinDictValue(targetDict):
    "use this to get max gc value for figuring out range of point colours"
    targetValues = list(targetDict.values())
    return min(targetValues)

def getAverageDictValue(targetDict):
    "use this to get max gc value for figuring out range of point colours"
    targetValues = list(targetDict.values())
    return sum(targetValues) / len(targetDict)