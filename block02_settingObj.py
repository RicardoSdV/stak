from .block00_typing import *
from .z_utils import tryCall


class Settings(object):
    """ The contents of __init__ is injected using the settings in block01_settings,
    so, add new settings in block01_settings & run ..injectors.py

    Otherwise, to modify existing settings before starting the interpreter it is enough
    to modify block02_settings & the settings object will be modified on first import.

    To update the settings object once the interpreter is running, modify settings in block02_settings
    & call so.reload() or its aliases found in stak\__init__.py, to update the settings object.

    Therefore, to keep settings dynamic reference the ones in the settings object, don't
    import settings from block01_settings. """

    __slots__ = ['saveStakComp', 'loudFiles', 'stakLogPrefix', 'saveTraceCompact', 'saveTrace', 'zippedPrefix', 'maxMroClsNsDepth', 'tryLogMro', 'saveStdPrimi', 'primiSuffix', 'saveStakPickle', 'logCallsFromLineno', 'defaultPathDepth', 'eventLabels', 'saveStdStakSpliceComp', 'compStdStakSpliceSuffix', 'picklePrefix', 'silenceTrace', 'traceLogPrefix', 'overrideSettingsOnLAR', 'loadAndResavePath', 'primiDir', 'saveTracePickle', 'variDir', 'saveStdStakSplice', 'silentFiles', 'alwaysLogFilePath', 'taskDir', 'compSuffix', 'saveStakPrimi', 'includeData', 'compactSuffix', 'stdLogPrefixes', 'printDir', 'stdStakSpliceSuffix', 'rootDir', 'pickleDir', 'alwaysLogLineno', 'maxCompressGroupSize', 'stdDir', 'repeatSilence']  # This line was injected by injectors.py

    def __init__(self):
        """ Settings i.e. can change without restarting interpreter.
        Modify this file & reload with so.reload() or aliases. """

        ## Labels
        self.eventLabels = ['PRE EVENT 1', 'POST EVENT 1']

        ## Dir paths: Change often
        self.taskDir  = 'task_stak'
        self.printDir = 'print'

        self.silenceTrace = 0

        self.repeatSilence = 30

        # Exclude paths that contain any part of the paths in here.
        self.silentFiles = []

        # If any, only allow paths that contain any part of paths here.
        self.loudFiles = []

        # TODO: Ideally pickles would all be in some backup file, and the
        #  path could be built dynamically based on the task name & print.
        self.loadAndResavePath = r'.STAK\task\print\pickle\pickle.pkl'

        ## File prefixes
        self.stdLogPrefixes = ('stdLogA', 'stdLogB')
        self.stakLogPrefix  = 'stak'
        self.traceLogPrefix = 'trace'
        self.picklePrefix   = 'pickle'
        self.zippedPrefix   = 'zipped'

        ## Increases compress times exponentially
        # reduce if saving takes too long.
        self.maxCompressGroupSize = 80

        ## Omro(l/p)ocs formatting
        self.tryLogMro          = 1
        self.alwaysLogFilePath  = 1
        self.alwaysLogLineno    = 1
        self.includeData        = 1
        self.logCallsFromLineno = 1  # trace only

        # Depths, if falsy no limit
        self.defaultPathDepth = 1
        self.maxMroClsNsDepth = 1

        ## Save which stak?
        self.saveStdPrimi          = 1
        self.saveStdStakSplice     = 1
        self.saveStdStakSpliceComp = 1
        self.saveStakPrimi         = 1
        self.saveStakComp          = 1
        self.saveStakPickle        = 1

        ## Save which trace?
        self.saveTrace             = 0
        self.saveTraceCompact      = 1
        self.saveTracePickle       = 1

        self.overrideSettingsOnLAR = 0

        ## Dir paths: semi-static
        self.rootDir    = '.STAK'
        self.primiDir   = 'primitives'
        self.variDir    = 'variants'
        self.stdDir     = ''
        self.pickleDir  = 'pickle'

        ## File suffixes
        self.primiSuffix             = ''
        self.compSuffix              = 'Compress'
        self.stdStakSpliceSuffix     = 'Splice'
        self.compStdStakSpliceSuffix = ''
        self.compactSuffix           = 'Compact'
        self.compactSuffix           = 'Compact'
        self.compStdStakSpliceSuffix = ''
        ## Init finit (do not delete this comment)


    savePrimis = property(lambda self: self.saveStakPrimi or self.saveStdPrimi)
    saveVaris  = property(lambda self: self.saveStakComp  or self.saveStdStakSpliceComp)

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

        # from .block03_constants import stakVersion
        # settings['stakVersion'] = stakVersion

        return settings

    def fromDict(self, settings):  # type: (Dic[str, Any]) -> None
        """ Update settings object with settings from dict to recreate backed up json logs """
        for name, setting in settings.iteritems():
            tryCall(
                setattr, self, name, setting,
                errMess='Logs were saved with a setting which no longer exists, '
                        'name=%s, setting=%s' % (name, setting)
            )


def onTraceSilenced(wasSilenced, isSilenced):
    assert wasSilenced != isSilenced

    from .block10_tracing import setTrace, delTrace, traceState

    if not traceState.mayHave: return
    if not wasSilenced and     isSilenced: delTrace(); return
    if     wasSilenced and not isSilenced: setTrace(); return


deltaActionSettings = {
    'silenceTrace': onTraceSilenced,
}

so = Settings()
so.reload()
