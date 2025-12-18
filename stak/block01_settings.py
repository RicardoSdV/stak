""" Settings: configurable parameters. Can be reloaded, dynamic references. """

## Labels
eventLabels = ['PRE EVENT 1', 'POST EVENT 1']

## Dir paths: Change often
taskDir  = 'task_stak'
printDir = 'print1'

silenceTrace = 0

# Exclude paths that contain any part of the paths in here.
silentFiles = []

# If any, only allow paths that contain any part of paths here.
loudFiles = []

# TODO: Ideally pickles would all be in some backup file, and the
#  path could be built dynamically based on the task name & print.
loadAndResavePath = r'.STAK\task\print\pickle\pickle.pkl'

isDev = 1

## File prefixes
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
savePrimis            = saveStakPrimi or saveStdPrimi
saveVaris             = saveStakComp or saveStdStakSpliceComp

## Save which trace?
saveTrace        = 0
saveTraceCompact = 0
saveTracePickle  = 0
printLiveTrace   = 1

## Std logs interceptor
interceptLogs      = 1
saveInterceptLogs  = 1
letGoInterceptLogs = 1  # After intercepting, call the original handlers too.

# Used to decipher what callables should be intercepted, and weather the intercepts should be saved.
# Format 4 meth: (moduleDotPath, (clsName, (methName, interceptorName, saveOrNot?)))
# Format 4 func: (moduleDotPath[:-1], (moduleName, (funcName, interceptorName, saveOrNot?)))
# interceptorName: For custom logging integrations, define handler in any stak block.
interceptSettings = (
    # Python standard logs:
    (
        'logging', (
            (('Logger', ), (
                ('debug'    , 'pyInterceptor', 1),
                ('info'     , 'pyInterceptor', 1),
                ('warning'  , 'pyInterceptor', 1),
                ('warn'     , 'pyInterceptor', 1),
                ('error'    , 'pyInterceptor', 1),
                ('exception', 'pyInterceptor', 1),
                ('critical' , 'pyInterceptor', 1),
                ('log'      , 'pyInterceptor', 1),
            ),),
        ),
    ),
    # Custom logging integrations:
)
# Skip saving of log lines which contain strings found in the list.
interceptedLogLinesIgnore = []

overrideSettingsOnLAR = 0

## Dir paths: semi-static
rootDir    = '.STAK'
primiDir   = 'primitives'
variDir    = 'variants'
pickleDir  = 'pickle'

## File suffixes
primiSuffix             = ''
compSuffix              = 'Compress'
stdStakSpliceSuffix     = 'Splice'
compactSuffix           = 'Compact'
