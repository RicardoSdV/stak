"""
This is the interface of stak, all callables intended to be called from outside
this module should be imported from here.

Callables to be called from code are in the callFromCodeInterface which can be
wildcard imported: from (...)stak import * or in the usual way.

Callables intended for shell use can be added to __builtins__ for easy calling
by calling jamInterfaceIntoBuiltins.
"""

from . import z_injectors as injectors
del injectors

from         .block00_typing       import *; time = clock()
from . import block01_settings     as settings
from . import block02_settingObj   as settingsObj
from . import block03_constants    as cs
from . import block04_log          as log
from . import block05_pathOps      as pathOps
from . import block06_stampOps     as stampOps
from . import block07_callChains   as callChains
from . import block08_joinLinks    as joinSplitLinks
from . import block09_dataLinks    as dataLinks
from . import block10_tracing      as tracing
from . import block11_compression  as compression
from . import block12_parseStdLogs as parseStdLogs
from . import block13_saveOps      as saveOps
from . import block15_utils        as utils


## Shell Aliases
s   = saveAll        = saveOps.saveAll
lar = loadAndResave  = saveOps.loadAndResave
l   = labelLogs      = log.labelLogs
c   = clearLogs      = log.clearLogs
rmp = removePrintDir = pathOps.removePrintDir
rs  = reloadSettings = settingsObj.reloadSettings
pt  = printTimings   = utils.printTimings

## Code Aliases
ffad         = dataLinks.firstFrameAndData
ffadal       = dataLinks.firstFrameAndDataAndLocals
omropocs     = dataLinks.omropocs
omrolocs     = dataLinks.omrolocs
omropocsalad = dataLinks.omropocsalad
omrolocsalad = dataLinks.omrolocsalad
omrolocsalar = dataLinks.omrolocsalar

## Shell & Code Aliases.
st = setTrace = tracing.setTrace
dt = delTrace = tracing.delTrace

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
    'omrolocs',
    'omrolocsalad',
    'omropocsalad',
    'omrolocsalar',
    'ffad',
    'ffadal',
    'setTrace',
    'delTrace',
)

__all__ = callFromCodeInterface


def jamInterfaceIntoBuiltins(
        allNames       = None,                    # type: Dic[str, Any]
        interfaceNames = callFromShellInterface,  # type: Itrb[str]
        extras         = (),                      # type: Itrb[Tup[str, Any]]
):                                                # type: (...) -> None

    import __builtin__
    from sys import modules

    _globals = allNames or globals()
    reloading = __name__ in modules
    for name in interfaceNames:
        if reloading or not hasattr(__builtin__, name):
            setattr(__builtin__, name, _globals[name])
        else:
            utils.E('COLLISION!', name=name)

    for name, val in extras:
        if reloading or not hasattr(__builtin__, name):
            setattr(__builtin__, name, val)
        else:
            utils.E('COLLISION!', name=name)

_locals = locals()
jamInterfaceIntoBuiltins(_locals)


from types import ModuleType
utils.timeAllCallables((
    v for v in _locals.itervalues() if isinstance(v, ModuleType)
))

print '[STAK]', __name__, 'import', clock() - time, 's'
