from sys import modules

from .block00_typing import *
from .z_utils import tryCall, E


class Settings(object):
    """ The contents of __init__ is injected using the settings in block01_settings,
    so, add new settings in block01_settings & run ..injectors.py

    Otherwise, to modify existing settings before starting the interpreter it is enough
    to modify block02_settings & the settings object will be modified on first import.

    To update the settings object once the interpreter is running, modify settings in block02_settings
    & call so.reload() or its aliases found in stak.__init__, to update the settings object.

    Therefore, to keep settings dynamic reference the ones in the settings object, don't
    import settings from block01_settings. """

    __slots__ = ('stakLogPrefix', 'compStdStakSpliceSuffix', 'saveStdStakSplice', 'saveTrace', 'zippedPrefix', 'maxMroClsNsDepth', 'savePrimiStd', 'tryLogMro', 'primiSuffix', 'jsonDir', 'primiDir', 'jsonPrefix', 'saveCompStdStakSplice', 'saveCompStak', 'defaultPathDepth', 'eventLabels', 'compactSuffix', 'silenceTrace', 'traceLogPrefix', 'saveJsonStak', 'saveJsonTrace', 'variDir', 'saveZipStak', 'alwaysLogFilePath', 'taskDir', 'compSuffix', 'includeData', 'saveCompactTrace', 'saveZipTrace', 'stdLogPrefixes', 'printDir', 'stdStakSpliceSuffix', 'savePrimiStak', 'rootDir', 'silencedFiles', 'alwaysLogLineno', 'maxCompressGroupSize', 'stdDir')  # This line was injected by injectors.py

    def __init__(self):
        self.compactSuffix           = 'Compact'

        ## Labels
        self.eventLabels = ['PRE EVENT 1', 'POST EVENT 1']

        ## Dir paths: Change often
        self.taskDir  = 'task'
        self.printDir = 'print'

        self.silenceTrace = 0
        self.silencedFiles = {
            r'C:\prjs\stak\src\stak_func\tester.py': 0
        }

        ## File prefixes
        self.stdLogPrefixes = ('stdLogA', 'stdLogB')
        self.stakLogPrefix  = 'stak'
        self.traceLogPrefix = 'trace'
        self.jsonPrefix     = 'json'
        self.zippedPrefix   = 'zipped'

        ## Increases compress times exponentially
        # reduce if saving takes too long.
        self.maxCompressGroupSize = 100

        ## Omro(l/p)ocs formatting
        self.tryLogMro         = 1
        self.alwaysLogFilePath = 1
        self.alwaysLogLineno   = 1
        self.includeData       = 1

        # Depths, if falsy no limit
        self.defaultPathDepth = 2
        self.maxMroClsNsDepth = 2

        ## Stak log, save which?
        self.savePrimiStak = 1
        self.saveCompStak  = 1
        self.saveJsonStak  = 1
        self.saveZipStak   = 0

        ## Standard log, save which?
        self.savePrimiStd = 1

        ## Spliced logs, save which?
        self.saveStdStakSplice     = 1
        self.saveCompStdStakSplice = 1

        ## Save which trace?
        self.saveTrace        = 1
        self.saveCompactTrace = 1
        self.saveJsonTrace    = 1
        self.saveZipTrace     = 0

        ## Dir paths: semi-static
        self.rootDir  = '.STAK'
        self.primiDir = 'primitives'
        self.variDir  = 'variants'
        self.stdDir   = ''
        self.jsonDir  = 'json'

        ## File suffixes
        self.primiSuffix             = ''
        self.compSuffix              = 'Compress'
        self.stdStakSpliceSuffix     = 'Splice'
        self.compStdStakSpliceSuffix = ''
        self.compactSuffix           = 'Compact'
        ## Init finit (do not delete this comment)

    savePrimis = property(lambda self: self.savePrimiStak or self.savePrimiStd)
    saveVaris  = property(lambda self: self.saveCompStak  or self.saveCompStdStakSplice)
    saveJson   = property(lambda self: self.saveJsonTrace or self.saveZipTrace)

    def reload(self):
        from . import block01_settings as s
        for name, newSetting in reload(s).__dict__.iteritems():
            if name.endswith('_'):
                continue

            oldSetting = getattr(self, name, None)
            if oldSetting == newSetting:
                continue

            tryCall(setattr, self, name, newSetting, errMess='If this error is raised by injectors.py, should be fine.')

            if name not in deltaActionSettings:
                continue

            deltaCallable = deltaActionSettings[name]
            deltaCallable(oldSetting, newSetting)

    def toDict(self):  # type: () -> Dic[str, Any]
        """ Serialize settings into a dict to save as json """
        settings = {name: tryCall(getattr, self, name, errMess='Name form slots not initialized, run injectors.py') for name in self.__slots__}

        from .block03_constants import stakVersion
        settings['stakVersion'] = stakVersion

        return settings

    def fromDict(self, settings):  # type: (Dic[str, Any]) -> None
        """ Update settings object with settings from dict to recreate backed up json logs """
        for name, setting in settings.iteritems():
            tryCall(setattr, self, name, setting, errMess='Logs were saved with a setting which no longer exists, name=%s, setting=%s' % (name, setting))


def onTraceSilenced(wasSilenced, isSilenced):
    assert wasSilenced != isSilenced

    from .block10_tracing import setTrace, delTrace, traceState

    if not traceState.mayHave: return
    if not wasSilenced and     isSilenced: delTrace(); return
    if     wasSilenced and not isSilenced: setTrace(); return


deltaActionSettings = {
    'silenceTrace': onTraceSilenced
}

so = Settings()
so.reload()
