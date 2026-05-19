"""
Constants, i.e. they don't change during an interpreter run. Manually inputted or injected by ..injectors.py
"""

silenceTimers = 0

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

wholeEnoughs = (('RITICAL', 7, 'CRITICAL'), ('ITICAL', 6, 'CRITICAL'), ('ARNING', 6, 'WARNING'), ('RNING', 5, 'WARNING'), ('OTICE', 5, 'NOTICE'), ('TICAL', 5, 'CRITICAL'), ('EBUG', 4, 'DEBUG'), ('TICE', 4, 'NOTICE'), ('RACE', 4, 'TRACE'), ('NING', 4, 'WARNING'), ('SSET', 4, 'ASSET'), ('WISE', 4, 'WWISE'), ('ICAL', 4, 'CRITICAL'), ('RROR', 4, 'ERROR'), ('ACE', 3, 'TRACE'), ('ATA', 3, 'DATA'), ('ACK', 3, 'HACK'), ('CAL', 3, 'CRITICAL'), ('ISE', 3, 'WWISE'), ('SET', 3, 'ASSET'), ('ICE', 3, 'NOTICE'), ('ROR', 3, 'ERROR'), ('BUG', 3, 'DEBUG'), ('NFO', 3, 'INFO'), ('ING', 3, 'WARNING'), ('FO', 2, 'INFO'), ('NG', 2, 'WARNING'), ('TA', 2, 'DATA'), ('CK', 2, 'HACK'), ('AL', 2, 'CRITICAL'), ('ET', 2, 'ASSET'), ('UG', 2, 'DEBUG'), ('OR', 2, 'ERROR'), ('SE', 2, 'WWISE'), ('A', 1, 'DATA'), ('K', 1, 'HACK'), ('O', 1, 'INFO'), ('L', 1, 'CRITICAL'), ('R', 1, 'ERROR'), ('T', 1, 'ASSET'))  # This line was injected by injectors.py

callableNames = {'getFrame', 'partial', 'makeDirPaths', 'chain', 'basename', 'datetime', 'isStampCutoff', 'wraps', 'gettrace', '_omrolocsalaraa', 'funcErr', 'saveTraceLog', 'makeCallChain', 'izip', 'spliceStakAndStdLog', 'getVariDirPath', 'trimTime', 'read', 'readAndParseStdLog', 'saveStdLogToPrimitives', 'floatToStr4', 'isdir', '_omrolocsoladoed', 'iterMroUntilDefClsFound', 'prettyfyLines', 'savePrimitiveStak', 'exists', 'getPrintDirPath', 'prettyfyLine', 'dirname', 'getTracePath', 'clock', 'makedirs', 'getStdLogPath', 'picklePrimitiveLogs', 'removePrintDir', 'saveStakLog', 'interpolMissingStamps', 'getCompStakPath', 'firstFrameAndData', 'onTraceSilenced', 'Settings', 'getBaseIgnoredPaths', 'omrolocsar', 'clearLogs', 'prettyCompressLines', 'parseLines', 'readPickle', 'compressAndSaveStak', 'str4ToStr', 'getPrimiStdPath', '_getframe', 'argsToStr', 'delTrace', 'omropocsar', 'TraceState', 'timeCall', 'splitext', 'walk', 'unixStampToStr', 'makeSplitLink', 'labelLogs', 'appendToStak', 'getStdStakSplicePath', 'log', 'makeSplitLinkTrace', 'setTrace', 'compileRegexExpression', 'deque', 'omropocsalad', 'serializeArgs', 'loadAndResave', 'settrace', 'getCompStdStakSplicePath', 'omropocs', 'omropocsalar', 'joinLink', 'copy', 'join', 'appendToTrace', 'compressAndSaveCompressedSplice', 'extendStak', 'joinSplitLinksAndLeaveOutSilencedFiles', 'FunctionType', 'Cnt', 'tryCall', 'joinLinks', 'interpolLines', 'addSuffix', 'compressCallChains', 'write', 'omrolocs', 'getPicklePath', 'saveUncompressedSplice', 'E', 'trace', 'getCompactTracePath', 'trimFlag', 'compress', 'rmtree', 'getIdFromPath', 'dateEntries', 'makePathUnique', 'CFL', 'saveAll', 'firstFrameAndDataAndLocals', 'makePrintDirPath', 'omrolocsalar', 'DebugEvent', 'getPrimiDirPath', 'writePickle', 'walkDirForSuffix', 'time', 'omrolocsalad', 'getPrimiStakPath', 'getPickleDirPath'}  # This line was injected by injectors.py

defaultSegFlag = 'main'

logFilesExt    = '.log'
pickleFilesExt = '.pkl'

blockPrefix = 'block'

backupsPath = r'C:\STAK_backups'

callFromShellInterface = (
    's'  , 'saveAll',
    'l'  , 'labelLogs',
    'c'  , 'clearLogs',
    'rmp', 'removePrintDir',
    'rs' , 'reloadSettings',
    'lar', 'loadAndResave',
    'st' , 'setTrace',
    'dt' , 'delTrace',
    'pt',  'printTimings',
)

callFromCodeInterface = (
    'omropocs',
    'omrorocs',
    'omrolocs',
    'omrolocsalad',
    'omropocsalad',
    'omrolocsalar',
    'ffad',
    'ffadal',
    'setTrace',
    'delTrace',
)

exclFromLocals = set(('self', 'cls') + callFromCodeInterface)
