from .block00_typing import *
from .z_utils import tryCall


class Settings(object):
    """ The contents of __init__ is injected using the settings in block01_settings,
    so, add new settings in block01_settings & run ..injectors.py

    Otherwise, to modify existing settings before starting the interpreter it is enough
    to modify block02_settings & the settings object will be modified on first import.

    To update the settings object once the interpreter is running, modify settings in block02_settings
    & call so.reload() or its aliases found in stak.__init__, to update the settings object.

    Therefore, to keep settings dynamic reference the ones in the settings object, don't
    import settings from block01_settings. """

    __slots__ = ('stakLogPrefix', 'compStdStakSpliceSuffix', 'maxMroClsNsDepth', 'tryLogMro', 'primiSuffix', 'defaultPathDepth', 'eventLabels', 'compactSuffix', 'traceLogPrefix', 'primiDir', 'variDir', 'alwaysLogFilePath', 'taskDir', 'compSuffix', 'stdLogPrefixes', 'printDir', 'stdStakSpliceSuffix', 'rootDir', 'silencedFiles', 'alwaysLogLineno', 'maxCompressGroupSize', 'stdDir', 'jsonDir', 'includeData', 'savePrimiStak', 'savePrimiStd', 'saveStakComp', 'saveSplice', 'saveCompSplice')  # This line was injected by injectors.py

    def __init__(self):


        ## Labels
        self.eventLabels = ['PRE EVENT 1', 'POST EVENT 1']

        ## Dir paths: Change often
        self.taskDir  = 'task'
        self.printDir = 'print'

        self.silencedFiles = {

        }

        ## File prefixes
        self.stdLogPrefixes = ('stdLogA', 'stdLogB')
        self.stakLogPrefix  = 'stak'
        self.traceLogPrefix = 'trace'

        # Omro(l/p)ocs formatting
        self.tryLogMro         = True
        self.alwaysLogFilePath = False
        self.alwaysLogLineno   = False
        self.defaultPathDepth  = 2
        self.maxMroClsNsDepth  = None
        self.includeData       = True

        ## Save which?
        self.savePrimiStak  = True
        self.savePrimiStd   = True
        self.saveStakComp   = True
        self.saveSplice     = True
        self.saveCompSplice = True

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

        ## Increases compress times exponentially
        self.maxCompressGroupSize = 100


        ## Init finit (do not delete this comment)

    savePrimis = property(lambda self: self.savePrimiStak or self.savePrimiStd)
    saveVaris  = property(lambda self: self.saveStakComp  or self.saveSplice)

    def reload(self):
        from . import block01_settings as s
        for name, setting in reload(s).__dict__.iteritems():
            if not name.startswith('__') and not name.endswith('__'):
                tryCall(setattr, self, name, setting, errMess='If this error is raised by injectors.py, its fine, works anyway, (probably...)')

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


so = Settings()
so.reload()
