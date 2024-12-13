"""
Some stuff is more convenient if computed, but really it only needs to be computed once, not every time the program is run.
So, the solution is to compute these things in this file & inject the results into STAK.py.
Also, removes some clutter from the already large STAK class.
And, incidentally allows for some cool stuff which would be impossible or very hard from STAK
"""

from typing import *
from collections import OrderedDict, defaultdict
from itertools import izip, chain


""" ======================================================= INJECTION LOGIC ======================================================= """

def run():
    cls, lines = writeMaybeForceLoadAndRereadStak()

    # Extract constants from STAK
    stakFlags  = cls.stakFlags
    stdFlags   = cls.stdFlags
    cutoffFlag = cls.cutoffFlag

    # Slots
    insertInPlace(lines, '    __slots__ = ', tuple(autoSlots(lines)))

    # Flags
    paddedStdFlags, paddedStakFlags = tuple(padFlags(stdFlags)), tuple(padFlags(stakFlags))
    insertInPlace(lines, '    pStakFlags = ', paddedStakFlags)
    insertInPlace(lines, '    paddedStdFlags = ', paddedStdFlags)
    insertInPlace(lines, '    pStdFlagsByStdFlags = ', {flag: pFlag for flag, pFlag in izip(stdFlags, paddedStdFlags)})
    insertInPlace(lines, '    allPflagsByFlags = ', allPaddedFlagsByAllFlags(stakFlags, stdFlags, cutoffFlag))

    # Parsing standard logs
    cutoffCombos = tuple(uniqueFlagCutoffCombosByRepetitions(stdFlags))
    insertInPlace(lines, '    from collections import OrderedDict; cutoffCombos = ', 'OrderedDict({}); del OrderedDict'.format(cutoffCombos))
    insertInPlace(lines, '    wholeEnoughs = ', wholeEnoughs(OrderedDict(cutoffCombos), stdFlags))

    # Stuff that is dependent on previous injection
    cls, lines = writeMaybeForceLoadAndRereadStak(lines)

    # Trace log stuff
    cNames = tuple(callableNames(cls))

    insertInPlace(lines, '    callableNames = ', str(cNames).replace('(', '{').replace(')', '}'))

    writeStak(lines)

def insertInPlace(lines, lookingFor, dataStructure):  # type: (List[str], str, Any) -> None
    for i, line in enumerate(lines):
        if line.startswith(lookingFor):
            lines[i] = '{}{}  # This line was injected by injectors.py\n'.format(lookingFor, str(dataStructure))
            return
    else:
        raise ValueError('Looking for "{}" prefix & not found! prefix must literally exist for injection to happen...')

""" =============================================================================================================================== """

def autoSlots(lines):  # type: (List[str]) -> Iterator[str]
    # Entirely tired of manually adding slots, so go through __init__ & add all attrs into slots
    inInit = False
    for line in lines:
        if line.startswith('    def __init__('):
            inInit = True
        elif inInit:
            if line.startswith('        self.') and '=' in line:
                yield line.replace('        self.', '').split('=')[0].rstrip()
            elif line.startswith('    def'):
                return

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

def callableNames(cls):  # type: (Type[Any]) -> Iterator[str]
    # Setting a trace implies that all the callables of STAK at some point might get traced
    # so, accumulate all their names so skip the tracing automatically
    clsName = cls.__name__
    return chain(callableAttrs(cls(), clsName), methsPropsStatsAndClassMethods(cls.__dict__, clsName))

def callableAttrs(obj, clsName):  # type: (Any, str) -> Iterator[str]
    for slot in obj.__slots__:
        if slot.startswith('__') and not slot.endswith('__'):
            attrName = '{}{}'.format(clsName, slot)
            if not attrName.startswith('_'):
                attrName = '_' + attrName
        else:
            attrName = slot
        if callable(getattr(obj, attrName)):
            yield slot

def methsPropsStatsAndClassMethods(clsDict, clsName):  # type: (Dict[str, Callable], str) -> Iterator[str]
    mangledClsName = clsName if clsName.startswith('_') else '_' + clsName
    for methName, meth in clsDict.items():
        if callable(meth) or isinstance(meth, (property, staticmethod, classmethod)):
            if methName.startswith(mangledClsName):  # Could be that a crazy soul includes the mangled class name in a non-private meth name
                methName = methName.replace(mangledClsName, '', 1)
            yield methName

""" ==================================================== READ WRITE OPERATIONS ==================================================== """

def writeMaybeForceLoadAndRereadStak(lines=None):  # type: (Optional[List[str]]) -> Tuple[Type['STAK'], List[str]]
    # For some things the latest injection is needed so module is reloaded in this way
    if lines:
        writeStak(lines)
    import STAK; reload(STAK)
    return STAK.STAK, readStak()

def readStak():  # type: () -> List[str]
    with open('STAK.py', 'r') as f:
        return f.readlines()

def writeStak(lines):  # type: (Iterable[str]) -> None
    with open('STAK.py', 'w') as f:
        f.writelines(lines)

""" =============================================================================================================================== """

if __name__ == '__main__':
    run()
