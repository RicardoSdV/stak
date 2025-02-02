## Labels
eventLabels = ['PRE EVENT 1', 'POST EVENT 1']

## Dir paths: Change often
taskDir  = 'task'
printDir = 'print'

## Switches: they don't turn off log gathering, but avoid saving the referred entries if switched off.
isOmrolocsOn = True
isDaffOn     = True
isTraceOn    = True

## File prefixes
stdLogPrefixes = ('stdLogA', 'stdLogB')
stakLogPrefix  = 'stak'
traceLogPrefix = 'trace'

## Dir paths: semi-static
rootDir  = '.STAK'
primiDir = 'primitives'
variDir  = 'variants'
stdDir   = ''

## File suffixes
primiSuffix             = ''
compSuffix              = 'Compress'
stdStakSpliceSuffix     = 'Splice'
compStdStakSpliceSuffix = ''
compactSuffix           = 'Compact'

logFilesExt = '.log'

## Increases compress times exponentially
maxCompressGroupSize = 100

blockPrefix = 'block'
