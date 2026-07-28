"""
This is the interface of stak, all callables intended to be called from outside
this module should be imported from here. They are all wrapped to be able to reload.

Callables to be called from code are in the callFromCodeInterface which can be
wildcard imported: from (...)stak import * or in the usual way.

Callables intended for shell use can be added to __builtins__ for easy calling
by calling jamInterfaceIntoBuiltins.
"""
from sys import modules as sysModules
from .save.ops import saveAll
from .make.log import labelLogs, clearLogs
from .utils.paths import removePrintDir
from .meta import reloadConfig
from .perf import printTimings
from .lib import timeClock
from .make.links import (
    firstFrameAndData, firstFrameAndDataAndLocals, omropocs, omrolocs, omrolocsalad,
    omrolocsalar, omrolpocs, omropocsalad, omrorocs)
from .make.trace import setTrace, delTrace

start = timeClock()

## Shell Aliases
s   = saveAll
l   = labelLogs
c   = clearLogs
rmp = removePrintDir
rs  = reloadConfig
pt  = printTimings

# Code Aliases
ffad   = firstFrameAndData
ffadal = firstFrameAndDataAndLocals

## Shell & Code Aliases.
st = setTrace
dt = delTrace

callFromShellInterface = (
    's'  , 'saveAll',
    'l'  , 'labelLogs',
    'c'  , 'clearLogs',
    'rmp', 'removePrintDir',
    'rc' , 'reloadConfig',
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
