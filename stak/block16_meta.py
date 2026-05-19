from .block00_autoImports import *

def onStakLoads_runInjectors():
    """ Only when isDev, may inject some code and reload stak
    so the code can be used in the same interpreter run. """
    if isDev:
        runInjectors()
        reloadStak()

def reloadSettings():
    oldSettings, newSettings = reloadModByNameGetDiff(__name__, 'settings')
    gSpace.update(newSettings)

    onSettingsReload(oldSettings, newSettings)

def reloadStak():
    """ This reload is when stak is running normally to avoid wiping state.
    When reloading onStakLoads we don't care about state since its on interpreter init.  """

    onStakPreReload()

    reloadUnited(__name__, staticModNames=staticBlockNames)

    onStakPostReload()


def jamInterfaceIntoBuiltins(interfaceNames, allNames): # type: (Itrb[str], Dic[str, Any]) -> None
    reloading = __package__ in sysModules
    for name in interfaceNames:
        if reloading or name not in builtins:
            builtins[name] = allNames[name]
        else:
            E('COLLISION!', name=name)

    if isDev and packageName not in builtins:
        builtins[packageName] = sysModules[__name__]
