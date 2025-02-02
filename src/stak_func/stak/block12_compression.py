from functools import partial

from .block00_typing import *
from .block01_settings import maxCompressGroupSize
from .block03_commonData import omrolocsFlag


class CompressionFormatList(list):
    # List that holds extra attributes for internal use in compression
    # self.cnt -> Count of repetitions this list represents
    # self.rep -> What does this list represent? some SplitLink s? some callChains?

    def __init__(self, cnt=1, rep='', *args):  # type: (int, str, Any) -> None
        super(CompressionFormatList, self).__init__(args)
        self.cnt = cnt
        self.rep = rep

def compress(
        postPassCfl,               # type: CompressionFormatList
        CFL=CompressionFormatList  # type: Typ[CompressionFormatList]
):                                 # type: (...) -> CompressionFormatList

    represents = postPassCfl.rep
    for groupSize in xrange(1, min(len(postPassCfl) // 2, maxCompressGroupSize)):

        prePassCfl = postPassCfl
        postPassCfl = CFL(cnt=prePassCfl.cnt, rep=prePassCfl.rep)

        thisGroupStartI = 0
        thisGroupEndI = groupSize - 1

        nextGroupStartI = groupSize
        nextGroupEndI = 2 * groupSize - 1

        thisGroup = prePassCfl[thisGroupStartI: thisGroupEndI + 1]
        nextGroup = prePassCfl[nextGroupStartI: nextGroupEndI + 1]

        groups_cnt = 1

        while thisGroup:

            if thisGroup == nextGroup:
                groups_cnt += 1

                nextGroupStartI += groupSize
                nextGroupEndI += groupSize

            else:
                if groups_cnt == 1:
                    postPassCfl.append(thisGroup[0])

                    thisGroupStartI += 1
                    thisGroupEndI += 1

                    nextGroupStartI += 1
                    nextGroupEndI += 1

                else:  # There has been one or more repetitions of thisGroup

                    compressedGroup = CompressionFormatList(groups_cnt, represents, *thisGroup)
                    postPassCfl.append(compressedGroup)

                    thisGroupStartI = nextGroupStartI
                    thisGroupEndI = nextGroupEndI

                    nextGroupStartI += groupSize
                    nextGroupEndI += groupSize

                    groups_cnt = 1

            thisGroup = prePassCfl[thisGroupStartI: thisGroupEndI + 1]
            nextGroup = prePassCfl[nextGroupStartI: nextGroupEndI + 1]

    return postPassCfl

isCfl = partial(isinstance, __class_or_tuple=CompressionFormatList)
isStr = partial(isinstance, __class_or_tuple=str)

def prettyfyLine(lineCfl, _isCfl=isCfl, _isStr=isStr):  # type: (CompressionFormatList, IsIns, IsIns) -> str
    result = ''

    if lineCfl.cnt > 1:
        result += '{}x['.format(lineCfl.cnt)

    for el in lineCfl:
        if _isCfl(el):
            assert el.rep == 'line'
            result += prettyfyLine(el)
        elif _isStr(el):
            result += (el + ' <- ')
        else:
            raise TypeError('Wrong type in compressed stack: type(el)', type(el))

    if lineCfl.cnt > 1:
        result = result.rstrip(' <- ')
        result += '] <- '

    return result

def compressCallChains(
        callChainsWithStrLinks,      # type: Itrb[Tup[Str4, str, str, Uni[str, Tup[str, ...]]]]
        _omrolocsFlag=omrolocsFlag,  # type: str
        pretty=prettyfyLine,         # type: Cal[[CompressionFormatList], str]
        comp=compress,               # type: Cal[[CompressionFormatList], CompressionFormatList]
        CFL=CompressionFormatList    # type: Typ[CompressionFormatList]
):  # type: (...) -> Itrt[Tup[Str4, str, str, str]]

    return (
        (stamp, segFlag, callerFlag,
         pretty(comp(CFL(1, 'line', *theRest))).rstrip(' <- ') if callerFlag == _omrolocsFlag else theRest)
        for stamp, segFlag, callerFlag, theRest in callChainsWithStrLinks
    )

def prettyfyLines(linesCfl, depth=0, _isCfl=isCfl, _isStr=isStr):
    # type: (CompressionFormatList, int, IsIns, IsIns) -> Lst[str]
    indent = depth * '    '
    result = []
    appendToResult = result.append
    extendResult = result.extend

    if linesCfl.cnt > 1:
        appendToResult('{}{}x'.format((depth - 1) * '    ', linesCfl.cnt))

    for el in linesCfl:
        if isCfl(el):
            assert el.rep == 'parsedLines'
            extendResult(prettyfyLines(el, depth + 1))
        elif isStr(el):
            appendToResult(indent + el)
        else:
            raise TypeError('Wrong type in compressed list: ', type(el))
    return result

def compressLines(lines):  # type: (Lst[str]) -> Lst[str]
    return prettyfyLines(
        compress(
            CompressionFormatList(1, 'parsedLines', *lines)
        )
    )
