from .block00_autoImports import *

def onStakLoads():
    if isDev:
        runInjectors()
        reloadUnited(__name__)

    onStakLoads_intercept()

def reloadSettings():
    oldSettings, newSettings = reloadModByNameGetDiff(__name__, 'settings')
    gSpace.update(newSettings)

    onSettingsReload_updateTracing(oldSettings, newSettings)
    onSettingsReload_reIntercept(oldSettings, newSettings)


def reloadStak():
    """ This reload is when stak is running normally to avoid wiping state. """

    onStakPreReload_restoreLoggers()

    reloadUnited(__name__, staticModNames=('state', ))

    onStakLoads_intercept()


def jamInterfaceIntoBuiltins(interfaceNames, allNames): # type: (Itrb[str], Dic[str, Any]) -> None
    reloading = __package__ in sysModules
    for name in interfaceNames:
        if reloading or name not in builtins:
            builtins[name] = allNames[name]
        else:
            E('COLLISION!', name=name)

    if isDev and packageName not in builtins:
        builtins[packageName] = sysModules[__name__]
