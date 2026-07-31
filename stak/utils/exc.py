""" Its a logger, exceptions are never critical, worst thing that should 
happen is we miss lines, but in dev mode we should let it crash. """

from .log import EXCEPTION
from ..const import isDev
from ..lib import funcToolsWraps


def logExcept(func, default=None):
    if isDev:
        return func

    @funcToolsWraps(func)
    def logExceptWrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            EXCEPTION('Exception in logExcept', exc=e)
            return default

    return logExceptWrapper


def tryCall(_callable, default=None, *args, **kwargs):
    if isDev:
        return _callable(*args, **kwargs)
    
    errMess = kwargs.pop('errMess', None)
    try:
        return _callable(*args, **kwargs)
    except Exception as e:
        if errMess: EXCEPTION(errMess, exc=e)
        else      : EXCEPTION(exc=e)
        return default
