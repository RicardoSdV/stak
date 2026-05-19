""" Settings i.e. can change without restarting interpreter.
Modify this file & reload with so.reload() or aliases. """

## Labels
eventLabels = ['PRE DELUXE TOOLTIP', 'POST DELUXE TOOLTIP', 'PRE TOOLTIP', 'POST TOOLTIP']

## Dir paths: Change often
taskDir  = 'deluxeDevices'
printDir = 'print3_padding'

silenceTrace = 0

# Exclude paths that contain any part of the paths in here.
silentFiles = []

# If any, only allow paths that contain any part of paths here.
loudFiles = []

repeatSilence = 0

# TODO: Ideally pickles would all be in some backup file, and the
#  path could be built dynamically based on the task name & print.
loadAndResavePath = r'.STAK\task\print\pickle\pickle.pkl'

## File prefixes
stdLogPrefixes = ('python',)
stakLogPrefix  = 'stak'
traceLogPrefix = 'trace'
picklePrefix   = 'pickle'
zippedPrefix   = 'zipped'

## Increases compress times exponentially
# reduce if saving takes too long.
maxCompressGroupSize = 80

## Omro(l/p)ocs formatting
tryLogMro          = 1
alwaysLogFilePath  = 0
alwaysLogLineno    = 1
includeData        = 1
logCallsFromLineno = 1  # trace only

# Depths, if falsy no limit
defaultPathDepth = 1
maxMroClsNsDepth = 0

## Save which stak?
saveStdPrimi          = 1
saveStdStakSplice     = 1
saveStdStakSpliceComp = 1
saveStakPrimi         = 1
saveStakComp          = 1
saveStakPickle        = 0

## Save which trace?
saveTrace             = 1
saveTraceCompact      = 0
saveTracePickle       = 0

overrideSettingsOnLAR = 0

## Dir paths: semi-static
rootDir    = '.STAK'
primiDir   = 'primitives'
variDir    = 'variants'
stdDir     = ''
pickleDir  = 'pickle'

## File suffixes
primiSuffix             = ''
compSuffix              = 'Compress'
stdStakSpliceSuffix     = 'Splice'
compStdStakSpliceSuffix = ''
compactSuffix           = 'Compact'
