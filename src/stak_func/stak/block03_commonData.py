"""
Data, manually inputted or injected by ..injectors.py
"""
from collections import OrderedDict


stakFlags = ('OMROLOCS', 'DATE', 'DAFF', 'LABEL')
pStakFlags = (': OMROLOCS: ', ': DATE    : ', ': DAFF    : ', ': LABEL   : ')  # This line was injected by injectors.py

omrolocsFlag , dateFlag , daffFlag , labelFlag  = stakFlags
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

callableNames = {'isStampCutoff', 'partial', 'makeDirPaths', 'formatCompStak', 'izip', 'saveTrace', 'saveStdStakSplice', 'datetime', 'savePrimiStd', 'pubClsMethCond', 'replaceRedundantWithSpacesInPlace', 'fmtOmrolocsEntry', 'privClsMethCond', 'dateEntry', 'readBlockNames', 'appendToLog', 'formatTrace', 'joinEventGroups', 'makeCallChain', 'save', 'basename', 'fmtLabelEntry', 'trimTime', 'joinStrLinkWithDataForLogging', 'stdStakSplice', 'handleLine', 'formatPrimiStak', 'setReloadedNames', 'autoLocals', 'isdir', 'retArgs', 'l', 'readImports', 'prettyfyLines', 'rmp', 'appendToTrace', 'clearLog', 'exists', 'splitIntsFromStrs', 'fmtDelEntry', 'unixStampToDatetime', 'prettyfyLine', 'dirname', 'isfile', 'splitLinkFromFrame', 'removeStakCallables', 'rp', 'tupleOfStrsToStr', 'savePrimiStak', 'splitLinksCallChain', 'makedirs', 'fmtCallEntry', 'reloadBlocks', 'label', 'compressLines', 'removePrintDir', 'ra', 'fmtSetEntry', 'interpolMissingStamps', 'padFlags', 'defaultdict', 'formatCompStdStakSplice', 'labelLog', 'getPackageName', 'extendLog', 'dataAndFirstFrame', 'handleCall', 'CompressionFormatList', 'fmtDataEntry', 'parseLines', 'privInsMethCond', 'getAliasesFromInterface', 'mroLinkToStrLink', 'OrderedDict', 's', 'rmPrint', '_getframe', 'fmtRetEntry', 'getPrintDirPath', 'delTrace', 'saveCompStak', 'Log', 'splitext', 'getStdLogPaths', 'padSegFlags', 'linkFromFrame', 'unixStampToStr', 'joinFileLink', 'jointLinkFromFrame', 'makeFilePathUnique', 'formatPrimiStd', 'saveCompStdStakSplice', 'setTrace', 'joinSplitLink', 'handleRet', 'makeOpenCalls', 'handleExc', 'preProcessStakLog', 'getBlocks', 'setAliasesInInterface', 'spliceStakLogWithStdLog', 'settrace', 'c', 'omropocs', 'entriesWithLinksJoin', 'trimFilePathsAddLineNums', 'daff', 'join', 'splitStampFromTheRest', 'trimFlagIfPoss', 'joinMroLink', 'makeMinMaxDiff', 'OldStyleClsType', 'linksJoin', 'FunctionType', 'mroClsNsGen', 'compileRegexExpression', 'formatStdStakSplice', 'getVariDirPath', 'parseStdLogs', 'parseAndInterpolLines', 'addSuffix', 'compressCallChains', 'reloadAll', 'readReloadableBlockNames', 'formatTraceLog', 'read', 'split', 'writeLogsToFile', 'diffAndRedundant', 'pubInsMethCond', 'omrolocs', 'joinTraceLinks', 'trace', 'trimFlag', 'compress', 'rmtree', 'formatCompactTrace', 'saveCompactTrace', 'saveAll', 'clear', 'jamInterfaceIntoBuiltins', 'fmtDateEntry', 'getPrimiDirPath', 'unixStampToTupleOfStrs', 'makeMinMaxOpen', 'time', 'omrolocsalad'}  # This line was injected by injectors.py

defaultSegFlag = 'main'
