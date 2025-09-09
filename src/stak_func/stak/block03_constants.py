""" Constants, i.e. they don't change during an interpreter run. Not technically true, since now constants can change,
when stak is first imported, but they remain static otherwise. Manually inputted or injected by block15_injectors. """
import sys

runInjectors = 0
## Manual input constants
# ---------------------------------------------------------------------------------------------------------------------
silenceTimers = 0

# Changes to these will rename modules & all references to them.
blockNames = (
    'typing',
    'settings',
    'settingObj',
    'constants',
    'log',
    'pathOps',
    'stampOps',
    'callChains',
    'joinLinks',
    'dataLinks',
    # 'newBlock',
    'tracing',
    'compression',
    'parseStdLogs',
    'saveOps',
    'debugComponent',
    'utils',
)

blockPrefix = 'block'

stakFlags  = ('OMROLOCS', 'LOCSALAD', 'DATE', 'DAFF', 'LABEL')
traceFlags = ('SET', 'CAL', 'RET', 'DEL')
stdFlags   = ('DEBUG', 'INFO', 'NOTICE', 'WARNING', 'ERROR', 'CRITICAL', 'HACK', 'TRACE', 'ASSET', 'WWISE', 'DATA')

pyExt     = '.py'
pycExt    = '.pyc'
logExt    = '.log'
pickleExt = '.pkl'

# ---------------------------------------------------------------------------------------------------------------------

## Computed constants
# ---------------------------------------------------------------------------------------------------------------------
lenPyExt       = len(pyExt)
lenPycExt      = len(pycExt)
lenBlockPrefix = len(blockPrefix)

# os does not hold the correct path char for certain programs, when inspecting frames,
# for saving should os.path.join, but for frame ops use pathSplitChar.
pathSplitChar = '/' if '/' in sys._getframe(0).f_code.co_filename else '\\'
# ---------------------------------------------------------------------------------------------------------------------

## Constants injected by injectors.py
# ---------------------------------------------------------------------------------------------------------------------
pStakFlags = [': OMROLOCS: ', ': LOCSALAD: ', ': DATE    : ', ': DAFF    : ', ': LABEL   : ']
pTraceFlags = [': SET: ', ': CAL: ', ': RET: ', ': DEL: ']

paddedStdFlags = [': DEBUG   : ', ': INFO    : ', ': NOTICE  : ', ': WARNING : ', ': ERROR   : ', ': CRITICAL: ', ': HACK    : ', ': TRACE   : ', ': ASSET   : ', ': WWISE   : ', ': DATA    : ']

pStdFlagsByStdFlags = {'INFO': ': INFO    : ', 'CRITICAL': ': CRITICAL: ', 'NOTICE': ': NOTICE  : ', 'TRACE': ': TRACE   : ', 'WWISE': ': WWISE   : ', 'HACK': ': HACK    : ', 'WARNING': ': WARNING : ', 'ASSET': ': ASSET   : ', 'ERROR': ': ERROR   : ', 'DEBUG': ': DEBUG   : ', 'DATA': ': DATA    : '}

allPflagsByFlags = {'INFO': ': INFO    : ', 'DAFF': ': DAFF    : ', 'NOTICE': ': NOTICE  : ', 'LOCSALAD': ': LOCSALAD: ', 'TRACE': ': TRACE   : ', 'CUTOFF': ': CUTOFF  : ', 'DATA': ': DATA    : ', 'WWISE': ': WWISE   : ', 'HACK': ': HACK    : ', 'CRITICAL': ': CRITICAL: ', 'LABEL': ': LABEL   : ', 'DEBUG': ': DEBUG   : ', 'WARNING': ': WARNING : ', 'ASSET': ': ASSET   : ', 'ERROR': ': ERROR   : ', 'DATE': ': DATE    : ', 'OMROLOCS': ': OMROLOCS: '}

pStdFlagsByStdFlags['CUTOFF'] = ': CUTOFF  : '  # Manually padding ain't great

cutoffFlag = 'CUTOFF'

wholeEnoughs = [('RITICAL', 7, 'CRITICAL'), ('ITICAL', 6, 'CRITICAL'), ('ARNING', 6, 'WARNING'), ('RNING', 5, 'WARNING'), ('OTICE', 5, 'NOTICE'), ('TICAL', 5, 'CRITICAL'), ('EBUG', 4, 'DEBUG'), ('TICE', 4, 'NOTICE'), ('RACE', 4, 'TRACE'), ('NING', 4, 'WARNING'), ('SSET', 4, 'ASSET'), ('WISE', 4, 'WWISE'), ('ICAL', 4, 'CRITICAL'), ('RROR', 4, 'ERROR'), ('ACE', 3, 'TRACE'), ('ATA', 3, 'DATA'), ('ACK', 3, 'HACK'), ('CAL', 3, 'CRITICAL'), ('ISE', 3, 'WWISE'), ('SET', 3, 'ASSET'), ('ICE', 3, 'NOTICE'), ('ROR', 3, 'ERROR'), ('BUG', 3, 'DEBUG'), ('NFO', 3, 'INFO'), ('ING', 3, 'WARNING'), ('FO', 2, 'INFO'), ('NG', 2, 'WARNING'), ('TA', 2, 'DATA'), ('CK', 2, 'HACK'), ('AL', 2, 'CRITICAL'), ('ET', 2, 'ASSET'), ('UG', 2, 'DEBUG'), ('OR', 2, 'ERROR'), ('SE', 2, 'WWISE'), ('A', 1, 'DATA'), ('K', 1, 'HACK'), ('O', 1, 'INFO'), ('L', 1, 'CRITICAL'), ('R', 1, 'ERROR'), ('T', 1, 'ASSET')]
backupsPath = r'C:\STAK_backups'

osPath = ''
ignorePaths = ''
packagePath = ''

# ---------------------------------------------------------------------------------------------------------------------
