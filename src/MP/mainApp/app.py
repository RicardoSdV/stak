from random import randint
from time import clock

from src.MP.mainApp.myLogging import myLogger, startLogger


def run():
    cnt = 0

    startLogger()

    while True:
        doWork()
        if cnt == 100:
            if not input('Continue?'):
                exit()
            cnt = 0
        cnt += 1



def doWork():
    _int = randint(0, 10)
    myLogger('My int = %s, at time = %s' % (_int, clock()))


