""" State: mutable runtime data. Changed by the program. """

from .block00_autoImports import *

class eCnt(object): __slots__ = ('cnt', )
eCnt = eCnt()
eCnt.cnt = 0

stakLog    = []              # type: StakLog
stakLogApp = stakLog.append  # type: Append
stakLogExt = stakLog.extend  # type: Extend

traceLog    = Deque()          # type: TraceLog
traceLogApp = traceLog.append  # type: Append
traceLogExt = traceLog.extend  # type: Extend

splitLinks    = []
splitLinksExt = splitLinks.extend

splitLinks_headIdxByPathLnHash = {}

jointLinks = []
jointLinksApp = jointLinks.append

jointLinks_strByPathLnHash = {}

callTimes    = []                # type: list
callTimesApp = callTimes.append  # type: Append

class traceState(object): __slots__ = ('mayHave', )
traceState = traceState()
traceState.mayHave = False

class interceptState(object): __slots__ = ('intercept', )
interceptState = interceptState()
interceptState.intercept = 0

ogLoggers = {}

events = {}  # type: Dic[str, Seq[Cal]]
