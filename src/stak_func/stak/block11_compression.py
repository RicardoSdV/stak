from .block00_typing import *
from .block02_settingObj import so

# TODO: This file really needs a refactoring and some perf testing and improvement
#  since its the main bottleneck when saving. But its too complicated to remove the
#  recursion in a performant way so I can't be bothered right now, but one day.


class CFL(list):
    """ Compression Format List: with count of repetitions this list represents. """
    def __init__(self, cnt=1, args=()):  # type: (int, Itrb) -> None
        super(CFL, self).__init__(args)
        self.cnt = cnt

def compress(postPassCfl, CFL=CFL):  # type: (CFL, Typ[CFL]) -> CFL

    for groupSize in xrange(1, min(len(postPassCfl) // 2, so.maxCompressGroupSize)):

        prePassCfl = postPassCfl
        postPassCfl = CFL(prePassCfl.cnt)

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

                    compressedGroup = CFL(groups_cnt, thisGroup)
                    postPassCfl.append(compressedGroup)

                    thisGroupStartI = nextGroupStartI
                    thisGroupEndI = nextGroupEndI

                    nextGroupStartI += groupSize
                    nextGroupEndI += groupSize

                    groups_cnt = 1

            thisGroup = prePassCfl[thisGroupStartI: thisGroupEndI + 1]
            nextGroup = prePassCfl[nextGroupStartI: nextGroupEndI + 1]

    return postPassCfl

def prettyfyLine(lineCfl):  # type: (CFL) -> str
    result = ''

    if lineCfl.cnt > 1:
        result += '%sx[' % lineCfl.cnt

    for el in lineCfl:
        if isinstance(el, CFL):
            result += prettyfyLine(el)
        elif isinstance(el, str):
            result += (el + ' <- ')
        else:
            raise TypeError('Wrong type in compressed callChain: type(el)', type(el))

    if lineCfl.cnt > 1:
        result = result.rstrip(' <- ')
        result += '] <- '

    return result

def compressCallChains(
        callChainsWithStrLinks,      # type: Itrb[Tup[Str4, Uni[str, Tup[str, ...]]]]

        _prettyfyLine = prettyfyLine,  # type: Cal[[CFL], str]
        _compress     = compress,      # type: Cal[[CFL], CFL]
        _CFL          = CFL            # type: Typ[CFL]

):  # type: (...) -> Itrt[Tup[Str4, Uni[str, Tup[str, ...]]]]

    for stamp, callChain in callChainsWithStrLinks:
        if not isinstance(callChain, tuple):
            yield stamp, callChain  # Is date entry or label
            continue

        cfl = _CFL(1, callChain)
        compressedCfl = _compress(cfl)
        prettyLine = _prettyfyLine(compressedCfl).strip(' <- ')

        yield stamp, prettyLine

def prettyfyLines(linesCfl, depth=0):  # type: (CFL, int) -> Lst[str]
    indent = depth * '    '
    result = []; append = result.append; extend = result.extend

    if linesCfl.cnt > 1:
        append('%s%sx\n' % ((depth - 1) * '    ', linesCfl.cnt))

    for el in linesCfl:
        elClass = el.__class__
        if elClass is CFL:
            extend(prettyfyLines(el, depth + 1))
        elif elClass is str:
            append(indent + el + '\n')
        else:
            raise TypeError('Wrong type in compressed list: ', elClass)
    return result

def prettyCompressLines(entries):  # type: (Itrb[Tup[..., str]]) -> Lst[str]
    cflLines = CFL(1, [entry[-1] for entry in entries])
    compressedCfls = compress(cflLines)
    prettyLines = prettyfyLines(compressedCfls)
    return prettyLines

