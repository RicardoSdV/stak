from multiprocessing import Process, Queue
import atexit

from src.MP.loggingApp.logging import interpreter2Logger


logProcess = None
logQueue = Queue()


def myLogger(msg):
    print 'From interpreter1:', msg
    logQueue.put(msg)


def startLogger():
    global logProcess

    if logProcess:
        print '[STAK] ERROR: Attempting to start the new logger when one is already running.'
        return

    logProcess = Process(target=interpreter2Logger, args=(logQueue, ))
    logProcess.daemon = True
    logProcess.start()

    atexit.register(stopLogger)

def stopLogger():
    if not logProcess:
        print '[STAK] ERROR: Attempting to stop a logger when none exists.'
        return

    logQueue.put('__STOP__')
    logProcess.join()
