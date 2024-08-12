"""
This is a research project to see if future stacking is viable

Conclusions:
    - Of course its possible, this is how debuggers work duh

    - Seems like once you set a trace and all the callables are called
    the trace returns to the original callable

    - A cool thing would be to be able to recreate a tree of calls for example

    A -> B

    Although this is not really representative of the linear nature of things

    Maybe it should be like:

    A -> B -> C -> D|
        |<- <- <- <-|
        |B -> E -> F -> G
"""
from sys import settrace, gettrace

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import *
    from types import FrameType



class TraceClass(object):
    __slots__ = ('__log', )

    def __init__(self):
        self.__log = []

    def __call__(self, frame, event, arg):
        # type: (FrameType, str, Any) -> TraceClass
        print 'type(arg)', type(arg)
        print 'event: {}, name: {}, arg: {}'.format(event, frame.f_code.co_name, arg)
        return self

    def fomrolocs(self):
        oldTrace = gettrace()
        if oldTrace is not self:
            settrace(self)

traceObj = TraceClass()


def E(param):
    print 'Leaf E'
    return 5
def D(): return E('param') +1
def C(): print 'Leaf C'
def B(someArg): C(); D()
def A(): traceObj.fomrolocs(); B(55)

A()


