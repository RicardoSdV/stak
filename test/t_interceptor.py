import logging

logger = logging.getLogger(__name__)


def customLoggingFunc(*args, **kwargs):
    args = ' '.join(args)
    kwargs = ', '.join('%s = %s' % (k, v) for k, v in kwargs.iteritems())
    print args, kwargs

def raiseException():
    raise Exception

def logErr():
    try:
        raiseException()
    except Exception as e:
        logger.error('exception raised', exc_info=e)

def logInfo():
    logger.info('some vital info = %s', 'tempus fugit')

def logDebug():
    two = 2
    logger.debug('some less vital info = %s, equals %s', 'onePlusOne', two)

def logCritical():
    try:
        raiseException()
    except Exception as e:
        logger.critical('its all one to shit = %s' % e)


def runInterceptTest():
    class ReprClass(object):
        def __repr__(self):
            return 'ReprClass(someInfo)'

    obj = ReprClass()
    customLoggingFunc('MYLOGGING: ', someObj=obj)
    logInfo()
    logDebug()
    logCritical()
    logErr()
