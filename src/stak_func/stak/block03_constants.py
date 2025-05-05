"""
Constants, i.e. they don't change during an interpreter run. Manually inputted or injected by ..injectors.py
"""
from collections import OrderedDict

stakVersion = 1

stakFlags = ('OMROLOCS', 'LOCSALAD', 'DATE', 'DAFF', 'LABEL')
pStakFlags = (': OMROLOCS: ', ': DATE    : ', ': DAFF    : ', ': LABEL   : ')  # This line was injected by injectors.py

omrolocsFlag , locsaladFlag, dateFlag , daffFlag , labelFlag  = stakFlags
pOmrolocsFlag, pDateFlag, pDataFlag, pLabelFlag = pStakFlags


traceFlags  = ('SET', 'CAL', 'RET', 'DEL')
pTraceFlags = (': SET: ', ': CAL: ', ': RET: ', ': DEL: ')  # This line was injected by injectors.py

setFlag , callFlag , retFlag , delFlag  = traceFlags
pSetFlag, pCallFlag, pRetFlag, pDelFlag = pTraceFlags

callFlags = {setFlag, callFlag}
retFlags  = {retFlag, delFlag }


stdFlags = ('DEBUG', 'INFO', 'NOTICE', 'WARNING', 'ERROR', 'CRITICAL', 'HACK', 'TRACE', 'ASSET')
paddedStdFlags = (': DEBUG   : ', ': INFO    : ', ': NOTICE  : ', ': WARNING : ', ': ERROR   : ', ': CRITICAL: ', ': HACK    : ', ': TRACE   : ', ': ASSET   : ')  # This line was injected by injectors.py

pStdFlagsByStdFlags = {'INFO': ': INFO    : ', 'CRITICAL': ': CRITICAL: ', 'NOTICE': ': NOTICE  : ', 'TRACE': ': TRACE   : ', 'HACK': ': HACK    : ', 'WARNING': ': WARNING : ', 'ASSET': ': ASSET   : ', 'ERROR': ': ERROR   : ', 'DEBUG': ': DEBUG   : '}  # This line was injected by injectors.py
allPflagsByFlags = {'INFO': ': INFO    : ', 'DAFF': ': DAFF    : ', 'NOTICE': ': NOTICE  : ', 'TRACE': ': TRACE   : ', 'CUTOFF': ': CUTOFF  : ', 'HACK': ': HACK    : ', 'CRITICAL': ': CRITICAL: ', 'LABEL': ': LABEL   : ', 'DEBUG': ': DEBUG   : ', 'WARNING': ': WARNING : ', 'ASSET': ': ASSET   : ', 'ERROR': ': ERROR   : ', 'DATE': ': DATE    : ', 'OMROLOCS': ': OMROLOCS: '}  # This line was injected by injectors.py

pStdFlagsByStdFlags['CUTOFF'] = ': CUTOFF  : '  # Manually padding ain't great
cutoffFlag = 'CUTOFF'

cutoffCombos = OrderedDict((('CRITICAL', 1), ('WARNING', 1), ('RITICAL', 1), ('NOTICE', 1), ('ITICAL', 1), ('ARNING', 1), ('RNING', 1), ('OTICE', 1), ('ASSET', 1), ('TICAL', 1), ('ERROR', 1), ('DEBUG', 1), ('TRACE', 1), ('HACK', 1), ('TICE', 1), ('RACE', 1), ('NING', 1), ('RROR', 1), ('INFO', 1), ('SSET', 1), ('ICAL', 1), ('EBUG', 1), ('ACE', 1), ('ACK', 1), ('CAL', 1), ('SET', 1), ('ICE', 1), ('ROR', 1), ('BUG', 1), ('NFO', 1), ('ING', 1), ('FO', 1), ('NG', 1), ('CK', 1), ('AL', 1), ('CE', 2), ('ET', 1), ('UG', 1), ('OR', 1), ('E', 2), ('G', 2), ('K', 1), ('O', 1), ('L', 1), ('R', 1), ('T', 1)))  # This line was injected by injectors.py
wholeEnoughs = {'NOTICE': 'NOTICE', 'RNING': 'WARNING', 'ACE': 'TRACE', 'ACK': 'HACK', 'HACK': 'HACK', 'EBUG': 'DEBUG', 'TICE': 'NOTICE', 'CAL': 'CRITICAL', 'OTICE': 'NOTICE', 'ASSET': 'ASSET', 'RACE': 'TRACE', 'FO': 'INFO', 'SET': 'ASSET', 'ITICAL': 'CRITICAL', 'NG': 'WARNING', 'WARNING': 'WARNING', 'NING': 'WARNING', 'ROR': 'ERROR', 'BUG': 'DEBUG', 'CK': 'HACK', 'CRITICAL': 'CRITICAL', 'TICAL': 'CRITICAL', 'NFO': 'INFO', 'K': 'HACK', 'AL': 'CRITICAL', 'O': 'INFO', 'L': 'CRITICAL', 'R': 'ERROR', 'ICE': 'NOTICE', 'ERROR': 'ERROR', 'DEBUG': 'DEBUG', 'ET': 'ASSET', 'ARNING': 'WARNING', 'INFO': 'INFO', 'SSET': 'ASSET', 'TRACE': 'TRACE', 'T': 'ASSET', 'RITICAL': 'CRITICAL', 'ICAL': 'CRITICAL', 'UG': 'DEBUG', 'ING': 'WARNING', 'OR': 'ERROR', 'RROR': 'ERROR'}  # This line was injected by injectors.py

callableNames = {'isStampCutoff', 'OrderedDict', 'makeDirPaths', 'formatCompStak', 'basename', 'saveTrace', 'saveStdStakSplice', 'datetime', 'savePrimiStd', 'pubClsMethCond', 'replaceRedundantWithSpacesInPlace', 'getSegFlag', 'privClsMethCond', 'write', 'appendToLog', 'formatTrace', 'getCompStakPaths', 'getCompactTracePaths', 'joinEventGroups', 'makeCallChain', 'formatCompStdStakSplice', 'izip', 'getVariDirPath', 'trimTime', 'read', 'stdStakSplice', 'handleLine', 'formatPrimiStak', 'autoLocals', 'isdir', 'iterMroUntilDefClsFound', 'prettyfyLines', 'getPrimiStdPaths', 'exists', 'splitIntsFromStrs', 'fmtDelEntry', 'getPrintDirPath', 'prettyfyLine', 'getCompStdStakSplicePaths', 'dirname', 'isfile', 'removeStakCallables', 'getTracePaths', 'tupleOfStrsToStr', 'savePrimiStak', 'makedirs', 'fmtCallEntry', 'compressLines', 'removePrintDir', 'fmtSetEntry', 'interpolMissingStamps', 'fmtOmrolocsEntry', 'firstFrameAndData', 'Settings', 'extendLog', 'clearLogs', 'handleCall', 'CompressionFormatList', 'entriesWithLinksJoin', 'parseLines', 'privInsMethCond', 'mroClsNsGen', '_getframe', 'fmtRetEntry', 'delTrace', 'getStdStakSplicePaths', 'splitext', 'getStdLogPaths', 'unixStampToStr', 'makeFilePathUnique', 'makeSplitLink', 'labelLogs', 'formatPrimiStd', 'saveCompStdStakSplice', 'setTrace', 'compileRegexExpression', 'handleRet', 'makeOpenCalls', 'handleExc', 'formatStdStakSplice', 'partial', 'spliceStakLogWithStdLog', 'omropocs', 'fmtDataEntry', 'joinLink', 'join', 'getPrimiStakPaths', 'parseStdLogs', 'trimFlagIfPoss', 'appendToTrace', 'makeMinMaxDiff', 'OldStyleClsType', 'saveCompStak', 'FunctionType', 'tryCall', 'joinLinks', 'fmtLabelEntry', 'splitStampFromTheRest', 'parseAndInterpolLines', 'addSuffix', 'compressCallChains', 'formatTraceLog', 'joinStrLinkWithDataForLogging', 'writeLogsToFile', 'diffAndRedundant', 'EventCounter', 'pubInsMethCond', 'omrolocs', 'trace', 'trimFlag', 'compress', 'rmtree', 'formatCompactTrace', 'dateEntries', 'saveCompactTrace', 'saveAll', 'fmtDateEntry', 'getPrimiDirPath', 'unixStampToTupleOfStrs', 'makeMinMaxOpen', 'time', 'omrolocsalad'}  # This line was injected by injectors.py

defaultSegFlag = 'main'

logFilesExt = '.log'
jsonFilesExt = '.json'

blockPrefix = 'block'

backupsPath = r'C:\STAK_backups'
