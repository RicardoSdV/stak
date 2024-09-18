"""
Some stuff is more convenient if computed, but really it only needs to be computed once, not every time the program is run.
So, the solution is to compute these things in this file & inject the results into STAK.py.
Also, removes some clutter from the already large STAK class.
"""
from typing import *
from collections import OrderedDict, defaultdict
from itertools import izip

from STAK import STAK

""" ======================================================= INJECTION LOGIC ======================================================= """

injectionComment = '  # This line was injected by injectors.py\n'

def run():
    # Extract constants from STAK
    stakFlags  = STAK._stakFlags
    stdFlags   = STAK._stdFlags
    cutoffFlag = STAK._cutoffFlag

    lines = readStak()

    # Slots
    insertInPlace(lines, '    __slots__ = ', str(tuple(autoSlots(lines))))

    # Flags
    paddedStdFlags, paddedStakFlags = tuple(padFlags(stdFlags)), tuple(padFlags(stakFlags))
    insertInPlace(lines, '    __paddedStakFlags = ', paddedStakFlags)
    insertInPlace(lines, '    __paddedStdFlags = ', paddedStdFlags)
    insertInPlace(lines, '    __pStdFlagsByStdFlags = ', str({flag: pFlag for flag, pFlag in izip(stdFlags, paddedStdFlags)}))
    insertInPlace(lines, '    __allPflagsByFlags = ', str(allPaddedFlagsByAllFlags(stakFlags, stdFlags, cutoffFlag)))

    # Parsing standard logs
    cutoffCombos = tuple(uniqueFlagCutoffCombosByRepetitions(stdFlags))
    cutoffCombosStr = '__OrderedDict({})'.format(str(cutoffCombos))
    insertInPlace(lines, '    __cutoffCombos = ', cutoffCombosStr)
    insertInPlace(lines, '    __wholeEnoughs = ', str(wholeEnoughs(OrderedDict(cutoffCombos), stdFlags)))


    writeStak(lines)

def insertInPlace(lines, lookingFor, dataStructure):  # type: (List[str], str, Any) -> None
    for i, line in enumerate(lines):
        if line.startswith(lookingFor):
            lines[i] = '{}{}{}'.format(lookingFor, str(dataStructure), injectionComment)
            return

""" =============================================================================================================================== """

def autoSlots(lines):  # type: (List[str]) -> Iterator[str]
    # Entirely tired of manually adding slots, so go through innit & add all into slots

    inInit = False
    for line in lines:
        if line.startswith('    def __init__('):
            inInit = True

        elif inInit:
            if line.startswith('    def'):
                return

            elif line.startswith('        self.') and '=' in line:
                yield line.lstrip('        self.').split('=')[0].rstrip()


def padFlags(flags):  # type: (Sequence[str]) -> Iterator[str]
    maxFlagLen = max(len(flag) for flag in flags)
    return (': ' + flag + ' ' * (maxFlagLen - len(flag)) + ': ' for flag in flags)

def uniqueFlagCutoffCombosByRepetitions(stdFlags):  # type: (Tuple[str, ...]) -> Iterator[Tuple[str, int]]
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

def wholeEnoughs(cutoffCombos, stdFlags):
    # type: (OrderedDict[str, int], Tuple[str, ...]) -> Dict[str, str]
    # There are certain strings, for which, if we know that they are a flag which was cutoff, are unique enough
    # to discern the full flag from. This creates a dict associating such "whole enough" flags & whole flags.
    return {
        wholeEnoughFlag: wholeFlag
        for wholeFlag in stdFlags
        for wholeEnoughFlag in wholeEnough(cutoffCombos, wholeFlag)
    }

def allPaddedFlagsByAllFlags(stakFlags, stdFlags, cutoffFlag):  # type: (Tuple[str, ...], Tuple[str, ...], str) -> Dict[str, str]
    allFlags = stakFlags + stdFlags + (cutoffFlag, )
    pAllFlags = padFlags(allFlags)
    return {flag: pFlag for flag, pFlag in izip(allFlags, pAllFlags)}


""" ==================================================== READ WRITE OPERATIONS ==================================================== """

def readStak():  # type: () -> List[str]
    with open('STAK.py', 'r') as f:
        return f.readlines()

def writeStak(lines):  # type: (Iterable[str]) -> None
    with open('STAK.py', 'w') as f:
        f.writelines(lines)

""" =============================================================================================================================== """

if __name__ == '__main__':
    run()
