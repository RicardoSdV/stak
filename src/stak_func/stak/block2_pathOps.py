from os import makedirs
from os.path import join, isdir, splitext

from block1_commonData import *

# Dynamic path generators
def pathDirPrint(): yield join(rootDir, taskDir, printDir)
def pathDirPrimi(): yield join(next(pathDirPrint()), primitivesDir)
def pathDirVari (): yield join(next(pathDirPrint()), variantsDir)
def pathLogStak (): yield join(next(pathDirPrimi()), stakLogFile)
def pathLogsStd (): return (join(next(pathDirPrimi()), logName) for logName in stdLogFiles)
def pathLogTrace(): yield join(next(pathDirPrimi()), traceLogFile)

def makeDirPaths():
    if not isdir(next(pathDirPrimi())):
        makedirs(next(pathDirPrimi()))
    if not isdir(next(pathDirVari())):
        makedirs(next(pathDirVari()))

def addSuffix(logName, suffix):  # type: (str, str) -> str
    name, ext = splitext(logName)
    return '{}{}{}'.format(name, suffix, ext)
