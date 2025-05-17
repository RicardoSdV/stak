"""
This is the interface of stak, all callables intended to be called from outside
this module should be imported from here.

Callables to be called from code are in the callFromCodeInterface which can be
wildcard imported: from (...)stak import * or in the usual way.

Callables intended for shell use can be added to __builtins__ for easy calling
by calling jamInterfaceIntoBuiltins.
"""

from .block00_typing import *
from .block02_settingObj import so
from .block04_log import labelLogs, clearLogs
from .block05_pathOps import removePrintDir
from .block07_creatingMroCallChains import omrolocs
from .block08_joinSplitLinks import omropocs
from .block09_dataLinks import firstFrameAndData, omrolocsalad, firstFrameAndDataAndLocals
from .block10_tracing import delTrace, setTrace
from .block14_saveOps import saveAll
from .z_utils import E

## Shell Aliases
s = save = saveAll
l = label = labelLogs
c = clear = clearLogs
rmp = rmPrint = removePrintDir
rs = reloadSettings = so.reload

callFromShellInterface = (
    's', 'save', 'saveAll',
    'l', 'label', 'labelLogs',
    'c', 'clear', 'clearLogs',
    'rmp', 'rmPrint', 'removePrintDir',
    'rs', 'reloadSettings',
)

## Code Aliases
ffad = firstFrameAndData
ffadal = firstFrameAndDataAndLocals

callFromCodeInterface = (
    'omropocs',
    'omrolocs',
    'omrolocsalad',
    'ffad',
    'ffadal',
    'setTrace',
    'delTrace',
)

__all__ = callFromCodeInterface


def jamInterfaceIntoBuiltins(interfaceNames=callFromShellInterface):  # type: (Itrb[str]) -> None
    import __builtin__
    from sys import modules

    _globals = globals()
    reloading = __name__ in modules
    for name in interfaceNames:
        if reloading or not hasattr(__builtin__, name):
            setattr(__builtin__, name, _globals[name])
        else:
            E('COLLISION!', name=name)
