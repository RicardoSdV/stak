from re import compile as compileRegexExpression

from .block00_typing    import *
from .block03_constants import cutoffFlag, stdFlags, wholeEnoughs


def interpolMissingStamps(prevLine, thisLine, nextLine, expectedChars=(4, 2, 2, 2, 2, 2, 3)):
    # type: (OptStr9, OptStr9, OptStr9, Int7) -> Itrt[str]

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

def trimFlag(line):  # type: (str) -> str
    for combo in stdFlags:
        if line.startswith(combo):
            return line.lstrip(combo)
    return line

def trimTime(line, matchTuple, numTrimChar=(25, 20, 17, 14, 11, 8, 5, 0)):  # type: (str, OptStr8, Int8) -> str
    for i, prefixEl in enumerate(matchTuple):
        if prefixEl is None:
            continue

        while not line.startswith(prefixEl):
            line = line[1:]

        return line[numTrimChar[i + 1] if i < 7 and matchTuple[i + 1] is None else numTrimChar[i]:]

def parseLines(
        lines,                         # type: Itrb[str]
        trimTime=trimTime,             # type: Cal[[str, OptStr8], str]
        trimFlag=trimFlag,             # type: Cal[[str], str]
        none8=(None,)*8,               # type: None8

        matcher=compileRegexExpression(
            r'(?:(\d{4})-)?' 
            r'(?:(\d{2})-)?' 
            r'(?:(\d{2}) )?' 
            r'(?:(\d{2}):)?' 
            r'(?:(\d{2}):)?' 
            r'(?:(\d{2})\.)?' 
            r'(?:(\d{3}))?' 
            r': ([A-Z]+):'
        ).search                         # type: Cal[[Any], SRE_Match]
):                                       # type: (...) -> Itrt[OptStr8PlusStr]

    for line in lines:
        match = matcher(line)
        matchTuple = match.groups() if match else none8

        if matchTuple[4] is None and matchTuple[3] is not None:
            # Hour & minute may be mixed up if cutoff at certain point
            #            (year, month, day , hour, minute       , second       , millisec     , flag
            matchTuple = (None, None , None, None, matchTuple[3], matchTuple[5], matchTuple[6], matchTuple[7])

        if matchTuple[-1] is not None:
            line = trimTime(line, matchTuple)
            line = trimFlag(line)
            yield matchTuple + (line.lstrip(': '),)
        else:
            # If flag is whole enough replace with the whole flag.
            line = line.lstrip()
            for combo, _len, whole in wholeEnoughs:
                if line[:_len] == combo:
                    line = line[_len:]
                    flag = whole
                    break
            else:
                flag = cutoffFlag

            yield None, None, None, None, None, None, None, flag, line.lstrip(': ')

def isStampCutoff(parsedLine, range6=tuple(xrange(6))):  # type: (OptStr9, Int6) -> bool
    for j in range6:
        if parsedLine[j] is None:
            return True
    return False

def interpolLines(parsedLines, none9=(None,)*9, interpol=interpolMissingStamps):
    # type: (..., None9, Cal[[OptStr9, OptStr9, OptStr9], Itrt[str]]) -> Lst[OptStr9]
    parsedLines = list(parsedLines)
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
                interpol(prevLine, parsedLine, nextLine)
            )

    return parsedLines
