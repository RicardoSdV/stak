""" For this to work properly imports must follow this format: from .'block name' import 'comma, separated, names'
except the imports from excluded blocks such as typing.
"""
from collections import defaultdict
from os.path import join

from .block00_typing import *
from .block06_pathOps import getPackageName
from .z_utils import read, readSortedBlockNames


excludedBlocks = {'block00_typing'}


def readReloadableBlockNames(path):
    yield '__init__'
    for name in readSortedBlockNames(path):
        name = name.rstrip('.py')
        if name not in excludedBlocks:
            yield name

def readImports(blockNames):  # type: (Tup[str, ...]) -> Dic[str, Dic[str, Lst[str]]]
    """
    :returns {
        importerBlock: {
            importedBlock: [importedNames, ...],
        }
    }
    """

    imports = {}
    for importerBlock in blockNames:
        importedNamesByOriginBlock = {}

        lines = read(join('stak', importerBlock + '.py'))
        for line in lines:

            if not (line.startswith('from ') and ' import ' in line):
                continue

            for blockName in blockNames:
                if blockName in line:
                    importedBlock = blockName
                    break
            else:
                continue

            names = line[len('from .' + importedBlock + ' import '):].split(', ')
            importedNamesByOriginBlock[importedBlock] = [name.rstrip('\n') for name in names]
        imports[importerBlock] = importedNamesByOriginBlock

    return imports

def reloadBlocks(blocks):  # type: (Dic[str, ModuleType]) -> None
    for block in blocks.itervalues():
        reload(block)

def getAliasesFromInterface(imports, interface):  # type: (Dic[str, Dic[str, Lst[str]]], Dic[str, Any]) -> Dic[str, Lst[str]]
    namesByIDs = {id(interface[n]): n for ns in imports['__init__'].itervalues() for n in ns}

    aliases = defaultdict(list)
    for alias, val in interface.iteritems():
        valID = id(val)
        if valID in namesByIDs:
            name = namesByIDs[valID]
            if name != alias:
                aliases[name].append(alias)

    return aliases

def setReloadedNames(imports, blocks):
    for importerBlockName, importedNamesByOriginBlock in imports.iteritems():
        if importerBlockName not in blocks:
            continue  # Some blocks might have never been imported, no need to reload those.

        importerBlock = blocks[importerBlockName].__dict__

        for originBlockName, importedNames in importedNamesByOriginBlock.iteritems():
            originBlock = blocks[originBlockName].__dict__

            for name in importedNames:
                importerBlock[name] = originBlock[name]

def setAliasesInInterface(aliasesByName, interface):
    for name, aliases in aliasesByName.iteritems():
        original = interface[name]
        for alias in aliases:
            interface[alias] = original

def reloadAll():
    packageName = getPackageName()

    blockNames = tuple(readReloadableBlockNames(packageName))
    imports = readImports(blockNames)
    blocks = dict(getBlocks(packageName))

    interface = blocks['stak'].__dict__
    aliasesByName = getAliasesFromInterface(imports, interface)
    reloadBlocks(blocks)

    setReloadedNames(imports, blocks)
    setAliasesInInterface(aliasesByName, interface)

    from . import jamInterfaceIntoBuiltins
    jamInterfaceIntoBuiltins(reloading=True)


# from stak import block03_reloader as r; r.getImportsFromBlocks()
