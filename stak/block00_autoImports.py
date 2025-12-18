""" The idea is to have a global namespace of modules inside stak, also replace stak ModuleTypes with own.
Finally, auto import all type hints when TYPE_CHECKING.

This module can be imported by any, but itself should not import.
"""
from typing import TYPE_CHECKING


## Lib imports py2/3 compatible
import __builtin__
builtins = __builtin__.__dict__

import sys
sysGetFrame = sys._getframe
sysGetTrace = sys.gettrace
sysSetTrace = sys.settrace
sysModules  = sys.modules
sysVersion  = sys.version
isPy3       = sysVersion.startswith('3')
isPy2       = not isPy3

import os
osMakeDirs     = os.makedirs
osListDir      = os.listdir
osRename       = os.rename
osPath         = os.path
osPathJoin     = osPath.join
osPathSplit    = osPath.split
osPathBaseName = osPath.basename
osPathDirName  = osPath.dirname
osPathExists   = osPath.exists
osPathIsDir    = osPath.isdir
osPathSplitExt = osPath.splitext
osPathAbsPath  = osPath.abspath
osAbsPath      = osPathDirName(osPathDirName(os.__file__))
lenOsAbsPath   = len(osAbsPath)

import math
floor = math.floor
log10 = math.log10

import types
Function = types.FunctionType
Module   = types.ModuleType

import time as timeM
time  = timeM.time
clock = timeM.clock if isPy2 else timeM.perf_counter

import itertools
chain     = itertools.chain
unsafeZip = zip
izip      = itertools.izip if isPy2 else unsafeZip
zip       = lambda *a, **k: list(unsafeZip(*a, **k)) if isPy3 else unsafeZip
repeat    = itertools.repeat
islice    = itertools.islice

import functools
Partial = functools.partial
wraps   = functools.wraps

import collections
Deque       = collections.deque
DefaultDict = collections.defaultdict

import datetime
DateTime      = datetime.datetime
DateTimeNow   = DateTime.now
fromTimeStamp = DateTime.fromtimestamp

import shutil
shutilRmTree = shutil.rmtree

import importlib
importModule = importlib.import_module

import copy as copyM
copy = copyM.copy

import traceback
printStack = traceback.print_stack
formatExc  = traceback.format_exc

from lib import io, packageUnite as pu
read       = io.read
write      = io.write
readLines  = io.readLines
writeLines = io.writeLines

reloadModByNameGetDiff = pu.reloadModByNameGetDiff
reloadUnited           = pu.reloadUnited

if TYPE_CHECKING:

    ## Import all the names of stak for the editor.
    # TODO: Inject these
    from .block01_settings       import *
    from .block02_constants      import *
    from .block03_state          import *
    from .block04_log            import *
    from .block05_utils          import *
    from .block06_stampOps       import *
    from .block07_pathOps        import *
    from .block08_callChains     import *
    from .block09_joinLinks      import *
    from .block10_dataLinks      import *
    from .block11_tracing        import *
    from .block12_interceptor    import *
    from .block13_compression    import *
    from .block14_saveOps        import *
    from .block15_debugComponent import *
    from .block16_injectors      import *
    from .block17_meta           import *
    from .block18_perf           import *
    from .block19_computed       import *

    # In-house builtins 4 editor
    __unitedModPaths__ = []
    __unitedModNames__ = []

    ## type hints
    from types import (
        CodeType,
        FrameType as Frame,
        ModuleType as Module,
        TracebackType, ModuleType,
    )
    from typing import (
        Any,
        Callable  as Cal,
        Container as Cont,
        Dict      as Dic,
        Deque     as Deq,
        Generator as Gen,
        Iterable  as Itrb,
        Iterator  as Itrt,
        List      as Lst,
        Literal   as Lit,
        Optional  as Opt,
        Sequence  as Seq,
        Set,
        Tuple     as Tup,
        Type      as Typ,
        Union     as Uni,
    )
    from logging import Logger

    # Type Aliases: Use to abbreviate simplicity, not hide complexity.
    Str4 = Tup[str, str, str, str]

    TraceEvent = Uni[Lit['call'], Lit['line'], Lit['return'], Lit['exception']]

#   splitLink      = (filePath, lineno, mroClsNs or None, calName, strData or None)
    SplitLink      = Tup[str, int, Opt[Tup[str, ...]], str, Opt[Tup[str, str]]]
    SplitLinkTrace = Tup[str, int, Opt[Tup[str, ...]], str, Opt[Tup[str, str]], Opt[int]]

    SplitLinkChain = Tup[SplitLink, ...]

    DataForLogging = Opt[Tup[Tup[str, str], ...]]

#   stakLog = [(unixStamp, splitLinkChain), ...]
    StakLog = Lst[Tup[float, SplitLinkChain]]

#   traceLog = [(unixStamp, traceFlag, splitLink)]
    TraceLog = Deq[Tup[float, str, SplitLink]]

    Primi = Uni[bool, int, long, float, str, unicode, None]

    # Lib Types
    Clock  = Cal[[], float]
    Append = Cal[[Any], None]
    Extend = Cal[[Itrb], None]

