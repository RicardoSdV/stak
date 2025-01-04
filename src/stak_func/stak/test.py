from src.stak_func.stak.block04_pathOps import pathSplitChar


minMaxOpen = iter([
    [],
    ['A', 'B', 'C', 'D'],
    ['A', 'B'],
    ['A', 'B', 'E', 'F', 'G', 'H'],
    [],
])

def diffAndRedundant(small, big):
    lastLinkInOld = small[-1] if len(small) != 0 else None
    isRedundant = True

    for el in big:
        if el == lastLinkInOld or lastLinkInOld is None:
            isRedundant = False

        if isRedundant:
            yield ' ' * len(el)
        else:
            yield el

def makeMinMaxDiff():  # type: (Itrt[Lst[str]]) -> Itrt[Lst[str]]
    isCallDiff = True
    prevLinks = next(minMaxOpen)
    for links in minMaxOpen:

        if isCallDiff:
            yield list(diffAndRedundant(prevLinks, links))
        else:
            yield list(diffAndRedundant(links, prevLinks))

        isCallDiff = not isCallDiff
        prevLinks = links

for el in makeMinMaxDiff():
    print el
