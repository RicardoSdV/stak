""" Settings i.e. can change without restarting interpreter.
Modify this file & reload with so.reload() or aliases. """

## Labels
eventLabels = ['PRE EVENT 1', 'POST EVENT 1']

## Dir paths: Change often
taskDir  = 'task'
printDir = 'print'

silenceTrace = 0
silencedFiles = {
    r'C:\prjs\stak\src\stak_func\tester.py': 0
}

## File prefixes
stdLogPrefixes = ('stdLogA', 'stdLogB')
stakLogPrefix  = 'stak'
traceLogPrefix = 'trace'
jsonPrefix     = 'json'
zippedPrefix   = 'zipped'

## Increases compress times exponentially
# reduce if saving takes too long.
maxCompressGroupSize = 100

## Omro(l/p)ocs formatting
tryLogMro         = 1
alwaysLogFilePath = 1
alwaysLogLineno   = 1
includeData       = 1

# Depths, if falsy no limit
defaultPathDepth = 2
maxMroClsNsDepth = 2

## Stak log, save which?
savePrimiStak = 1
saveCompStak  = 1
saveJsonStak  = 1
saveZipStak   = 0

## Standard log, save which?
savePrimiStd = 1

## Spliced logs, save which?
saveStdStakSplice     = 1
saveCompStdStakSplice = 1

## Save which trace?
saveTrace        = 1
saveCompactTrace = 1
saveJsonTrace    = 1
saveZipTrace     = 0

## Dir paths: semi-static
rootDir  = '.STAK'
primiDir = 'primitives'
variDir  = 'variants'
stdDir   = ''
jsonDir  = 'json'

## File suffixes
primiSuffix             = ''
compSuffix              = 'Compress'
stdStakSpliceSuffix     = 'Splice'
compStdStakSpliceSuffix = ''
compactSuffix           = 'Compact'
