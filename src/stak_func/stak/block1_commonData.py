__doc__ = None
"""
Holds data referenced by more than one block, otherwise the data is defined in its block.
"""

from .block0_typing import *

# Names that should change relatively often
printDir    = 'print'
taskDir     = 'task'
eventLabels = ['PRE-EVENT-1', 'POST-EVENT-1', 'PRE-EVENT-2', 'POST-EVENT-2']
eventCnt    = 0

# Names that can but really shouldn't change that often
rootDir       = '.STAK'
primitivesDir = 'primitives'
variantsDir   = 'variants'
stakLogFile   = 'stak.log'
traceLogFile  = 'trace.log'
stdLogFiles   = ('stdLogA.log', 'stdLogB.log')
maxCompressGroupSize = 100  # Increases compress times exponentially

# Stak log stuff
log = []  # type: Lst[Tup[float, str, Uni[Tup[Uni[Tup[str, int, str], Tup[Lst[str], str]], ...]]]]
appendToLog = log.append
extendLog   = log.extend

# Trace log stuff
traceLog = []
openFuncs = set()  # type: Set[FrameType]
appendToTraceLog = traceLog.append

# Flags
stakFlags = ('OMROLOCS', 'DATE', 'DATA', 'LABEL')
pStakFlags = (': OMROLOCS: ', ': DATE    : ', ': DATA    : ', ': LABEL   : ')  # This line was injected by injectors.py

stdFlags = ('DEBUG', 'INFO', 'NOTICE', 'WARNING', 'ERROR', 'CRITICAL', 'HACK', 'TRACE', 'ASSET')
paddedStdFlags = (': DEBUG   : ', ': INFO    : ', ': NOTICE  : ', ': WARNING : ', ': ERROR   : ', ': CRITICAL: ', ': HACK    : ', ': TRACE   : ', ': ASSET   : ')  # This line was injected by injectors.py

pStdFlagsByStdFlags = {'INFO': ': INFO    : ', 'CRITICAL': ': CRITICAL: ', 'NOTICE': ': NOTICE  : ', 'TRACE': ': TRACE   : ', 'HACK': ': HACK    : ', 'WARNING': ': WARNING : ', 'ASSET': ': ASSET   : ', 'ERROR': ': ERROR   : ', 'DEBUG': ': DEBUG   : '}  # This line was injected by injectors.py
allPflagsByFlags = {'INFO': ': INFO    : ', 'CRITICAL': ': CRITICAL: ', 'NOTICE': ': NOTICE  : ', 'TRACE': ': TRACE   : ', 'CUTOFF': ': CUTOFF  : ', 'OMROLOCS': ': OMROLOCS: ', 'HACK': ': HACK    : ', 'LABEL': ': LABEL   : ', 'DEBUG': ': DEBUG   : ', 'WARNING': ': WARNING : ', 'ASSET': ': ASSET   : ', 'ERROR': ': ERROR   : ', 'DATE': ': DATE    : ', 'DATA': ': DATA    : '}  # This line was injected by injectors.py

pStdFlagsByStdFlags['CUTOFF'] = ': CUTOFF  : '  # Manually padding ain't great
cutoffFlag = 'CUTOFF'

traceFlag = 'TRACE'


# Trace log stuff
callableNames = {'appendToLog', 'extendLog', 'appendToTraceLog', 'jointLinkFromFrame', 'splitLinkFromFrame', 'jointLinksCallChain', 'splitLinksCallChain', 'traceOriginatorEntry', 'traceTerminatorEntry', 'saveStakLogToPrimitives', 'saveTraceLogToPrimitives', 'saveStdLogsToPrimitives', 'basename', 'delTrace', 'gettrace', '__spliceGen', 'join', '__pubClsMethCond', 'clear', '__saveSplicedToVariants', '__prettyfyLine', '__interpolStampGen', '__trimFlag', '_dateEntry', '__partStrLinkCreator', '__trimFlagIfPoss', 'rmtree', '__linksAndFirstFrameLocalsGen', 'makedirs', 'setTrace', '__joinFileLink', 'dirname', 'exists', '__unixStampToTupleOfInts', 'settrace', '__strLinkCallChainGen', 'save', '__parseAndInterpolLines', '__joinTraceEntriesUntilReversal', '__mroClsNsGen', '__OldStyleClsType', '__formatLinesForLinesCompression', 'matcher', '__retArgs', '__formatStakLog', 'FunctionType', 'omropocs', '__call__', '__formatParsedStdLog', '__genPathDirPrimi', '__compress', 'autoLocals', '__trimFilePathAddLinenoGen', '_getframe', '__mroLinkToStrLink', '__compressLinksGen', 'l', '__data', '__tupleOfIntsToTupleOfStrs', '__parsedLinesGen', 'datetime', '__datetimeToTupleOfInts', '__pubInsMethCond', '__prettyfyLines', '__privClsMethCond', '__genPathDirPrint', '__tupleOfStrsToStr', 'time', '__init__', '__parsedStdLogGen', '__privInsMethCond', 'rp', '__joinMroLink', '__splitStampFromTheRest', '__saveCompressedStakLogToVariants', 'label', '__preProcessLogGen', '__saveCompressedSplicedLogs', '__trimTime', '__addSuffix', '__unixStampToTupleOfStrs', 'omrolocs', '__saveLogsToFile', '__linksGen', 'splitext', 'rmPrint', 'isdir', '__compressLines', '__genPathDirVari', '__genPathLogStak', 'data', '__traceEntry', 'c', 'isfile', '__splitLinkToStr', '__genPathLogTrace', '__formatTraceLog', '__fileUnique', '__genPathLogsStd', 's', '__linkFromFrame', 'omrolocsalad', 'unixStampToDatetime', '__unixStampToStr', 'CompressionFormatList', 'tupleOfStrsToStr'}  # This line was injected by injectors.py
