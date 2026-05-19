""" Constants: Static hardcoded data. """

from .block00_autoImports import *

## Manual input constants
# ---------------------------------------------------------------------------------------------------------------------

# Changes to these will rename/add/delete modules & all references to them.
blockNames = (
    'autoImports',
    'settings',
    'constants',
    'state',
    'log',
    'utils',
    'stampOps',
    'pathOps',
    'callChains',
    'joinLinks',
    'dataLinks',
    'tracing',
    'interceptor',
    'compression',
    'saveOps',
    'injectors',
    'meta',
    'perf',
    'wrapC',
    'compile',
    'events',
)

staticBlockNames = ('state', 'wrapC')

validOSs = {'linux', }
validPys = {'27', }

blockPrefix = 'block'
lenBlockPrefix = len(blockPrefix)

pyExt     = '.py'
pycExt    = '.pyc'
logExt    = '.log'
pickleExt = '.pkl'

lenPyExt  = len(pyExt)
nLenPyExt = -lenPyExt
lenPycExt = len(pycExt)

exclFromLocals = {'self', 'cls'}

stakFlags  = ('OMROLOCS', 'LOCSALAD', 'DATE', 'DAFF', 'LABEL')
traceFlags = ('SET', 'CAL', 'RET', 'DEL')

silenceTimers = 0

# ---------------------------------------------------------------------------------------------------------------------

## Constants injected by injectors.py
# ---------------------------------------------------------------------------------------------------------------------
pStakFlags = [': OMROLOCS: ', ': LOCSALAD: ', ': DATE    : ', ': DAFF    : ', ': LABEL   : ']  # Injected
pTraceFlags = [': SET: ', ': CAL: ', ': RET: ', ': DEL: ']  # Injected
# ---------------------------------------------------------------------------------------------------------------------

# Level would have been the depth of nesting had this been nested.
# Using binary flags was tried, but binary operations in python are too slow,
# so, packing the information implicitly in incrementing integers is faster,
# This may cause the number of flags to increase exponentially & be less flexible,
# but so far its fiiineee.

(
# Level 1 Entry Flags
labelEntryFlag,
callChainEntryFlag,
dataChainEntryFlag,
dataEntryFlag,

# Level 2 Entry Flags
mroLinkEntryFlag,
fileLinkEntryFlag,

) = range(6)

callChainLinkFlags = {
    mroLinkEntryFlag,
    fileLinkEntryFlag,
}

# These are the fixed lens, the entries themselves can be dynamically longer based on the count entries.
baseEntryLens = {
    # dateEntryFlag   : 3,  # [..., flag, absStamp, clockStamp, ...]
    labelEntryFlag    : 2,  # [..., flag, stamp, labelStr, ...]
    callChainEntryFlag: 3,  # [..., flag, stamp, linkCnt, ...]
    dataChainEntryFlag: 4,  # [..., flag, stamp, dataCnt, linkCnt, ...]
    dataEntryFlag     : 3,  # [..., flag, stamp, dataCnt, ...]

    mroLinkEntryFlag  : 5,  # [..., flag, path, lineno, calName, clsCnt, ...]
    fileLinkEntryFlag : 4,  # [..., flag, path, lineno, calName, ...]
}

cntIdxsByEntryFlag = {
    mroLinkEntryFlag: (4, ),
    fileLinkEntryFlag: (),
}

# Stak Log example
# A thing to consider is that no data entry is possible without a call chain, now,
# sometimes the entire chain is not desired, in this case we still have a chain but
# with one link only. This means that data can be linked to entries implicitly by order.
# However, they share time stamp, the data and its chain I mean, so how to solve this problem?


# stakLog = [
#     entryID = 0,
#     entryID = 1,
#     entryID = 2,
#     entryID = 0,
# ]

# clockStamps = [  # Linked by Idx to stakLog
#     clockStamp = 2514.0686976,
#     clockStamp = 2515.8576039,
#     clockStamp = 2516.3113509,
#     clockStamp = 2516.7229875,
# ]

# stakLogEntriesById = [  # Where Idx is ID
#     (labelEntryFlag, '============== SOME LABEL ================'),
#     (callChainEntryFlag, callChainID=0),
#     (dataChainEntryFlag, dataID=0, callChainID=0),
# ]

# idsByStakLogEntries = {
#     (labelEntryFlag, '============== SOME LABEL ================'): 0,
#     (callChainEntryFlag, callChainID=0): 1,
#     (dataChainEntryFlag, dataID=0, callChainID=0): 2,
# }

# dataById = [
#     ('key1', 'val1', 'key2', 'val2'),
# ]

# callChainsById = [
#     (linkID=0, linkID=1),
# ]

# idsByCallChain = {
#     (linkID=0, linkID=1): 0,
# }

# splitLinksById = [  # Where Idx is ID
#     (mroLinkEntryFlag, '\path', 123, 'calName', 0),  # ID = 0
#     (fileLinkEntryFlag, '\path', 234, 'calName'),  # ID = 1
# ]

# idsBySplitLink = {
#     (mroLinkEntryFlag, '\path', 123, 'calName', 0): 0,
#     (fileLinkEntryFlag, '\path', 234, 'calName'): 1,
# }

# mrosById = [
#     ('Cls1', 'Cls2', 'Cls3'),
# ]

# idsByMro = {
#     ('Cls1', 'Cls2', 'Cls3'): 0,
# }
