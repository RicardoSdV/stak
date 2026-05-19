from .block00_autoImports import *

## Placeholders
#
c_stak = None  # type: cDLL

@logPlaceholder
def c_init():  # type: () -> None
    """ Init c part of stak """

@logPlaceholder
def c_setIsDev(is_dev):  # type: (cByte) -> None
    """ Enabled logging to file when is_dev == 1 """

@logPlaceholder
def c_setSilentFiles(cnt, paths):  # type: (int, cArr[cCharPtr]) -> None
    """ Free old silent files array make a new one with the passed files. """


## Event handlers
#
@logExcept
def onStakLoads_replaceCPlaceholders():
    DEBUG('Replacing c placeholders')

    if stakBinaryDirPath not in sysPath:
        sysPath.append(stakBinaryDirPath)
    import c_stak

    g = globals()

    g['c_stak']     = c_stak
    g['c_init']     = c_stak.stak_init
    g['c_setIsDev'] = c_stak.stak_set_is_dev

def onStakLoads_setSettingsToC():
    setSettingsToC()
    c_init()  # Init after settings, so init happens with proper settings.

def onStakReloads_setSettingsToC():
    setSettingsToC()

def onSettingsReload_setSettingsToC():
    setSettingsToC()


## Code
#
def setSettingsToC():
    DEBUG('setSettingsToC')

    c_setIsDev(isDev)
    c_setSilentFiles(len(silentFiles), silentFiles)
