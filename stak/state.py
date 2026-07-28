""" State: mutable runtime data. Changed by the program. """

from .lib import Deque, timeClock, timeTime

config = {}

class Cnt(object):
    __slots__ = ('cnt', )
    def __init__(self):
        self.cnt = 0

eCnt = Cnt()

stakLog    = []
stakLogApp = stakLog.append
stakLogExt = stakLog.extend

traceLog    = Deque()
traceLogApp = traceLog.append
traceLogExt = traceLog.extend

idsBySplitLink    = {}
splitLinksById    = []
splitLinksByIdApp = splitLinksById.append

jointLinksById    = {}

jointLinks_strByPathLnHash = {}

callTimes    = []
callTimesApp = callTimes.append

class traceState(object): __slots__ = ('mayHave', )
traceState = traceState()
traceState.mayHave = False

class interceptState(object): __slots__ = ('intercept', )
interceptState = interceptState()
interceptState.intercept = 0

absRefStamp = timeTime()
clockRefStamp = timeClock()  # Clock call needed to start the clock if no one called it yet.

ogLoggers = {}
