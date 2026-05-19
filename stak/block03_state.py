""" State: mutable runtime data. Changed by the program. """

from .block00_autoImports import *

class Cnt(object):
    __slots__ = ('cnt', )
    def __init__(self, initCnt=0):
        self.cnt = 0

eCnt = Cnt()

stakLog    = []              # type: StakLog
stakLogApp = stakLog.append  # type: Append
stakLogExt = stakLog.extend  # type: Extend

traceLog    = Deque()          # type: TraceLog
traceLogApp = traceLog.append  # type: Append
traceLogExt = traceLog.extend  # type: Extend

IdsBySplitLink    = {}  # type: Dic[tuple, int]
splitLinksById    = []  # type: Lst[tuple]
splitLinksByIdApp = splitLinksById.append  # type: Append

jointLinksById    = {}  # type: Dic[int, str]

jointLinks_strByPathLnHash = {}

callTimes    = []                # type: list
callTimesApp = callTimes.append  # type: Append

class traceState(object): __slots__ = ('mayHave', )
traceState = traceState()
traceState.mayHave = False

class interceptState(object): __slots__ = ('intercept', )
interceptState = interceptState()
interceptState.intercept = 0

absRefStamp = time()
clockRefStamp = clock()  # Clock call needed to start the clock if no one called it yet.

ogLoggers = {}

events = {}  # type: Dic[str, Seq[Cal]]
