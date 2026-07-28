from ..lib import sysExcInfo, tracebackFormatStack, tracebackPrintException, isPy2, sysGetFrame

LOG_DEBUG = False

def LOGGER(msg):  # Override if you want to use a different logger.
    print(msg)

def INFO(message, *args):
    LOGGER('[STAK] INFO : %s' % (message % args))
    return True

def DEBUG(message='', *args):
    if LOG_DEBUG:
        LOGGER('[STAK] DEBUG: %s' % (message % args))
    return True

def ERROR(message='', *args):
    LOGGER('[STAK] ERROR: %s' % (message % args))
    LOG_STACK(2)
    return True

def EXCEPTION(message='', exc=None, *args):
    if message:
        LOGGER('[STAK] EXC  : %s' % (message % args))
    if exc:
        if isPy2:
            tracebackPrintException(*sysExcInfo())
        else:
            tracebackPrintException(exc.__class__, exc, exc.__traceback__)
    return True

def LOG_STACK(frameNum=1):
    frame = sysGetFrame(frameNum)
    for el in tracebackFormatStack(frame):
        LOGGER(('[STAK] FRAME: %s' % el).rstrip('\n'))
