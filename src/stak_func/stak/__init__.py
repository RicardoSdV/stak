"""
This is the interface of stak, all callables intended to be called from outside
this module should be imported from here.

For convenience the entire interface can be imported as: from (...)stak import *
Or, in the usual way.
"""
import __builtin__

from .block00_typing import *
from .block01_settings import eventLabels
from .block02_commonData import reloadData
from .block03_log import labelLog, clearLog, log
from .block04_pathOps import removePrintDir
from .block06_creatingMroCallChains import omropocs, omrolocs
from .block07_autoLocals import dataAndFirstFrame, autoLocals, omrolocsalad
from .block08_tracing import setTrace, delTrace
from .block11_savingAllLogs import saveAll


def reloadSettings():
    from . import block01_settings
    reload(block01_settings)


## Aliases
s = save = saveAll
l = label = labelLog
ls = labels = eventLabels
rp = rmp = rmPrint = removePrintDir
c = clear = clearLog
rs = rls = reloadSettings
daff = dataAndFirstFrame

callFromShellInterface = (
    's', 'save', 'saveAll',
    'l', 'label', 'labelLog',
    'ls', 'labels', 'eventLabels',
    'rp', 'rmp', 'rmPrint', 'removePrintDir',
    'c', 'clear', 'clearLog',
    'rs', 'rls', 'reloadSettings',
)

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

def jamInterfaceIntoBuiltins(names=callFromShellInterface, _locals=locals()):
    # type: (Tup[str, ...], Dic[str, Any]) -> None

    def printLog():
        for entry in log:
            print entry

    setattr(__builtin__, 'printLog', printLog)

    for name in names:
        if not hasattr(__builtin__, name):
            setattr(__builtin__, name, _locals[name])
        else:
            print 'ERROR: COLLISION! :: {}'.format(name)

def getModules():  # type: () -> Lst[ModuleType]
    from . import block00_typing
    from . import block01_settings
    from . import block02_commonData
    from . import block03_log
    from . import block04_pathOps
    from . import block05_stampOps
    from . import block06_creatingMroCallChains
    from . import block07_autoLocals
    from . import block08_tracing
    from . import block09_compression
    from . import block10_parsingStdLogs
    from . import block11_savingAllLogs

    return locals().values()



