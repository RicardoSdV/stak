"""
This is the interface of stak, all callables intended to be called from outside
this module should be imported from here.

For convenience the entire interface can be imported as: from (...)stak import *
Or, in the usual way.
"""
import __builtin__

from .block00_typing import *
from .block01_settings import eventLabels, printDir
from .block02_loadAndReload import run
from .block04_reloader import reloadAll
from .block05_log import labelLog, clearLog
from .block06_pathOps import removePrintDir
from .block09_creatingMroCallChains import omrolocs, omropocs
from .block10_autoLocals import dataAndFirstFrame, autoLocals, omrolocsalad
from .block11_tracing import delTrace, setTrace
from .block16_savingAllLogs import saveAll

run()

## Shell Aliases
s = save = saveAll
l = label = labelLog
ls = labels = eventLabels
pd = printDir
rp = rmp = rmPrint = removePrintDir
c = clear = clearLog
ra = reloadAll

callFromShellInterface = (
    's', 'save', 'saveAll',
    'l', 'label', 'labelLog',
    'ls', 'labels', 'eventLabels',
    'pd', 'printDir',
    'rp', 'rmp', 'rmPrint', 'removePrintDir',
    'c', 'clear', 'clearLog',
    'ra', 'reloadAll',
)


## Code Aliases
daff = dataAndFirstFrame

callFromCodeInterface = (
    'omropocs',
    'omrolocs',
    'omrolocsalad',
    'daff',
    'autoLocals',
    'setTrace',
    'delTrace',
)

__all__ = callFromCodeInterface

def jamInterfaceIntoBuiltins(interfaceNames=callFromShellInterface, reloading=False):
    # type: (Tup[str, ...], bool) -> None

    _globals = globals()
    for name in interfaceNames:
        if not hasattr(__builtin__, name) or reloading:
            setattr(__builtin__, name, _globals[name])
        else:
            print 'ERROR: COLLISION! :: {}'.format(name)

