"""
Assuming that the log may be cutoff but the format won't change.
If some or all the stamp is missing it is interpolated from the
previous & next. If some part of the flag is missing whatever flag
is kept in the line and no further action is taken to recreate
"""

import re
from collections import defaultdict, OrderedDict

from typing import Tuple, List, Optional, Iterable, Dict, Sequence, Union


def cutOffLogs():
    return (
        '2024-07-04 13:17:45.269: INFO: [CORRECTLOG] This is a log line which is expected and correct\n',
        '2024-07-04 13:17:45.269: DEBUG: A debug line \n',
        '2024-07-04 13:17:45.269: CRITICAL: Longest expected flag\n',
        '024-07-04 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
        '24-07-04 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
        '4-07-04 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
        '-07-04 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
        '07-04 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
        '7-04 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
        '-04 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
        '04 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
        '4 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
        ' 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
        '13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
        '3:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
        ':17:45.269: CRITICAL: Some flag of the log is cutoff\n',
        '17:45.269: CRITICAL: Some flag of the log is cutoff\n',
        '7:45.269: CRITICAL: Some flag of the log is cutoff\n',
        ':45.269: CRITICAL: Some flag of the log is cutoff\n',
        '45.269: CRITICAL: Some flag of the log is cutoff\n',
        '5.269: CRITICAL: Some flag of the log is cutoff\n',
        '.269: CRITICAL: Some flag of the log is cutoff\n',
        '269: CRITICAL: Some flag of the log is cutoff\n',
        '69: CRITICAL: Some flag of the log is cutoff\n',
        '9: CRITICAL: Some flag of the log is cutoff\n',
        ': CRITICAL: Some flag of the log is cutoff\n',
        ' CRITICAL: Some flag of the log is cutoff\n',
        'CRITICAL: Some flag of the log is cutoff\n',
        'RITICAL: Some flag of the log is cutoff\n',
        'ITICAL: Some flag of the log is cutoff\n',
        'TICAL: Some flag of the log is cutoff\n',
        'ICAL: Some flag of the log is cutoff\n',
        'CAL: Some flag of the log is cutoff\n',
        'AL: Some flag of the log is cutoff\n',
        'L: Some flag of the log is cutoff\n',
        ': Some flag of the log is cutoff\n',
        ' Some flag of the log is cutoff\n',
        'Some flag of the log is cutoff\n',
        'Some: flag: of the log is cutoff\n',
    )

LogTuple = Tuple[str, ...]
Line = str
Index = int
EmptyStr = str

StdLogLines = List[Line]

Year     = str
Month    = str
Day      = str
Hour     = str
Minute   = str
Second   = str
MilliSec = str

ColonFlag = str
TrimmedLine = str

MatchTuple = Tuple[
    Optional[Year],
    Optional[Month],
    Optional[Day],
    Optional[Hour],
    Optional[Minute],
    Optional[Second],
    Optional[MilliSec],
    Optional[ColonFlag],
]

ParsedLine = Tuple[
    Optional[Year],
    Optional[Month],
    Optional[Day],
    Optional[Hour],
    Optional[Minute],
    Optional[Second],
    Optional[MilliSec],
    Optional[ColonFlag],
    Optional[TrimmedLine],
]

InterpolatedTimestampElement = Union[
    Union[Year,     EmptyStr],
    Union[Month,    EmptyStr],
    Union[Day,      EmptyStr],
    Union[Hour,     EmptyStr],
    Union[Minute,   EmptyStr],
    Union[Second,   EmptyStr],
    Union[MilliSec, EmptyStr],
]

CutoffLogFlagCombo = str
CutoffLogFlagCombos = Tuple[CutoffLogFlagCombo, ...]  # All possible cutoffs


ParsedStdLogLines = List[ParsedLine]
colonFlags = ('DEBUG', 'INFO', 'NOTICE', 'WARNING', 'ERROR', 'CRITICAL', 'HACK')

logPattern = re.compile(
    r'(?:(\d{4})-)?'  # year
    r'(?:(\d{2})-)?'  # month
    r'(?:(\d{2}) )?'  # day
    r'(?:(\d{2}):)?'  # hour
    r'(?:(\d{2}):)?'  # minute
    r'(?:(\d{2})\.)?'  # second
    r'(?:(\d{3}))?'  # millisec
    r': ([A-Z]+):'  # logFlag
)

nones9 = (None, None, None, None, None, None, None, None, None)

def uniqueFlagCutoffCombosByRepetitionsCreator(strs):
    # type: (Sequence[str]) -> OrderedDict[str, int]
    combos = defaultdict(int)

    for _str in strs:
        while _str:
            combos[_str] += 1
            _str = _str[1:]

    sortedCombos = sorted(combos, key=len, reverse=True)

    orderedCombos = OrderedDict({combo: combos[combo] for combo in sortedCombos})

    return orderedCombos

cutoffCombos = uniqueFlagCutoffCombosByRepetitionsCreator(colonFlags)

def wholeEnoughsCreator(flags, cutoffCombos):
    # type: (Sequence[Line], defaultdict[str, int]) -> Dict[str, str]

    def wholeEnoughGenerator(part, cutoffCombos):
        while part:
            if cutoffCombos[part] > 1:
                return
            yield part
            part = part[1:]

    wholeEnoughs = {}
    for flag in flags:
        for wholeEnough in wholeEnoughGenerator(flag, cutoffCombos):
            wholeEnoughs[wholeEnough] = flag
    return wholeEnoughs

wholeEnoughs = wholeEnoughsCreator(colonFlags, cutoffCombos)
for combo, flag in wholeEnoughs.items():
    print flag, combo, cutoffCombos[combo]

def trimFlagFromLineReturnFlagIfWholeEnough(line):
    # type: (Line) -> Tuple[Line, Union[ColonFlag, EmptyStr]]
    line = line.lstrip()

    for combo in cutoffCombos:
        if line.startswith(combo):
            line = line.lstrip(combo)

            repCnt = cutoffCombos[combo]
            if repCnt > 1:
                return line, ''
            return line, wholeEnoughs[combo]

    return line, ''


def trimTimeFromLine(line, logTuple):  # type: (Line, LogTuple) -> Line
    numsTrimChars = (25, 20, 17, 14, 11, 8, 5, 0)
    for i, prefixEl in enumerate(logTuple):
        if prefixEl is not None:

            while not line.startswith(prefixEl):
                line = line[1:]

            numTrimChars = numsTrimChars[i+1] if i < 7 and logTuple[i+1] is None else numsTrimChars[i]

            return line[numTrimChars:]

def trimFlagFromLine(line):
    combos = cutoffCombos
    for combo in combos:
        if line.startswith(combo):
            return line.lstrip(combo)
    return line

range6 = range(6)
def isStampCutoff(line):  # type: (ParsedLine) -> bool
    for j in range6:
        if line[j] is None:
            return True
    return False

def interpolatedTimestampGenerator(prevLine, thisLine, nextLine):
    # type: (ParsedLine, ParsedLine, ParsedLine) -> Iterable[InterpolatedTimestampElement]

    for i in range6:
        prevEl, nextEl = prevLine[i], nextLine[i]
        if prevEl is None and nextEl is None:
            yield ''
        if prevEl is not None:
            if nextEl is not None:
                yield str((int(prevEl) + int(nextEl)) // 2)
            else:
                yield prevEl
        else:
            yield nextEl

    yield thisLine[-2]
    yield thisLine[-1]

def parsedLinesGenerator(lines):
    nones8 = (None, None, None, None, None, None, None, None)
    for line in lines:
        match = logPattern.search(line)
        matchTuple = match.groups() if match else nones8

        if matchTuple[4] is None and matchTuple[3] is not None:
            matchTuple = (None, None, None, None, matchTuple[3], matchTuple[5], matchTuple[6])

        if matchTuple[-1] is not None:
            line = trimTimeFromLine(line, matchTuple)
            line = trimFlagFromLine(line)
            yield matchTuple + (line.lstrip(': '),)
        else:
            line, flag = trimFlagFromLineReturnFlagIfWholeEnough(line)
            yield None, None, None, None, None, None, None, flag, line.lstrip(': ')


def parseLog(lines):  # type: (StdLogLines) -> ParsedStdLogLines
    parsedLines = list(parsedLinesGenerator(lines))

    lenLines = len(parsedLines)
    for line in parsedLines:

        if isStampCutoff(line):
            thisLineIndex = parsedLines.index(line)  # Only expecting to interpolate < 1% of parsedLines
            prevLine, nextLine = nones9, nones9
            prevLineIndex, nextLineIndex = thisLineIndex-1, thisLineIndex+1

            while isStampCutoff(prevLine) and prevLineIndex < lenLines:
                prevLine = parsedLines[prevLineIndex]
                prevLineIndex -= 1

            while isStampCutoff(nextLine) and nextLineIndex < lenLines:
                nextLine = parsedLines[nextLineIndex]
                nextLineIndex += 1

            parsedLines[thisLineIndex] = tuple(interpolatedTimestampGenerator(prevLine, line, nextLine))

    return parsedLines

ogLines = cutOffLogs()
parsedLines = parseLog(ogLines)


for parsedLine, unparsedLine in zip(parsedLines, ogLines):
    print parsedLine
    print unparsedLine



















