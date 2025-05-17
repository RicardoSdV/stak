"""
Some stuff is more convenient if computed, but really it only needs to be computed once, not every time the program is run.
So, the solution is to compute these things in this file & inject the results into stak.
Also, removes some clutter from the code.
Also, settings are injected by running this.
"""
from time import time
start = time()

from collections import OrderedDict, defaultdict
from functools import partial
from itertools import izip
from os.path import join

from src.stak_func.stak.block00_typing import *
from src.stak_func.stak.block03_constants import stdFlags, stakFlags, cutoffFlag, traceFlags
from src.stak_func.stak.z_utils import read, padFlags, write, loadBlocks, tryCall, packageName, P

constsFileName = 'block03_constants.py'
constsPath = join(packageName, constsFileName)

readConstants = partial(read, constsPath)
writeConstants = partial(write, constsPath)

def runInjectors():
    # Settings injection must happen first
    tryCall(injectSettings, errMess='Settings injection failed')
    tryCall(injectConstants, errMess='Constants injection failed')

    P('Injection took:', round(time() - start, 2), 's')

def injectSettings():
    from src.stak_func.autoSetting import readSettingObj, slottables, writeSettingObj

    settingObjLines = readSettingObj()
    insertInPlace(settingObjLines, '    __slots__ = ', tuple(slottables))
    writeSettingObj(settingObjLines)

def injectConstants():
    constsLines = readConstants()

    # Flags
    paddedStdFlags   = tuple(padFlags(stdFlags))
    paddedStakFlags  = tuple(padFlags(stakFlags))
    paddedTraceFlags = tuple(padFlags(traceFlags))

    insertInPlace(constsLines, 'pStakFlags = '         , paddedStakFlags)
    insertInPlace(constsLines, 'paddedStdFlags = '     , paddedStdFlags)
    insertInPlace(constsLines, 'pTraceFlags = '        , paddedTraceFlags)
    insertInPlace(constsLines, 'pStdFlagsByStdFlags = ', {flag: pFlag for flag, pFlag in izip(stdFlags, paddedStdFlags)})
    insertInPlace(constsLines, 'allPflagsByFlags = '   , allPaddedFlagsByAllFlags())

    # Parsing standard logs
    cutoffCombos = tuple(uniqueFlagCutoffCombosByRepetitions())
    insertInPlace(constsLines, 'cutoffCombos = ', 'OrderedDict({})'.format(cutoffCombos))
    insertInPlace(constsLines, 'wholeEnoughs = ', wholeEnoughs(OrderedDict(cutoffCombos)))

    writeConstants(constsLines)

    blocks = loadBlocks()
    callableNames = getCallableNames(blocks)
    insertInPlace(constsLines, 'callableNames = ', '{' + str(set(callableNames)).lstrip('set([').rstrip('])') + '}')

    writeConstants(constsLines)

def insertInPlace(lines, lookingFor, dataStructure):  # type: (Lst[str], str, Any) -> None
    for i, line in enumerate(lines):
        if line.startswith(lookingFor):
            lines[i] = '{}{}  # This line was injected by injectors.py\n'.format(lookingFor, str(dataStructure))
            return
    else:
        raise ValueError('Looking for "{}" prefix & not found!'.format(lookingFor))

def uniqueFlagCutoffCombosByRepetitions():  # type: () -> Itrt[Tup[str, int]]
    combos = defaultdict(int)

    for _str in stdFlags:
        while _str:
            combos[_str] += 1
            _str = _str[1:]

    for combo in sorted(combos, key=len, reverse=True):
        yield combo, combos[combo]

def wholeEnough(cutoffCombos, flag):  # type: (OrderedDict[str, int], str) -> str
    while flag:
        if cutoffCombos[flag] > 1:
            return
        yield flag
        flag = flag[1:]

def wholeEnoughs(cutoffCombos):  # type: (OrderedDict[str, int]) -> Dic[str, str]
    # There are certain strings, for which, if we know that they are a flag which was cutoff, are unique enough
    # to discern the full flag from. This creates a dict associating such "whole enough" flags & whole flags.
    return {
        wholeEnoughFlag: wholeFlag
        for wholeFlag in stdFlags
        for wholeEnoughFlag in wholeEnough(cutoffCombos, wholeFlag)
    }

def allPaddedFlagsByAllFlags():  # type: () -> Dic[str, str]
    allFlags = stakFlags + stdFlags + (cutoffFlag, )
    pAllFlags = padFlags(allFlags)
    return {flag: pFlag for flag, pFlag in izip(allFlags, pAllFlags)}

def getCallableNames(blocks):  # type: (Itrb[ModuleType]) -> Itrt[str]
    # Setting a trace implies that all the callables of STAK at some point might get traced
    # so, accumulate all their names to skip tracing.
    for module in blocks:
        for name, val in module.__dict__.iteritems():
            if callable(val):
                yield name


if __name__ == '__main__':
    runInjectors()
