# Level would have been the depth of nesting had this been nested.
# Using binary flags was tried, but binary operations in python are too slow,
# so, packing the information implicitly in incrementing integers is faster,
# This may cause the number of flags to increase exponentially & be less flexible,
# but so far its fiiineee.

# Level 1 Spec Flags
stampAndChainEntry = 1

# Level 2 Spec Flags
splitLinkChainEntry = 2

# Level 3 Spec Flags
fileLinkEntry      = 3
fileDataLinkEntry  = 4
fileDataCalLnEntry = 5

mroLinkEntry          = 6
mroDataLinkEntry      = 7
mroDataCalLnLinkEntry = 8









# Entry spec bin flags (32-bit signed)
specCnt  = 1    # 000 0000 0000 0000 0000 0000 0000 0001
stamp    = 2    # 000 0000 0000 0000 0000 0000 0000 0010
chain    = 4    # 000 0000 0000 0000 0000 0000 0000 0100
link     = 8    # 000 0000 0000 0000 0000 0000 0000 1000
path     = 16   # 000 0000 0000 0000 0000 0000 0001 0000
lineno   = 32   # 000 0000 0000 0000 0000 0000 0010 0000
mroClsNs = 64   # 000 0000 0000 0000 0000 0000 0100 0000
calName  = 128  # 000 0000 0000 0000 0000 0000 1000 0000
logData  = 256  # 000 0000 0000 0000 0000 0001 0000 0000
keySpec  = 512  # 000 0000 0000 0000 0000 0010 0000 0000
valSpec  = 1024 # 000 0000 0000 0000 0000 0100 0000 0000
strSpec  = 2048 # 000 0000 0000 0000 0000 1000 0000 0000


# splitLink = path, frame.f_lineno, calName, mroClsNs, dataForLogging

# log = [i(stamp | chain), stamp, i(cnt | link), 3, i(path | lineno | calName | mroClsNs | logData), '\path', 123, i(strSpec | cnt), 3, 'Cls1', 'Cls2' 'meth', i(cnt| keySpec | valSpec), 'a', 1, 'b', 2, i(), i(),]



# ## Entry Flags & their spec flags

## Entry ID masks
# elCountMask   = 63          # 000 0000 0000 0000 0000 0000 0011 1111
# entryFlagMask = 4032        # 000 0000 0000 0000 0000 1111 1100 0000
# specFlagMask  = 2147479552  # 111 1111 1111 1111 1111 0000 0000 0000

# stakEntry = 1
# stamp  = 1
# chain  = 2
#
# chainEntry = 2
# link = 1
#
# linkEntry  = 3
# path    = 1
# lineno  = 2
# mro     = 4
# calName = 8
# linkKVP = 16
# linkStr = 32
#
# KVEntry    = 4  # Key value entry
# key = 1
# val = 2
#
#
# ## Stak Entry Spec Flags
#
#
#
# # logEx = [stamp, string, chain, stamp, chain, stamp, chain, stamp, string, ]
#
#
# # log = [i(stamp | string | chain, stakEntry, 3), stamp, string, i(splitLink, chainEntry, 2), i(linkEntry), i()]




# ## EntryFlags
# stakEntry = 1
# traceEntry = 2
# interceptEntry = 3
#
# ## EntryContentsFlag
# strContent = 4
# callChainContent = 5
#
# ## Chain link flags
# fileLink = 6
# mroLink  = 7
#
#
# # log = [i(stakEntry, 2), stamp, i(strContent, 1), str, i(callChainContent, 3), i(fileLink, )]


