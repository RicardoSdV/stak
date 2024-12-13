from .block1_commonData import *


class CompressionFormatList(list):
    # List that holds extra attributes for internal use in compression

    def __init__(self, cnt=1, rep='', *args):  # type: (int, str, Any) -> None
        super(CompressionFormatList, self).__init__(args)
        self.cnt = cnt
        self.rep = rep

def compress(postPassCfl):
    represents = postPassCfl.rep

    for groupSize in range(1, min(len(postPassCfl) // 2, maxCompressGroupSize)):

        prePassCfl = postPassCfl
        postPassCfl = CompressionFormatList(cnt=prePassCfl.cnt, rep=prePassCfl.rep)

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

                    compressed_group = CompressionFormatList(groups_cnt, represents, *thisGroup)
                    postPassCfl.append(compressed_group)

                    thisGroupStartI = nextGroupStartI
                    thisGroupEndI = nextGroupEndI

                    nextGroupStartI += groupSize
                    nextGroupEndI += groupSize

                    groups_cnt = 1

            thisGroup = prePassCfl[thisGroupStartI: thisGroupEndI + 1]
            nextGroup = prePassCfl[nextGroupStartI: nextGroupEndI + 1]

    return postPassCfl

def prettyfyLine(lineCfl):  # type: (CompressionFormatList) -> str
    result = ''

    if lineCfl.cnt > 1:
        result += '{}x['.format(lineCfl.cnt)

    for el in lineCfl:
        if isinstance(el, CompressionFormatList):
            assert el.rep == 'line'
            result += prettyfyLine(el)
        elif isinstance(el, str):
            result += (el + ' <- ')
        else:
            raise TypeError('Wrong type in compressed stack: type(el)', type(el))

    if lineCfl.cnt > 1:
        result = result.rstrip(' <- ')
        result += (']' + ' <- ')

    return result

def compressLinksGen(callChainsWithStrLinks):
    # type: (Tup[Tup[StrsStamp, str, Uni[str, Tup[str, ...]]], ...]) -> Itrt[Tup[StrsStamp, str, str]]

    omrolocsFlag, _prettyfyLine, _compress = stakFlags[0], prettyfyLine, compress
    return (
        (
            stamp,
            flag,
            prettyfyLine(
                compress(
                    CompressionFormatList(1, 'line', *theRest)
                )
            ).rstrip(' <- ')
            if flag == omrolocsFlag else theRest,
        )
        for stamp, flag, theRest in callChainsWithStrLinks
    )

def compressLines(lines):  # type: (Lst[str]) -> Lst[str]
    return prettyfyLines(
        compress(
            CompressionFormatList(1, 'parsedLines', *lines)
        )
    )

def prettyfyLines(linesCfl, depth=0):
    indent = depth * '    '
    result = []

    if linesCfl.cnt > 1:
        result.append('{}{}x'.format((depth - 1) * '    ', linesCfl.cnt))

    for el in linesCfl:
        if isinstance(el, CompressionFormatList):
            assert el.rep == 'parsedLines'
            result.extend(prettyfyLines(el, depth + 1))
        elif isinstance(el, str):
            result.append(indent + el)
        else:
            raise TypeError('Wrong type in compressed list: type(el)', type(el))
    return result

