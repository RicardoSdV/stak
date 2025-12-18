"""
This is the interface of stak, all callables intended to be called from outside
this module should be imported from here. They are all wrapped to be able to reload.

Callables to be called from code are in the callFromCodeInterface which can be
wildcard imported: from (...)stak import * or in the usual way.

Callables intended for shell use can be added to __builtins__ for easy calling
by calling jamInterfaceIntoBuiltins.
"""

from lib.packageUnite import loadUnited
stak = loadUnited()
stak.onStakLoads()

## Shell Aliases
s   = saveAll        = stak.saveAll
lar = loadAndResave  = stak.loadAndResave
l   = labelLogs      = stak.labelLogs
c   = clearLogs      = stak.clearLogs
rmp = removePrintDir = stak.removePrintDir
rs  = reloadSettings = stak.reloadSettings
pt  = printTimings   = stak.printTimings

# Code Aliases
ffad         = stak.firstFrameAndData
ffadal       = stak.firstFrameAndDataAndLocals
omropocs     = stak.omropocs
omrorocs     = stak.omrorocs
omrolocs     = stak.omrolocs
omrolpocs    = stak.omrolpocs
omropocsalad = stak.omropocsalad
omrolocsalad = stak.omrolocsalad
omrolocsalar = stak.omrolocsalar

## Shell & Code Aliases.
st = setTrace = stak.setTrace
dt = delTrace = stak.delTrace

def stakMe():
    """ omrolocs all callables in file """
    print 'Implement me lazy bastard!'

callFromShellInterface = (
    's'  , 'saveAll',
    'l'  , 'labelLogs',
    'c'  , 'clearLogs',
    'rmp', 'removePrintDir',
    'rs' , 'reloadSettings',
    'lar', 'loadAndResave',
    'st' , 'setTrace',
    'dt' , 'delTrace',
    'pt',  'printTimings',
)

callFromCodeInterface = (
    'omropocs',
    'omrorocs',
    'omrolocs',
    'omrolpocs',
    'omrolocsalad',
    'omropocsalad',
    'omrolocsalar',
    'ffad',
    'ffadal',
    'setTrace',
    'delTrace',
)

__all__ = callFromCodeInterface

stak.jamInterfaceIntoBuiltins(callFromShellInterface, globals())
