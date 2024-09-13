"""
ATTENTION! Highly unstable and experimental

This is a research project to see if future stacking is viable

Cool Potential features:
    - Have it work in different modes i.e. trace calls only or more info?


Conclusions:
    - Of course its possible, this is how debuggers work duh

    - Seems like once you set a trace and all the callables are called
    the trace returns to the original callable

    - A cool thing would be to be able to recreate a tree of calls for example

    A -> B -> C -> D|
        |<- <- <- <-|
        |B -> E -> F -> G

Known issues:
    - need to manually unset the trace to avoid following the trace throughout the application

"""
from sys import settrace, gettrace

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import *
    from types import FrameType


class TraceCalls(object):
    """ Sets self as trace, logs all calls """
    __slots__ = ('__traceLog', '__depth')

    def __init__(self):
        self.__traceLog = []
        self.__depth = 0

    def __call__(self, frame, event, arg):  # type: (FrameType, str, Any) -> 'TraceCalls'
        if event == 'call':
            self.__traceLog.append()
        elif event == 'line':
            pass
        elif event == 'return':
            print 'return from', frame.f_code.co_name
        elif event == 'exception':
            pass
        else:
            raise ValueError('Unforeseen event string')

        self.__depth += 1
        return self

    def fomrolocs(self):
        oldTrace = gettrace()
        if oldTrace is not self:
            settrace(self)

traceObj = TraceCalls()


def E(param): print 'Leaf E'; return 5
def D(): return E('param') +1
def C(): print 'Leaf C'
def B(someArg): C(); D()
def A():
    traceObj.fomrolocs()
    B(55)

A()
