"""
Some stuff is more convenient if computed, but really it only needs to be computed once, not every time the program is run.
So, the solution is to compute these things in this file & inject the results into the files where they are used.
Also, removes some clutter from the already large code.
"""

from collections import OrderedDict, defaultdict
from itertools import izip

from src.stak_func.stak.block00_typing import *
from src.stak_func.stak.block02_loadAndReload import blocks
from src.stak_func.stak.block03_commonData import stdFlags, stakFlags, cutoffFlag, traceFlags
from src.stak_func.stak.block06_pathOps import getPackageName
from src.stak_func.stak.z_utils import read, padFlags


dataFile = 'stak\\block02_commonData.py'

def runInjectors():
    dataLines = read(dataFile)

    # Flags
    paddedStdFlags   = tuple(padFlags(stdFlags))
    paddedStakFlags  = tuple(padFlags(stakFlags))
    paddedTraceFlags = tuple(padFlags(traceFlags))

    insertInPlace(dataLines, 'pStakFlags = '         , paddedStakFlags)
    insertInPlace(dataLines, 'paddedStdFlags = '     , paddedStdFlags)
    insertInPlace(dataLines, 'pTraceFlags = '        , paddedTraceFlags)
    insertInPlace(dataLines, 'pStdFlagsByStdFlags = ', {flag: pFlag for flag, pFlag in izip(stdFlags, paddedStdFlags)})
    insertInPlace(dataLines, 'allPflagsByFlags = '   , allPaddedFlagsByAllFlags())

    # Parsing standard logs
    cutoffCombos = tuple(uniqueFlagCutoffCombosByRepetitions())
    insertInPlace(dataLines, 'cutoffCombos = ', 'OrderedDict({})'.format(cutoffCombos))
    insertInPlace(dataLines, 'wholeEnoughs = ', wholeEnoughs(OrderedDict(cutoffCombos)))

    write(dataLines, dataFile)
    insertInPlace(dataLines, 'callableNames = ', '{' + str(set(getCallableNames())).lstrip('set([').rstrip('])') + '}')

    write(dataLines, dataFile)

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

def getCallableNames():  # type: () -> Itrt[str]
    # Setting a trace implies that all the callables of STAK at some point might get traced
    # so, accumulate all their names to skip tracing.
    for _, module in blocks:
        for name, val in module.__dict__.iteritems():
            if callable(val):
                yield name

def write(lines, fileName):  # type: (Itrb[str], str) -> None
    with open(fileName, 'w') as f:
        f.writelines(lines)


if __name__ == '__main__':
    runInjectors()
