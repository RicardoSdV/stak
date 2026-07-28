from .data_links import omrolocs
from ..lib import (
    importModule, Partial, PY_CRITICAL_LVL, PY_FATAL_LVL, PY_ERROR_LVL, PY_WARNING_LVL, PY_WARN_LVL, PY_INFO_LVL,
    PY_DEBUG_LVL, PY_NOTSET_LVL)
from ..state import config, ogLoggers
from ..utils.ez_log import ERROR

# TODO: What happens when the loggers are not replaced before they are imported? 
# if using the normal python logging it works because it dynamically references the 
# class, but with a function it wont. Instead of replacing swap out the __code__.


def iterInterceptSettings(settings):

    for dotPath, callable_namesByContainers in settings:
        try:
            module = importModule(dotPath)
        except ImportError as e:
            ERROR('Intercept evaded, import failed, %s' % dotPath)
            continue

        for containerName, callableNames in callable_namesByContainers:
            container = getattr(module, containerName, None)
            if container is None:
                ERROR('Intercept evaded, container not found, %s' % dotPath)
                continue

            for calName, interceptorName, saveOrNot in callableNames:
                cal = getattr(container, calName, None)
                if cal is None:
                    ERROR('Intercept evaded, callable not found %s %s %s' % (dotPath, containerName, calName))
                    continue

                yield dotPath, containerName, container, calName, cal, interceptorName, saveOrNot


def replaceLoggers(settings):
    if not config['interceptLogs']:
        return

    _globals = globals()

    for dotPath, containerName, container, calName, cal, interceptorName, saveOrNot in iterInterceptSettings(settings):

        # Save original loggers
        ogLoggers[(dotPath, containerName, calName)] = cal

        # Replace with interceptors
        if interceptorName not in _globals:
            ERROR('Intercept evaded, interceptor not found %s' % interceptorName)
            continue


        setattr(container, calName, _globals[interceptorName])


def restoreLoggers(settings):
    for dotPath, containerName, container, calName, cal, interceptorName, saveOrNot in iterInterceptSettings(settings):
        ogLoggerKey = (dotPath, containerName, calName)
        if ogLoggerKey not in ogLoggers:
            ERROR('OG logger lost %s' % ogLoggerKey)
            continue

        setattr(container, calName, ogLoggers[ogLoggerKey])


## Event handlers
# ---------------------------------------------------------------------------------------------------------------------
def onStakLoads_interceptLoggers():
    replaceLoggers(config['interceptSettings'])

def onSettingsReload_reIntercept(oldSettings, newSettings):
    restoreLoggers(oldSettings['interceptSettings'])
    replaceLoggers(newSettings['interceptSettings'])

def onStakPreReload_restoreLoggers():
    restoreLoggers(config['interceptSettings'])

def onStakPostReload_interceptLoggers():
    replaceLoggers(config['interceptSettings'])
# ---------------------------------------------------------------------------------------------------------------------


## Interceptors
# ---------------------------------------------------------------------------------------------------------------------
def pyLogInterceptor(__lvl__, __log__, self, msg, *args, **kwargs):
    # type: (int, Opt[Cal], Opt[Cal], Logger, str, *Any, **Any) -> None
    msg = msg % args

    import logging

    if __log__:
        __log__(msg)

    if  config['logPyLogOg']:
        __ogCal__(msg, **kwargs)


criticalPyLogInterceptor = Partial(pyLogInterceptor, PY_CRITICAL_LVL, omrolocs)
fatalPyLogInterceptor    = Partial(pyLogInterceptor, PY_FATAL_LVL   , omrolocs)
errorPyLogInterceptor    = Partial(pyLogInterceptor, PY_ERROR_LVL   , omrolocs)
warningPyLogInterceptor  = Partial(pyLogInterceptor, PY_WARNING_LVL , omrolocs)
warnPyLogInterceptor     = Partial(pyLogInterceptor, PY_WARN_LVL    , omrolocs)
infoPyLogInterceptor     = Partial(pyLogInterceptor, PY_INFO_LVL    , omrolocs)
debugPyLogInterceptor    = Partial(pyLogInterceptor, PY_DEBUG_LVL   , omrolocs)
notsetPyLogInterceptor   = Partial(pyLogInterceptor, PY_NOTSET_LVL  , omrolocs)
# ---------------------------------------------------------------------------------------------------------------------
