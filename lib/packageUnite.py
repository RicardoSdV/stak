""" Make a single virtual module out of all the modules found in the package. """
from itertools import chain
from traceback import print_stack
from types import ModuleType
from sys import modules as sysModules, _getframe as sysGetFrame, exit as sysExit
from os import listdir as osListDir
from os.path import join as osPathJoin, split as osPathSplit

import typing
if typing.TYPE_CHECKING:
    from typing import Dict, Sequence as Seq, Tuple, Any, Iterable as Iterb, Container
    from types import FrameType

LOG = True
_META_KEYS = {'__doc__', '__name__', '__file__', '__package__', '__unitedModNames__', '__unitedModPaths__'}


def delStatics(_dict, statics):
    # type: (Dict, Container) -> None
    for k in _dict.keys():
        if k in statics:
            del _dict[k]

class DictWithStatics(dict):
    def __init__(self, statics, *args, **kwargs):
        # type: (Container[str], *Any, **Any) -> None
        super(DictWithStatics, self).__init__(*args, **kwargs)
        self.statics = statics

    def __setitem__(self, key, value):
        if key not in self.statics:
            super(DictWithStatics, self).__setitem__(key, value)

    def __delitem__(self, key):
        if key not in self.statics:
            super(DictWithStatics, self).__delitem__(key)

    def update(self, __m, **kwargs):
        delStatics(__m, self.statics)
        delStatics(kwargs, self.statics)
        super(DictWithStatics, self).update(__m, **kwargs)

def reloadModByNameGetDiff(unitedModDotPath, moduleName, staticNames=()):
    # type: (str, str, Iterb[str]) -> Tuple[Dict[str, Any], Dict[str, Any]]
    unitedDict = sysModules[unitedModDotPath].__dict__
    newNames = reloadModByName(unitedModDotPath, moduleName, staticNames)
    oldNames = {k: unitedDict.get(k) for k in newNames}
    return oldNames, newNames

def reloadModByName(unitedModDotPath, name, staticNames=()):
    # type: (str, str, Iterb[str]) -> Dict[str, Any]
    return reloadModsByNames(unitedModDotPath, (name, ), staticNames)

def reloadModsByNames(unitedModDotPath, names, staticNames=()):
    # type: (str, Iterb[str], Iterb[str]) -> Dict[str, Any]
    unitedDict = sysModules[unitedModDotPath].__dict__
    unitedModNames = unitedDict['__unitedModNames__']
    staticModNames = (n for n in unitedModNames if n not in names)
    return loadModules(unitedDict, staticNames, staticModNames)

def loadModules(unitedDict, staticNames=(), staticModNames=()):
    # type: (Dict[str, Any], Iterb[str], Iterb[str]) -> Dict[str, Any]
    """ If you call this directly make sure to have populated the unitedDict with _META_KEYS & valid values.
    """
    staticNames = set(staticNames)
    staticModNames = set(staticModNames)

    # Extract metadata to keep it static.
    staticKeys = staticNames | _META_KEYS
    staticNames = {k: unitedDict[k] for k in staticKeys}
    unitedDict = DictWithStatics(staticKeys, staticNames)

    # Read, compile & exec code in paths
    modNames = staticNames['__unitedModNames__']
    modPaths = staticNames['__unitedModPaths__']
    for name, path in zip(modNames, modPaths):
        with open(path, 'r') as f:
            src = f.read()
        code = compile(src, path, 'exec')
        exec(code, unitedDict)

    return unitedDict.copy()  # Copy to return a standard dict

def reloadUnited(unitedDotPath, staticNames=(), staticModNames=()):
    # type: (str, Iterb[str], Iterb[str]) -> None

    unitedDict = sysModules[unitedDotPath].__dict__
    newNames = loadModules(unitedDict, staticNames, staticModNames)
    unitedDict.update(newNames)

def loadUnited(
        unitedModuleName='__united__', prefix='', suffix='', ext='.py',
        ignorePaths=('__init__.py', ), overridePaths=(), overrideNames=(),
        frameNum=1, sliceArgs=(1, 2, 1), nameSplitChar='_'
):  # type: (str, str, str, str, Seq[str], Seq[str], Seq[str], int, Tuple[int, int, int], str) -> ModuleType

    # Get paths from frame
    calledFromFrame = sysGetFrame(frameNum)  # type: FrameType
    frameGlobals = calledFromFrame.f_globals  # type: Dict[str: ...]
    packageDotPath = frameGlobals['__name__']  # type: str
    unitedDotPath = packageDotPath + '.' + unitedModuleName
    frameCode = calledFromFrame.f_code
    fileName = frameCode.co_filename
    packagePath = osPathSplit(fileName)[0]
    unitedPath = osPathJoin(packagePath, unitedModuleName) + ext

    # Create United Module
    unitedModule = ModuleType(unitedDotPath)
    sysModules[unitedDotPath] = unitedModule

    # Find sub-module paths, or use the overrides.
    if overridePaths and overrideNames:
        if len(overridePaths) != len(overrideNames):
            print 'ERROR: Each path must correspond to its name', overridePaths, overrideNames
            sysExit()
        absPaths = list(overridePaths); modNames = list(overrideNames)
    else:
        absPaths = []; absPathsApp = absPaths.append
        modNames = []; modNamesApp = modNames.append

        suffixAndExt = suffix + ext
        lenPrefix = len(prefix)
        nLenSuffixAndExt = -len(suffixAndExt)

        for fileName in sorted(osListDir(packagePath)):
            if (
                    fileName[:lenPrefix] != prefix or
                    fileName[nLenSuffixAndExt:] != suffixAndExt or
                    any(fileName.endswith(ignorePath) for ignorePath in ignorePaths)
            ):
                continue

            absFilePath = osPathJoin(packagePath, fileName)
            absPathsApp(absFilePath)

            modName = fileName[lenPrefix:nLenSuffixAndExt]
            if nameSplitChar:
                start, stop, step = sliceArgs
                modName = nameSplitChar.join(modName.split(nameSplitChar)[start: stop: step])

            modNamesApp(modName)

    # Populate module metadata
    unitedDict = unitedModule.__dict__
    unitedDict['__doc__'] = 'Virtual Module combining all the modules of package %s' % packageDotPath
    unitedDict['__name__'] = unitedDotPath
    unitedDict['__file__'] = unitedPath
    unitedDict['__package__'] = packageDotPath
    unitedDict['__unitedModPaths__'] = absPaths
    unitedDict['__unitedModNames__'] = modNames

    # Read, compile & exec submodules
    newNames = loadModules(unitedDict)
    unitedDict.update(newNames)

    return unitedModule
