from stak import *

def A():
    setTrace()
    B()
    delTrace()

def B():
    res = C(1, 1)
    E()
    return res

def C(a, b):
    D(a, b)
    return D(a, b)

def D(a, b):
    two = a + b
    return two

def E():
    F()

def F():
    G()

def G():
    three = 1 + 2
    try:
        H()
    except ValueError:
        return

def H():
    raise ValueError()


def runTraceTest():
    A()
