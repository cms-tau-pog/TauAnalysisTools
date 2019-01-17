# def createFilePath(filePath):
#    import TauAnalysis.Configuration.tools.eos as eos
#    try:
#        eos.lsl(filePath)
#    except IOError:
#        print "filePath = %s does not yet exist, creating it." % filePath
#        eos.mkdir(filePath)
#        time.sleep(3)
#    eos.chmod(filePath, 777)

import subprocess
import json


# Functions for skimming scripts creation
def runcommand(commandline):
    """Run and print a specific command."""
    print(commandline)
    subprocess.call(commandline, shell=True)


# Functions for training scripts creation
def replaceCommomns(commonName, commonList, singleList):
    if commonName in singleList:
        singleList[:] = [x for x in singleList if x != commonName]
        singleList[:] = commonList + singleList


def _decode_list(data):
    rv = []
    for item in data:
        if isinstance(item, unicode):
            item = item.encode('utf-8')
        elif isinstance(item, list):
            item = _decode_list(item)
        elif isinstance(item, dict):
            item = _decode_dict(item)
        rv.append(item)
    return rv


def _decode_dict(data):
    rv = {}
    for key, value in data.iteritems():
        if isinstance(key, unicode):
            key = key.encode('utf-8')
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        elif isinstance(value, list):
            value = _decode_list(value)
        elif isinstance(value, dict):
            value = _decode_dict(value)
        rv[key] = value
    return rv


def getTrainingSets(trainingsets='trainingsets.json'):
    with open(trainingsets) as f:
        ff = json.load(f, object_hook=_decode_dict)

    preselections = ff['preselections']
    cutDiscriminatorsAll = ff['cutDiscriminators']
    trainings = ff['trainings']
    commonsDict = {
        'commonOtherVariables': ff['commonOtherVariables'],
        'commonSpectatorVariables': ff['commonSpectatorVariables'],
    }

    for cval in cutDiscriminatorsAll.values():
        cval["preselection"] = preselections[cval["preselection"]]

    for tval in trainings.values():
        tval["preselection"] = preselections[tval["preselection"]]
        replaceCommomns('commonOtherVariables', commonsDict['commonOtherVariables'], tval["otherVariables"])
        replaceCommomns('commonSpectatorVariables', commonsDict['commonSpectatorVariables'], tval["spectatorVariables"])

    return preselections, cutDiscriminatorsAll, trainings, commonsDict
