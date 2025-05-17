"""
Constants, i.e. they don't change during an interpreter run. Manually inputted or injected by ..injectors.py
"""
from collections import OrderedDict

stakVersion = 1

stakFlags = ('OMROLOCS', 'LOCSALAD', 'DATE', 'DAFF', 'LABEL')
pStakFlags = (': OMROLOCS: ', ': LOCSALAD: ', ': DATE    : ', ': DAFF    : ', ': LABEL   : ')  # This line was injected by injectors.py

omrolocsFlag , locsaladFlag, dateFlag , daffFlag , labelFlag  = stakFlags
pOmrolocsFlag, pLocsalad, pDateFlag, pDataFlag, pLabelFlag = pStakFlags


traceFlags  = ('SET', 'CAL', 'RET', 'DEL')
pTraceFlags = (': SET: ', ': CAL: ', ': RET: ', ': DEL: ')  # This line was injected by injectors.py

setFlag , callFlag , retFlag , delFlag  = traceFlags
pSetFlag, pCallFlag, pRetFlag, pDelFlag = pTraceFlags

callFlags = {setFlag, callFlag}
retFlags  = {retFlag, delFlag }


stdFlags = ('DEBUG', 'INFO', 'NOTICE', 'WARNING', 'ERROR', 'CRITICAL', 'HACK', 'TRACE', 'ASSET', 'WWISE', 'DATA')
paddedStdFlags = (': DEBUG   : ', ': INFO    : ', ': NOTICE  : ', ': WARNING : ', ': ERROR   : ', ': CRITICAL: ', ': HACK    : ', ': TRACE   : ', ': ASSET   : ', ': WWISE   : ', ': DATA    : ')  # This line was injected by injectors.py

pStdFlagsByStdFlags = {'INFO': ': INFO    : ', 'CRITICAL': ': CRITICAL: ', 'NOTICE': ': NOTICE  : ', 'TRACE': ': TRACE   : ', 'WWISE': ': WWISE   : ', 'HACK': ': HACK    : ', 'WARNING': ': WARNING : ', 'ASSET': ': ASSET   : ', 'ERROR': ': ERROR   : ', 'DEBUG': ': DEBUG   : ', 'DATA': ': DATA    : '}  # This line was injected by injectors.py
allPflagsByFlags = {'INFO': ': INFO    : ', 'DAFF': ': DAFF    : ', 'NOTICE': ': NOTICE  : ', 'LOCSALAD': ': LOCSALAD: ', 'TRACE': ': TRACE   : ', 'CUTOFF': ': CUTOFF  : ', 'DATA': ': DATA    : ', 'WWISE': ': WWISE   : ', 'HACK': ': HACK    : ', 'CRITICAL': ': CRITICAL: ', 'LABEL': ': LABEL   : ', 'DEBUG': ': DEBUG   : ', 'WARNING': ': WARNING : ', 'ASSET': ': ASSET   : ', 'ERROR': ': ERROR   : ', 'DATE': ': DATE    : ', 'OMROLOCS': ': OMROLOCS: '}  # This line was injected by injectors.py

pStdFlagsByStdFlags['CUTOFF'] = ': CUTOFF  : '  # Manually padding ain't great
cutoffFlag = 'CUTOFF'

cutoffCombos = OrderedDict((('CRITICAL', 1), ('WARNING', 1), ('RITICAL', 1), ('NOTICE', 1), ('ITICAL', 1), ('ARNING', 1), ('RNING', 1), ('WWISE', 1), ('OTICE', 1), ('ASSET', 1), ('TICAL', 1), ('ERROR', 1), ('DEBUG', 1), ('TRACE', 1), ('HACK', 1), ('TICE', 1), ('RACE', 1), ('DATA', 1), ('NING', 1), ('RROR', 1), ('INFO', 1), ('SSET', 1), ('WISE', 1), ('ICAL', 1), ('EBUG', 1), ('ACE', 1), ('ATA', 1), ('ACK', 1), ('CAL', 1), ('ISE', 1), ('SET', 1), ('ICE', 1), ('ROR', 1), ('BUG', 1), ('NFO', 1), ('ING', 1), ('FO', 1), ('NG', 1), ('TA', 1), ('CK', 1), ('AL', 1), ('CE', 2), ('ET', 1), ('UG', 1), ('OR', 1), ('SE', 1), ('A', 1), ('E', 3), ('G', 2), ('K', 1), ('O', 1), ('L', 1), ('R', 1), ('T', 1)))  # This line was injected by injectors.py
wholeEnoughs = {'A': 'DATA', 'NOTICE': 'NOTICE', 'RNING': 'WARNING', 'ACE': 'TRACE', 'ATA': 'DATA', 'ACK': 'HACK', 'WWISE': 'WWISE', 'HACK': 'HACK', 'EBUG': 'DEBUG', 'TICE': 'NOTICE', 'CAL': 'CRITICAL', 'OTICE': 'NOTICE', 'ASSET': 'ASSET', 'RACE': 'TRACE', 'ISE': 'WWISE', 'FO': 'INFO', 'SET': 'ASSET', 'DATA': 'DATA', 'ITICAL': 'CRITICAL', 'NG': 'WARNING', 'WARNING': 'WARNING', 'NING': 'WARNING', 'ROR': 'ERROR', 'BUG': 'DEBUG', 'TA': 'DATA', 'CK': 'HACK', 'CRITICAL': 'CRITICAL', 'TICAL': 'CRITICAL', 'NFO': 'INFO', 'K': 'HACK', 'AL': 'CRITICAL', 'O': 'INFO', 'L': 'CRITICAL', 'R': 'ERROR', 'ICE': 'NOTICE', 'ERROR': 'ERROR', 'DEBUG': 'DEBUG', 'ET': 'ASSET', 'ARNING': 'WARNING', 'INFO': 'INFO', 'SSET': 'ASSET', 'WISE': 'WWISE', 'TRACE': 'TRACE', 'T': 'ASSET', 'RITICAL': 'CRITICAL', 'ICAL': 'CRITICAL', 'UG': 'DEBUG', 'ING': 'WARNING', 'OR': 'ERROR', 'SE': 'WWISE', 'RROR': 'ERROR'}  # This line was injected by injectors.py

callableNames = {'isStampCutoff', 'OrderedDict', 'makeDirPaths', 'chain', 'basename', 'datetime', 'partial', 'saveRawLogsToJson', 'getZippedPath', 'joinEventGroups', 'saveTraceLog', 'makeCallChain', 'izip', 'getVariDirPath', 'writeGzip', 'trimTime', 'read', 'isdir', 'iterMroUntilDefClsFound', 'parseStdLog', 'prettyfyLines', 'exists', 'splitIntsFromStrs', 'getPrintDirPath', 'prettyfyLine', 'replaceRedundantWithSpacesInPlace', 'dirname', 'isfile', 'getTracePath', 'tupleOfStrsToStr', 'makedirs', 'getStdLogPath', 'extendStak', 'removePrintDir', 'saveStakLog', 'interpolMissingStamps', 'getCompStakPath', 'firstFrameAndData', 'onTraceSilenced', 'Settings', 'clearLogs', 'prettyCompressLines', 'entriesWithLinksJoin', 'parseLines', 'getPrimiStdPath', 'compactTraceLog', '_getframe', 'delTrace', 'TraceState', 'splitext', 'walk', 'unixStampToStr', 'makeFilePathUnique', 'makeSplitLink', 'labelLogs', 'appendToStak', 'getStdStakSplicePath', 'writeJson', 'setTrace', 'compileRegexExpression', 'makeOpenCalls', 'serializeArgs', 'getCompStdStakSplicePath', 'omropocs', 'joinLink', 'getJsonPath', 'join', 'interpolLines', 'trimFlagIfPoss', 'appendToTrace', 'makeMinMaxDiff', 'FunctionType', 'tryCall', 'joinLinks', 'splitStampFromTheRest', 'addSuffix', 'compressCallChains', 'write', 'diffAndRedundant', 'EventCounter', 'omrolocs', 'E', 'trace', 'getCompactTracePath', 'trimFlag', 'compress', 'rmtree', 'getJsonDirPath', 'dateEntries', 'CFL', 'saveAll', 'firstFrameAndDataAndLocals', 'getPrimiDirPath', 'unixStampToTupleOfStrs', 'makeMinMaxOpen', 'time', 'omrolocsalad', 'getPrimiStakPath', 'walkDirForSuffix'}  # This line was injected by injectors.py

defaultSegFlag = 'main'

logFilesExt    = '.log'
jsonFilesExt   = '.json'
zippedFilesExt = '.json.gz'

blockPrefix = 'block'

backupsPath = r'C:\STAK_backups'
