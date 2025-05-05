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
from .block08_creatingMroCallChains import omrolocs
from .block09_joinSplitLinks import omropocs
from .block10_dataLinks import firstFrameAndData, omrolocsalad, firstFrameAndDataAndLocals
from .block11_tracing import delTrace, setTrace
from .block16_savingAllLogs import saveAll
from .z_utils import redStr

## Shell Aliases
s = save = saveAll
l = label = labelLogs
c = clear = clearLogs
rmp = rmPrint = removePrintDir
settingsObj = so
rs = reloadSettings = so.reload

callFromShellInterface = (
    's', 'save', 'saveAll',
    'l', 'label', 'labelLogs',
    'c', 'clear', 'clearLogs',
    'rmp', 'rmPrint', 'removePrintDir',
    'so', 'settingsObj',
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
            print redStr('ERROR: COLLISION! in stak.__init__.jamInterfaceIntoBuiltins, name=%s' % name)
