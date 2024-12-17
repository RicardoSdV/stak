"""
This is the interface of stak, all callables intended to be called from outside
this module should be imported from here.

For convenience the entire interface can be imported as: from (...)stak import *
Or, in the usual way.
"""
import __builtin__

from .block01_settings import eventLabels
from .block02_commonData import reloadData
from .block03_log import labelLog, clearLog
from .block04_pathOps import removePrintDir
from .block06_creatingMroCallChains import omropocs, omrolocs
from .block07_autoLocals import data, autoLocals, omrolocsalad
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

__all__ = (
    # Call from shell
    's', 'save', 'saveAll',
    'l', 'label', 'labelLog',
    'ls', 'labels', 'eventLabels',
    'rp', 'rmp', 'rmPrint', 'removePrintDir',
    'c', 'clear', 'clearLog',
    'rs', 'rls', 'reloadSettings',

    # Call from code
    'omropocs',
    'omrolocs',
    'omrolocsalad',
    'data',
    'autoLocals',
    'setTrace',
    'delTrace',
)

_locals = locals()
for name in __all__:
    if not hasattr(__builtin__, name):
        setattr(__builtin__, name, _locals[name])
    else:
        print 'ERROR: COLISION! :: {}'.format(name)
