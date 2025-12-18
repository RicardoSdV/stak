""" Constants: Static hardcoded data. """

from .block00_autoImports import *

## Manual input constants
# ---------------------------------------------------------------------------------------------------------------------
ignorePaths = set()   # TODO: Theres references to this around, but I have no idea why theres no definition

silenceTimers = 0

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
    'debugComponent',
    'injectors',
    'meta',
    'perf',
    'computed',
)

blockPrefix = 'block'

stakFlags  = ('OMROLOCS', 'LOCSALAD', 'DATE', 'DAFF', 'LABEL')
traceFlags = ('SET', 'CAL', 'RET', 'DEL')


pyExt     = '.py'
pycExt    = '.pyc'
logExt    = '.log'
pickleExt = '.pkl'

exclFromLocals = {'self', 'cls'}

backupsPath = r'C:\STAK_backups'  # TODO: !

# ---------------------------------------------------------------------------------------------------------------------

## Constants injected by injectors.py
# ---------------------------------------------------------------------------------------------------------------------
pStakFlags = [': OMROLOCS: ', ': LOCSALAD: ', ': DATE    : ', ': DAFF    : ', ': LABEL   : ']  # Injected
pTraceFlags = [': SET: ', ': CAL: ', ': RET: ', ': DEL: ']  # Injected
# ---------------------------------------------------------------------------------------------------------------------

## Entry ID masks
elCountMask   = 63    # 000 0000 0000 0000 0000 0000 0011 1111
entryFlagMask = 4032  # 000 0000 0000 0000 0000 1111 1100 0000

# Entry spec bin flags (32-bit signed)
specCntBF    = 1     # 000 0000 0000 0000 0000 0000 0000 0001
strFlagBF    = 2     # 000 0000 0000 0000 0000 0000 0000 0010
stampBF      = 4     # 000 0000 0000 0000 0000 0000 0000 0100
chainBF      = 8     # 000 0000 0000 0000 0000 0000 0000 1000
linkBF       = 16    # 000 0000 0000 0000 0000 0000 0001 0000
pathBF       = 32    # 000 0000 0000 0000 0000 0000 0010 0000
linenoBF     = 64    # 000 0000 0000 0000 0000 0000 0100 0000
calNameBF    = 128   # 000 0000 0000 0000 0000 0000 1000 0000
mroClsNsBF   = 256   # 000 0000 0000 0000 0000 0001 0000 0000
logDataBF    = 512   # 000 0000 0000 0000 0000 0010 0000 0000
keySpecBF    = 1024  # 000 0000 0000 0000 0000 0100 0000 0000
valSpecBF    = 2048  # 000 0000 0000 0000 0000 1000 0000 0000
strSpecBF    = 4096  # 000 0000 0000 0000 0001 0000 0000 0000
callFromLnBF = 8192  # 000 0000 0000 0000 0010 0000 0000 0000

# Entry masks (identifiers for types of entries. They could contain more elements.)
splitLinkBFs = pathBF | linenoBF | calNameBF

# Level would have been the depth of nesting had this been nested.
# Using binary flags was tried, but binary operations in python are too slow,
# so, packing the information implicitly in incrementing integers is faster,
# This may cause the number of flags to increase exponentially & be less flexible,
# but so far its fiiineee.

(
# Level 1 Entry Flags
dateEntry,
labelEntry,
callChainEntry,
dataChainEntry,

# Level 2 Entry Flags
mroLinkEntry,
fileLinkEntry,

) = range(6)

baseEntryLens = {
    mroLinkEntry: 5,
    fileLinkEntry: 4,
}

cntIdxsByEntryFlag = {
    mroLinkEntry: (4, ),
    fileLinkEntry: (),
}

# Stak Log example
# stakLog = [
#     dateEntry, '2024-01-01',
#     labelEntry, '============== SOME LABEL ================',
#     callChainEntry,
#         stamp,
#         lnkCnt=2,
#         lnkHash1=hash('\path', 123),
#         lnkHash2=hash(hash('\path', 234)),
#
#     dataChainEntry,
#         stamp,
#         dataCnt=4,
#         'key1',
#         'val1',
#         'key2',
#         'val2',
#         lnkCnt=2,
#         lnkHash1=hash('\path', 123),
#         lnkHash2=hash(hash('\path', 234))
# ]
#
#
# splitLinks = [
#     mroLinkEntry, '\path', 123, 'calName', 3, 'Cls1', 'Cls2', 'Cls3',
#     fileLinkEntry, '\path', 234, 'calName',
# ]
#
#
# splitLinks_headIdxByPathLnHash = {
#     hash(('\path', 123)): 0,
#     hash(('\path', 234)): 8,
# }
#
# jointLinks = ['strLink1', 'strLink2', ..]
#
# jointLinks_idxByPathLnHash = {
#    hash(('\path', 123)): 0
#    hash(('\path', 234)): 1
# }
