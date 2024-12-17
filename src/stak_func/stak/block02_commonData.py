"""
Data, manually inputted or injected by ..injectors.py
"""
from collections import OrderedDict

stakFlags = ('OMROLOCS', 'DATE', 'DATA', 'LABEL')
pStakFlags = (': OMROLOCS: ', ': DATE    : ', ': DATA    : ', ': LABEL   : ')  # This line was injected by injectors.py

omrolocsFlag , dateFlag , dataFlag , labelFlag  = stakFlags
pOmrolocsFlag, pDateFlag, pDataFlag, pLabelFlag = pStakFlags

stdFlags = ('DEBUG', 'INFO', 'NOTICE', 'WARNING', 'ERROR', 'CRITICAL', 'HACK', 'TRACE', 'ASSET')
paddedStdFlags = (': DEBUG   : ', ': INFO    : ', ': NOTICE  : ', ': WARNING : ', ': ERROR   : ', ': CRITICAL: ', ': HACK    : ', ': TRACE   : ', ': ASSET   : ')  # This line was injected by injectors.py

pStdFlagsByStdFlags = {'INFO': ': INFO    : ', 'CRITICAL': ': CRITICAL: ', 'NOTICE': ': NOTICE  : ', 'TRACE': ': TRACE   : ', 'HACK': ': HACK    : ', 'WARNING': ': WARNING : ', 'ASSET': ': ASSET   : ', 'ERROR': ': ERROR   : ', 'DEBUG': ': DEBUG   : '}  # This line was injected by injectors.py
allPflagsByFlags = {'INFO': ': INFO    : ', 'CRITICAL': ': CRITICAL: ', 'NOTICE': ': NOTICE  : ', 'TRACE': ': TRACE   : ', 'CUTOFF': ': CUTOFF  : ', 'OMROLOCS': ': OMROLOCS: ', 'HACK': ': HACK    : ', 'LABEL': ': LABEL   : ', 'DEBUG': ': DEBUG   : ', 'WARNING': ': WARNING : ', 'ASSET': ': ASSET   : ', 'ERROR': ': ERROR   : ', 'DATE': ': DATE    : ', 'DATA': ': DATA    : '}  # This line was injected by injectors.py

pStdFlagsByStdFlags['CUTOFF'] = ': CUTOFF  : '  # Manually padding ain't great
cutoffFlag = 'CUTOFF'

cutoffCombos = OrderedDict((('CRITICAL', 1), ('WARNING', 1), ('RITICAL', 1), ('NOTICE', 1), ('ITICAL', 1), ('ARNING', 1), ('RNING', 1), ('OTICE', 1), ('ASSET', 1), ('TICAL', 1), ('ERROR', 1), ('DEBUG', 1), ('TRACE', 1), ('HACK', 1), ('TICE', 1), ('RACE', 1), ('NING', 1), ('RROR', 1), ('INFO', 1), ('SSET', 1), ('ICAL', 1), ('EBUG', 1), ('ACE', 1), ('ACK', 1), ('CAL', 1), ('SET', 1), ('ICE', 1), ('ROR', 1), ('BUG', 1), ('NFO', 1), ('ING', 1), ('FO', 1), ('NG', 1), ('CK', 1), ('AL', 1), ('CE', 2), ('ET', 1), ('UG', 1), ('OR', 1), ('E', 2), ('G', 2), ('K', 1), ('O', 1), ('L', 1), ('R', 1), ('T', 1)))  # This line was injected by injectors.py
wholeEnoughs = {'NOTICE': 'NOTICE', 'RNING': 'WARNING', 'ACE': 'TRACE', 'ACK': 'HACK', 'HACK': 'HACK', 'EBUG': 'DEBUG', 'TICE': 'NOTICE', 'CAL': 'CRITICAL', 'OTICE': 'NOTICE', 'ASSET': 'ASSET', 'RACE': 'TRACE', 'FO': 'INFO', 'SET': 'ASSET', 'ITICAL': 'CRITICAL', 'NG': 'WARNING', 'WARNING': 'WARNING', 'NING': 'WARNING', 'ROR': 'ERROR', 'BUG': 'DEBUG', 'CK': 'HACK', 'CRITICAL': 'CRITICAL', 'TICAL': 'CRITICAL', 'NFO': 'INFO', 'K': 'HACK', 'AL': 'CRITICAL', 'O': 'INFO', 'L': 'CRITICAL', 'R': 'ERROR', 'ICE': 'NOTICE', 'ERROR': 'ERROR', 'DEBUG': 'DEBUG', 'ET': 'ASSET', 'ARNING': 'WARNING', 'INFO': 'INFO', 'SSET': 'ASSET', 'TRACE': 'TRACE', 'T': 'ASSET', 'RITICAL': 'CRITICAL', 'ICAL': 'CRITICAL', 'UG': 'DEBUG', 'ING': 'WARNING', 'OR': 'ERROR', 'RROR': 'ERROR'}  # This line was injected by injectors.py

# Trace log stuff
traceFlag = 'TRACE'
callableNames = {'isStampCutoff', 'OrderedDict', 'makeDirPaths', 'formatCompStak', 'basename', 'saveStdStakSplice', 'datetime', 'savePrimiStd', 'pubClsMethCond', 'prodCallTreeUntilReset', 'partial', 'unixStampToTupleOfInts', 'privClsMethCond', 'dateEntry', 'appendToLog', 'preProcessLog', 'izip', 'getVariDirPath', 'trimTime', 'joinStrLinkWithDataForLogging', 'matcher', 'linksGen', 'formatPrimiStak', 'autoLocals', 'isdir', 'retArgs', 'linksFromFrame', 'prettyfyLines', 'splitLinkToStr', 'exists', 'stdStakSplice', 'getPrintDirPath', 'tupleOfIntsToTupleOfStrs', 'getCompStdStakSplicePaths', 'addSuffix', 'isfile', 'splitLinkFromFrame', 'tupleOfStrsToStr', 'fmtOmrolocsEntry', 'splitLinksCallChain', 'makedirs', 'clearLog', 'compressLines', 'removePrintDir', 'interpolMissingStamps', 'makeFullStrLinkCallChains', 'getStdPrimiLogFilePaths', 'formatCompStdStakSplice', '_uniqueStakCompPaths', 'labelLog', 'trimFilePathAddLineno', 'extendLog', 'getStakCompFilePath', 'CompressionFormatList', 'fmtDataEntry', 'parseLines', 'FunctionType', 'mroClsNsGen', 'mroLinkToStrLink', '_getframe', 'jointLinksCallChain', 'delTrace', 'getStdStakSplicePaths', 'Log', 'splitext', 'getStdLogPaths', 'unixStampToStr', 'joinFileLink', 'traceEntry', 'jointLinkFromFrame', 'makeFilePathUnique', 'formatPrimiStd', 'saveCompStdStakSplice', 'setTrace', 'reloadSettings', 'traceTerminatorEntry', 'reloadData', 'compressLinks', 'unixStampToDatetime', 'omropocs', '_uniqueCompStdStakSplicePaths', 'join', 'splitStampFromTheRest', 'trimFlagIfPoss', 'joinMroLink', 'OldStyleClsType', 'saveCompStak', 'traceOriginatorEntry', 'privInsMethCond', 'prettyfyLine', 'compileRegexExpression', 'datetimeToTupleOfInts', 'fmtLabelEntry', 'formatStdStakSplice', 'parseStdLogs', '_uniqueStdPrimiPaths', 'getStakPrimiFilePath', 'dirname', 'formatTraceLog', 'writeLogsToFile', 'spliceStakLogWithStdLog', '_uniqueStakPrimiPaths', 'pubInsMethCond', 'omrolocs', '_uniqueStdStakSplicePaths', 'linksAndFirstFrameLocalsFromFrame', 'repeat', 'trace', 'parseAndInterpolLines', 'trimFlag', 'compress', 'rmtree', 'data', 'saveAll', 'fmtDateEntry', 'getPrimiDirPath', 'savePrimiStak', 'unixStampToTupleOfStrs', 'time', 'omrolocsalad'}  # This line was injected by injectors.py


def reloadData():
    from sys import modules
    reload(modules[__name__])
