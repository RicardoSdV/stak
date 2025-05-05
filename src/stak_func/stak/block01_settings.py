""" Settings i.e. can change without restarting interpreter.
Modify this file & reload with so.reload() or aliases. """

## Labels
eventLabels = ['PRE EVENT 1', 'POST EVENT 1']

## Dir paths: Change often
taskDir  = 'task'
printDir = 'print'

silencedFiles = {
    r'C:\prjs\stak\src\stak_func\tester.py': 0
}

## File prefixes
stdLogPrefixes = ('stdLogA', 'stdLogB')
stakLogPrefix  = 'stak'
traceLogPrefix = 'trace'

# Omro(l/p)ocs formatting
tryLogMro         = True
alwaysLogFilePath = False
alwaysLogLineno   = False
defaultPathDepth  = 2
maxMroClsNsDepth  = 2  # If falsy no limit
includeData       = True

## Save which?
savePrimiStak  = True
savePrimiStd   = True
saveStakComp   = True
saveSplice     = True
saveCompSplice = True

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

## Increases compress times exponentially
maxCompressGroupSize = 100


