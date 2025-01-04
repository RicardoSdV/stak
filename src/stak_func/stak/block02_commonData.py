"""
Data, manually inputted or injected by ..injectors.py
"""
from collections import OrderedDict

stakFlags = ('OMROLOCS', 'DATE', 'DATA', 'LABEL', 'SETTRACE', 'CALTRACE', 'RETTRACE', 'DELTRACE')
pStakFlags = (': OMROLOCS: ', ': DATE    : ', ': DATA    : ', ': LABEL   : ', ': SETTRACE: ', ': CALTRACE: ', ': RETTRACE: ', ': DELTRACE: ')  # This line was injected by injectors.py

omrolocsFlag , dateFlag , dataFlag , labelFlag , setFlag , callFlag , retFlag , delFlag  = stakFlags
pOmrolocsFlag, pDateFlag, pDataFlag, pLabelFlag, pSetFlag, pCallFlag, pRetFlag, pDelFlag = pStakFlags

hasLinksFlags = {omrolocsFlag, setFlag, callFlag, retFlag, delFlag}

traceFlags = {setFlag, callFlag, retFlag, delFlag}

callFlags = {setFlag, callFlag}
retFlags  = {retFlag, delFlag}

stdFlags = ('DEBUG', 'INFO', 'NOTICE', 'WARNING', 'ERROR', 'CRITICAL', 'HACK', 'TRACE', 'ASSET')
paddedStdFlags = (': DEBUG   : ', ': INFO    : ', ': NOTICE  : ', ': WARNING : ', ': ERROR   : ', ': CRITICAL: ', ': HACK    : ', ': TRACE   : ', ': ASSET   : ')  # This line was injected by injectors.py

pStdFlagsByStdFlags = {'INFO': ': INFO    : ', 'CRITICAL': ': CRITICAL: ', 'NOTICE': ': NOTICE  : ', 'TRACE': ': TRACE   : ', 'HACK': ': HACK    : ', 'WARNING': ': WARNING : ', 'ASSET': ': ASSET   : ', 'ERROR': ': ERROR   : ', 'DEBUG': ': DEBUG   : '}  # This line was injected by injectors.py
allPflagsByFlags = {'INFO': ': INFO    : ', 'CRITICAL': ': CRITICAL: ', 'DELTRACE': ': DELTRACE: ', 'RETTRACE': ': RETTRACE: ', 'TRACE': ': TRACE   : ', 'CUTOFF': ': CUTOFF  : ', 'OMROLOCS': ': OMROLOCS: ', 'SETTRACE': ': SETTRACE: ', 'HACK': ': HACK    : ', 'NOTICE': ': NOTICE  : ', 'ERROR': ': ERROR   : ', 'LABEL': ': LABEL   : ', 'DEBUG': ': DEBUG   : ', 'WARNING': ': WARNING : ', 'ASSET': ': ASSET   : ', 'CALTRACE': ': CALTRACE: ', 'DATE': ': DATE    : ', 'DATA': ': DATA    : '}  # This line was injected by injectors.py

pStdFlagsByStdFlags['CUTOFF'] = ': CUTOFF  : '  # Manually padding ain't great
cutoffFlag = 'CUTOFF'

cutoffCombos = OrderedDict((('CRITICAL', 1), ('WARNING', 1), ('RITICAL', 1), ('NOTICE', 1), ('ITICAL', 1), ('ARNING', 1), ('RNING', 1), ('OTICE', 1), ('ASSET', 1), ('TICAL', 1), ('ERROR', 1), ('DEBUG', 1), ('TRACE', 1), ('HACK', 1), ('TICE', 1), ('RACE', 1), ('NING', 1), ('RROR', 1), ('INFO', 1), ('SSET', 1), ('ICAL', 1), ('EBUG', 1), ('ACE', 1), ('ACK', 1), ('CAL', 1), ('SET', 1), ('ICE', 1), ('ROR', 1), ('BUG', 1), ('NFO', 1), ('ING', 1), ('FO', 1), ('NG', 1), ('CK', 1), ('AL', 1), ('CE', 2), ('ET', 1), ('UG', 1), ('OR', 1), ('E', 2), ('G', 2), ('K', 1), ('O', 1), ('L', 1), ('R', 1), ('T', 1)))  # This line was injected by injectors.py
wholeEnoughs = {'NOTICE': 'NOTICE', 'RNING': 'WARNING', 'ACE': 'TRACE', 'ACK': 'HACK', 'HACK': 'HACK', 'EBUG': 'DEBUG', 'TICE': 'NOTICE', 'CAL': 'CRITICAL', 'OTICE': 'NOTICE', 'ASSET': 'ASSET', 'RACE': 'TRACE', 'FO': 'INFO', 'SET': 'ASSET', 'ITICAL': 'CRITICAL', 'NG': 'WARNING', 'WARNING': 'WARNING', 'NING': 'WARNING', 'ROR': 'ERROR', 'BUG': 'DEBUG', 'CK': 'HACK', 'CRITICAL': 'CRITICAL', 'TICAL': 'CRITICAL', 'NFO': 'INFO', 'K': 'HACK', 'AL': 'CRITICAL', 'O': 'INFO', 'L': 'CRITICAL', 'R': 'ERROR', 'ICE': 'NOTICE', 'ERROR': 'ERROR', 'DEBUG': 'DEBUG', 'ET': 'ASSET', 'ARNING': 'WARNING', 'INFO': 'INFO', 'SSET': 'ASSET', 'TRACE': 'TRACE', 'T': 'ASSET', 'RITICAL': 'CRITICAL', 'ICAL': 'CRITICAL', 'UG': 'DEBUG', 'ING': 'WARNING', 'OR': 'ERROR', 'RROR': 'ERROR'}  # This line was injected by injectors.py

callableNames = {'isStampCutoff', 'partial', 'makeDirPaths', 'formatCompStak', 'basename', 'saveTrace', 'saveStdStakSplice', 'datetime', 'savePrimiStd', 'pubClsMethCond', 'OrderedDict', 'fmtOmrolocsEntry', 'privClsMethCond', 'dateEntry', 'appendToLog', 'preProcessLog', 'makeCallChain', 'isdir', 'getVariDirPath', 'trimTime', 'joinStrLinkWithDataForLogging', 'matcher', 'stdStakSplice', 'handleLine', 'formatPrimiStak', 'autoLocals', 'makeStrLinkCallChains', 'retArgs', 'prettyfyLines', 'exists', 'unixStampToDatetime', 'getPrintDirPath', 'prettyfyLine', 'dirname', 'isfile', 'splitLinkFromFrame', 'tupleOfStrsToStr', 'savePrimiStak', 'splitLinksCallChain', 'makedirs', 'clearLog', 'compressLines', 'removePrintDir', 'interpolMissingStamps', 'formatCompStdStakSplice', 'labelLog', 'fmtCallEntry', 'trimFilePathAddLineno', 'extendLog', 'dataAndFirstFrame', 'handleCall', 'handleReturn', 'CompressionFormatList', 'formatTrace', 'parseLines', 'privInsMethCond', 'mroClsNsGen', 'mroLinkToStrLink', '_getframe', 'fmtRetEntry', 'delTrace', 'setTrace', 'Log', 'splitext', 'getStdLogPaths', 'linkFromFrame', 'unixStampToStr', 'joinFileLink', 'jointLinkFromFrame', 'makeFilePathUnique', 'formatPrimiStd', 'saveCompStdStakSplice', 'saveCompStak', 'reloadSettings', 'reloadData', 'compressLinks', 'spliceStakLogWithStdLog', 'settrace', 'omropocs', 'fmtDataEntry', 'handleException', 'join', 'splitStampFromTheRest', 'trimFlagIfPoss', 'joinMroLink', 'OldStyleClsType', 'splitTrace', 'FunctionType', 'compileRegexExpression', 'formatStdStakSplice', 'fmtLabelEntry', 'parseStdLogs', 'parseAndInterpolLines', 'addSuffix', 'writeLogsToFile', 'pubInsMethCond', 'omrolocs', 'trace', 'trimFlag', 'compress', 'rmtree', 'saveAll', 'fmtDateEntry', 'getPrimiDirPath', 'unixStampToTupleOfStrs', 'time', 'omrolocsalad'}  # This line was injected by injectors.py


def reloadData():
    from sys import modules
    reload(modules[__name__])
