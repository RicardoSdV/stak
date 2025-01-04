

## Labels
eventLabels = ['PRE EVENT 1', 'POST EVENT 1']

## Dir paths: Change often
taskDir  = 'task'
printDir = 'print'

## Dir paths: semi-static
rootDir  = '.STAK'
primiDir = 'primitives'
variDir  = 'variants'
stdDir   = ''

## File prefixes
stakLogPrefix  = 'stak'
stdLogPrefixes = ('stdLogA', 'stdLogB')
traceLogPrefix = 'trace'

## File suffixes
primiSuffix             = ''
compSuffix              = 'Compress'
stdStakSpliceSuffix     = 'Splice'
compStdStakSpliceSuffix = ''
compactSuffix           = 'Compact'

logFilesExt = '.log'

## Increases compress times exponentially
maxCompressGroupSize = 100

def reloadSettings():
    from sys import modules
    reload(modules[__name__])
