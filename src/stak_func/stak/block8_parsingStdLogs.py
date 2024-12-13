from collections import OrderedDict
from re import compile as compileRegexExpression

from .block0_typing import *
from .block1_commonData import cutoffFlag, stdFlags, stdLogFiles


matcher = compileRegexExpression(
    r'(?:(\d{4})-)?' r'(?:(\d{2})-)?' r'(?:(\d{2}) )?' r'(?:(\d{2}):)?' r'(?:(\d{2}):)?' r'(?:(\d{2})\.)?' r'(?:(\d{3}))?' r': ([A-Z]+):'
).search

expectedChars = (4, 2, 2, 2, 2, 2, 3)

cutoffCombos = OrderedDict((('CRITICAL', 1), ('WARNING', 1), ('RITICAL', 1), ('NOTICE', 1), ('ITICAL', 1), ('ARNING', 1), ('RNING', 1), ('OTICE', 1), ('ASSET', 1), ('TICAL', 1), ('ERROR', 1), ('DEBUG', 1), ('TRACE', 1), ('HACK', 1), ('TICE', 1), ('RACE', 1), ('NING', 1), ('RROR', 1), ('INFO', 1), ('SSET', 1), ('ICAL', 1), ('EBUG', 1), ('ACE', 1), ('ACK', 1), ('CAL', 1), ('SET', 1), ('ICE', 1), ('ROR', 1), ('BUG', 1), ('NFO', 1), ('ING', 1), ('FO', 1), ('NG', 1), ('CK', 1), ('AL', 1), ('CE', 2), ('ET', 1), ('UG', 1), ('OR', 1), ('E', 2), ('G', 2), ('K', 1), ('O', 1), ('L', 1), ('R', 1), ('T', 1)))  # This line was injected by injectors.py
wholeEnoughs = {'NOTICE': 'NOTICE', 'RNING': 'WARNING', 'ACE': 'TRACE', 'ACK': 'HACK', 'HACK': 'HACK', 'EBUG': 'DEBUG', 'TICE': 'NOTICE', 'CAL': 'CRITICAL', 'OTICE': 'NOTICE', 'ASSET': 'ASSET', 'RACE': 'TRACE', 'FO': 'INFO', 'SET': 'ASSET', 'ITICAL': 'CRITICAL', 'NG': 'WARNING', 'WARNING': 'WARNING', 'NING': 'WARNING', 'ROR': 'ERROR', 'BUG': 'DEBUG', 'CK': 'HACK', 'CRITICAL': 'CRITICAL', 'TICAL': 'CRITICAL', 'NFO': 'INFO', 'K': 'HACK', 'AL': 'CRITICAL', 'O': 'INFO', 'L': 'CRITICAL', 'R': 'ERROR', 'ICE': 'NOTICE', 'ERROR': 'ERROR', 'DEBUG': 'DEBUG', 'ET': 'ASSET', 'ARNING': 'WARNING', 'INFO': 'INFO', 'SSET': 'ASSET', 'TRACE': 'TRACE', 'T': 'ASSET', 'RITICAL': 'CRITICAL', 'ICAL': 'CRITICAL', 'UG': 'DEBUG', 'ING': 'WARNING', 'OR': 'ERROR', 'RROR': 'ERROR'}  # This line was injected by injectors.py


def interpolMissingStamps(prevLine, thisLine, nextLine):  # type: (OptStr9, OptStr9, OptStr9) -> Itrt[str]
    for i, numChars in enumerate(expectedChars):
        prevEl, nextEl = prevLine[i], nextLine[i]
        if prevEl is None and nextEl is None:
            yield ' ' * numChars
        if prevEl is not None:
            if nextEl is not None:
                yield str((int(prevEl) + int(nextEl)) // 2).zfill(numChars)
            else:
                yield prevEl
        else:
            yield nextEl

    yield thisLine[-2]
    yield thisLine[-1]


def splitStampFromTheRest(lines):  # type: (Lst[Str9]) -> Itrt[Tup[Str4, str, str]]
    for year, month, day, hour, minute, second, millisec, flag, theRest in lines:
        yield (
            (hour, minute, second, millisec),
            flag,
            theRest,
        )


## Parse & interpol sub-block
def trimFlagIfPoss(line):  # type: (str) -> Str2
    line = line.lstrip()
    for combo in cutoffCombos:
        if line.startswith(combo):
            line = line.lstrip(combo)
            if cutoffCombos[combo] > 1:
                return line, cutoffFlag
            return line, wholeEnoughs[combo]
    return line, cutoffFlag


def trimFlag(line):  # type: (str) -> str
    for combo in stdFlags:
        if line.startswith(combo):
            return line.lstrip(combo)
    return line


def trimTime(line, matchTuple, numTrimChar=(25, 20, 17, 14, 11, 8, 5, 0)):  # type: (str, OptStr8, Int8) -> str
    for i, prefixEl in enumerate(matchTuple):
        if prefixEl is not None:

            while not line.startswith(prefixEl):
                line = line[1:]

            return line[numTrimChar[i+1] if i < 7 and matchTuple[i+1] is None else numTrimChar[i]:]


def parseLines(
        lines,                           # type: Lst[str]
        _trimTime=trimTime,              # type: Cal[[str, OptStr8], str]
        _trimFlag=trimFlag,              # type: Cal[[str], str]
        _trimFlagIfPoss=trimFlagIfPoss,  # type: Cal[[str], Str2]
        none8=(None, None, None, None, None, None, None, None)
):  # type: (...) -> Itrt[OptStr8PlusStr]

    for line in lines:
        match = matcher(line)
        matchTuple = match.groups() if match else none8

        if matchTuple[4] is None and matchTuple[3] is not None:
            # Hour & minute may be mixed up if cutoff at certain point
            #            (year, month, day , hour  , minute       , second       , millisec     , flag
            matchTuple = (None, None , None, None  , matchTuple[3], matchTuple[5], matchTuple[6], matchTuple[7])

        if matchTuple[-1] is not None:
            line = _trimTime(line, matchTuple)
            line = _trimFlag(line)
            yield matchTuple + (line.lstrip(': '), )
        else:
            line, flag = _trimFlagIfPoss(line)
            yield None, None, None, None, None, None, None, flag, line.lstrip(': ')


def isStampCutoff(parsedLine, range6=tuple(xrange(6))): # type: (OptStr9, Int6) -> bool
    for j in range6:
        if parsedLine[j] is None:
            return True
    return False

def parseAndInterpolLines(lines, none9=(None, None, None, None, None, None, None, None, None)):  # type: (Lst[str], None9) -> Lst[OptStr9]
    parsedLines = list(parseLines(lines))

    _interpolMissingStamps = interpolMissingStamps
    lenLines = len(parsedLines)
    for parsedLine in parsedLines:

        if isStampCutoff(parsedLine):
            thisLineIndex = parsedLines.index(parsedLine)  # Only expecting to interpolate < 1% of parsedLines
            prevLineIndex, nextLineIndex = thisLineIndex - 1, thisLineIndex + 1
            prevLine, nextLine = none9, none9

            while isStampCutoff(prevLine) and prevLineIndex < lenLines:
                prevLine = parsedLines[prevLineIndex]
                prevLineIndex -= 1

            while isStampCutoff(nextLine) and nextLineIndex < lenLines:
                nextLine = parsedLines[nextLineIndex]
                nextLineIndex += 1

            parsedLines[thisLineIndex] = tuple(
                _interpolMissingStamps(prevLine, parsedLine, nextLine)
            )

    return parsedLines

## Parse block interface
def parseStdLogs():  # type: () -> Itrt[Tup[Tup[Str4, str, str], ...]]
    for path in stdLogFiles:
        with open(path, 'r') as f:
            lines = f.readlines()
        yield tuple(
            splitStampFromTheRest(
                parseAndInterpolLines(
                    lines
                )
            )
        )

