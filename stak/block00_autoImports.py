""" The idea is to have a global namespace of modules inside stak, also replace stak ModuleTypes with own.
Finally, auto import all type hints when TYPE_CHECKING.

This module can be imported by any, but itself should not import.
"""
## Lib imports py2/3 compatible
import __builtin__
builtins = __builtin__.__dict__

import collections
Deque       = collections.deque
DefaultDict = collections.defaultdict

import copy as copyM
copy = copyM.copy

import ctypes as cTypes
cByte    = cTypes.c_byte
cInt     = cTypes.c_int
cSizeT   = cTypes.c_size_t
cCharPtr = cTypes.c_char_p
cDLL     = cTypes.CDLL
cArr     = cTypes.Array
cPtr     = cTypes.POINTER

import sys
sysGetFrame = sys._getframe
sysGetTrace = sys.gettrace
sysSetTrace = sys.settrace
sysModules  = sys.modules
sysVersion  = sys.version
pyVersion   = sysVersion.split(' ')[0]
pyVerJoint  = ''.join(pyVersion.split('.')[:2])
isPy3       = sysVersion.startswith('3')
isPy2       = not isPy3
sysPlatform = sys.platform
osName      = 'linux' if sysPlatform[:5] == 'linux' else sysPlatform
binaryExt   = '.so' if osName == 'linux' else osName
sysPath     = sys.path

import subprocess
openSubProcess = subprocess.Popen
subProcessPipe = subprocess.PIPE

import os
osMakeDirs       = os.makedirs
osListDir        = os.listdir
osRename         = os.rename
osPath           = os.path
osWalk           = os.walk
osPathJoin       = osPath.join
osPathSplit      = osPath.split
osPathBaseName   = osPath.basename
osPathDirName    = osPath.dirname
osPathExists     = osPath.exists
osPathIsDir      = osPath.isdir
osPathSplitExt   = osPath.splitext
osPathAbsPath    = osPath.abspath
osPathGetModTime = osPath.getmtime
osAbsPath        = osPathDirName(osPathDirName(os.__file__))
lenOsAbsPath     = len(osAbsPath)

import distutils.sysconfig as sysConfig
getConfigVar = sysConfig.get_config_var

import math
floor = math.floor
log10 = math.log10

import types
Function = types.FunctionType
Module   = types.ModuleType

import time as timeM
time  = timeM.time
if isPy2:
    if osName == 'linux':
        clock = time  # Best time in linux py2 (a bit shit)
    else:
        assert osName == 'win', 'Only Windows & linux supported.'
        clock = timeM.clock
else:
    assert isPy3
    clock = time.perf_counter

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

import datetime
DateTime      = datetime.datetime
DateTimeNow   = DateTime.now
fromTimeStamp = DateTime.fromtimestamp

import shutil
shutilRmTree = shutil.rmtree

import importlib
importModule = importlib.import_module

import traceback
formatStack = traceback.format_stack
formatExc   = traceback.format_exc
printExc    = traceback.print_exception

from . import lib
reloadModByNameGetDiff = lib.reloadModByNameGetDiff
reloadUnited           = lib.reloadUnited
read       = lib.read
write      = lib.write
readLines  = lib.readLines
writeLines = lib.writeLines

import logging
PY_CRITICAL_LVL = logging.CRITICAL
PY_FATAL_LVL    = logging.FATAL
PY_ERROR_LVL    = logging.ERROR
PY_WARNING_LVL  = logging.WARNING
PY_WARN_LVL     = logging.WARN
PY_INFO_LVL     = logging.INFO
PY_DEBUG_LVL    = logging.DEBUG
PY_NOTSET_LVL   = logging.NOTSET

import pybind11


# os does not hold the correct path char for certain programs, when inspecting frames,
# for os file ops should os.path.join, but for frame ops use pathSplitChar.
pathSplitChar = '/' if '/' in sysGetFrame(0).f_code.co_filename else '\\'

splitPackageDotPath = __name__.split('.')[:-1]
packageName         = splitPackageDotPath[-1]

packagePath       = osPathDirName(osPathAbsPath(__file__))      # stak/stak
stakCPath         = osPathJoin(packagePath, 'c')                # stak/stak/c
stakIncludePath   = osPathJoin(stakCPath, 'include')            # stak/stak/c/include
stakSrcPath       = osPathJoin(stakCPath, 'src')                # stak/stak/c/src
stakBuildPath     = osPathJoin(packagePath, 'lib', 'build')     # stak/stak/lib/build
stakBinaryDirPath = osPathJoin(stakBuildPath, osName, 'py' + pyVerJoint)
stakBinaryPath    = osPathJoin(stakBinaryDirPath, 'c_stak' + binaryExt)
sourceModTimePath = osPathJoin(stakBuildPath, 'lastSourceModTime.txt')

packagePathLen = len(packagePath)


try:  # Vanilla python27 does not support typing
    from typing import TYPE_CHECKING
except ImportError:
    TYPE_CHECKING = False

if TYPE_CHECKING:

    ## Import all the names of stak for the editor.
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
    from .block15_injectors      import *
    from .block16_meta           import *
    from .block17_perf           import *
    from .block18_wrapC          import *
    from .block19_compile        import *
    from .block20_events         import *

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

    __all__ = list(locals().keys())
