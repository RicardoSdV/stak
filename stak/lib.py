"""
Lib names are not descriptive enough so normally people import the top module & . access
it to provide more info but this is creating run time overhead for no reason, also for py223
compatibility all lib imports should come from this module and not their lib.
"""
import os
osName           = os.name
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

import sys
sysVersion  = sys.version
sysGetFrame = sys._getframe
sysGetTrace = sys.gettrace
sysSetTrace = sys.settrace
sysExcInfo  = sys.exc_info
sysModules  = sys.modules

import importlib
importModule = importlib.import_module

import shutil
shutilRmTree = shutil.rmtree

import traceback
tracebackPrintException = traceback.print_exception
tracebackFormatStack    = traceback.format_stack

import types
Function = types.FunctionType

import collections
DefaultDict = collections.defaultdict
Deque       = collections.deque

import functools
Partial        = functools.partial
funcToolsWraps = functools.wraps

import time
timeTime = time.time

import datetime
DateTime        = datetime.datetime
dtFromTimeStamp = DateTime.fromtimestamp

import math
mathFloor = math.floor
mathLog10 = math.log10

import itertools
iSlice = itertools.islice

import copy
deepCopy = copy.deepcopy

import cPickle
cPickleDumps           = cPickle.dumps
cPickleLoad            = cPickle.load
cPickleHighestProtocol = cPickle.HIGHEST_PROTOCOL

import logging
PY_CRITICAL_LVL = logging.CRITICAL
PY_FATAL_LVL    = logging.FATAL
PY_ERROR_LVL    = logging.ERROR
PY_WARNING_LVL  = logging.WARNING
PY_WARN_LVL     = logging.WARN
PY_INFO_LVL     = logging.INFO
PY_DEBUG_LVL    = logging.DEBUG
PY_NOTSET_LVL   = logging.NOTSET


# Py 223
isPy2 = sysVersion.startswith('2')
print 'isPy2', isPy2

if isPy2:
    if hasattr(time, 'clock'):
        timeClock = time.clock
    else:
        timeClock = time.time
else:
    timeClock = time.perf_counter


if isPy2:
    iterItems = dict.iteritems
    items = dict.items
else:
    iterItems = dict.items
    items = lambda d: list(dict.items(d))


if isPy2:
    izip = itertools.izip
    zip = zip
else:
    izip = zip
    zip = lambda *args: list(zip(*args))
