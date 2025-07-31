""" Settings i.e. can change without restarting interpreter.
Modify this file & reload with so.reload() or aliases. """

## Labels
eventLabels = ['PRE EVENT 1', 'POST EVENT 1']

## Dir paths: Change often
taskDir  = 'task_stak'
printDir = 'print'

silenceTrace = 0

# Exclude paths that contain any part of the paths in here.
silentFiles = []

# If any, only allow paths that contain any part of paths here.
loudFiles = []

# TODO: Ideally pickles would all be in some backup file, and the
#  path could be built dynamically based on the task name & print.
loadAndResavePath = r'.STAK\task\print\pickle\pickle.pkl'

## File prefixes
stdLogPrefixes = ('stdLogA', 'stdLogB')
stakLogPrefix  = 'stak'
traceLogPrefix = 'trace'
picklePrefix   = 'pickle'
zippedPrefix   = 'zipped'

## Increases compress times exponentially
# reduce if saving takes too long.
maxCompressGroupSize = 80

## Omro(l/p)ocs formatting
tryLogMro          = 1
alwaysLogFilePath  = 1
alwaysLogLineno    = 1
includeData        = 1
logCallsFromLineno = 1  # trace only

# Depths, if falsy no limit
defaultPathDepth = 1
maxMroClsNsDepth = 1

## Save which stak?
saveStdPrimi          = 1
saveStdStakSplice     = 1
saveStdStakSpliceComp = 1
saveStakPrimi         = 1
saveStakComp          = 1
saveStakPickle        = 1

## Save which trace?
saveTrace             = 0
saveTraceCompact      = 1
saveTracePickle       = 1

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
