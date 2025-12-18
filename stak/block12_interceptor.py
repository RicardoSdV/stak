from .block00_autoImports import *

def iterInterceptSettings(settings):
    # type: (tuple) -> Itrt[Tup[str, object, Cal]]

    for dotPath, callable_namesByContainers in settings:
        try:
            module = importModule(dotPath)
        except ImportError as e:
            print '[STAK] ERROR: Intercept evaded, import fail', dotPath, e
            continue

        for containerName, callableNames in callable_namesByContainers:
            container = getattr(module, containerName, None)
            if container is None:
                print '[STAK] ERROR: Intercept evaded, container not found', dotPath, containerName
                continue

            for calName, interceptorName, saveOrNot in callableNames:
                cal = getattr(container, calName, None)
                if cal is None:
                    print '[STAK] ERROR: Intercept evaded, callable not found', dotPath, containerName, calName
                    continue

                yield dotPath, containerName, container, calName, cal, interceptorName, saveOrNot


def replaceLoggers(settings):
    if not interceptLogs:
        return

    for dotPath, containerName, container, calName, cal, interceptorName, saveOrNot in iterInterceptSettings(settings):
        # Save original loggers
        ogLoggers[(dotPath, containerName, calName)] = cal

        # Replace with interceptors
        if interceptorName not in gSpace:
            print '[STAK] ERROR: Intercept evaded, interceptor not found', interceptorName
            continue
        setattr(container, calName, gSpace[interceptorName])


def restoreLoggers(settings):
    for dotPath, containerName, container, calName, cal, interceptorName, saveOrNot in iterInterceptSettings(settings):
        ogLoggerKey = (dotPath, containerName, calName)
        if ogLoggerKey not in ogLoggers:
            print '[STAK] ERROR: OG logger lost', ogLoggerKey
            continue

        setattr(container, calName, ogLoggers[ogLoggerKey])


## Event handlers
# ---------------------------------------------------------------------------------------------------------------------
def onStakLoads_intercept():
    replaceLoggers(interceptSettings)


def onSettingsReload_reIntercept(oldSettings, newSettings):
    restoreLoggers(oldSettings['interceptSettings'])
    replaceLoggers(newSettings['interceptSettings'])

def onStakPreReload_restoreLoggers():
    restoreLoggers(interceptSettings)
# ---------------------------------------------------------------------------------------------------------------------


## Interceptors
# ---------------------------------------------------------------------------------------------------------------------
def pyLogInterceptor(__log__, __ogCal__, self, msg, *args, **kwargs):
    # type: (Opt[Cal], Opt[Cal], Logger, str, *Any, **Any) -> None
    msg = msg % args

    if __log__:
        __log__(msg)

    if __ogCal__:
        __ogCal__(msg, **kwargs)
# ---------------------------------------------------------------------------------------------------------------------
