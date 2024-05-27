"""
How to use:
    - Paste def oMROpOCS in some high level utils type file
    - Call oMROpOCS() from the callable to debug
    - Optionally set the printMRO and adjust the callStackDepth optionally at a global level or by passing the args

Known issues:
    - Wrappers

Unknown issues:
    - How does this behave when a method overrides its predecessor and also calls it with super()?

Cool potential features:
    - If there are multiple methods in the call stack that have the same definer and caller class maybe print only
    one copy of the MRO and substitute in the other frames by ... or something

    - Support static methods
"""

import types
from inspect import stack

from testCode import SomeClass


def oMROpOCS(pMRO=True, callStackDepth=999):
    frames, clsMethStrs, callChain = stack()[1:callStackDepth+1], [], []

    for frame in frames:
        fObj, methName, = frame[0], frame[3]; fLocals = fObj.f_locals

        isInsMeth = True if 'self' in fLocals else False; isClsMeth = True if 'cls' in fLocals else False
        callerCls = fLocals['self'].__class__ if isInsMeth else fLocals['cls'] if isClsMeth else None

        if not (isInsMeth or isClsMeth) or isinstance(callerCls, types.ClassType):
            callChain.append(frame[1].split('/')[-1] + '.' + methName); continue

        definerClsFound, fCode, clsNs = False, fObj.f_code, []
        isPrivate = True if methName.startswith('__') and not methName.endswith('__') else False
        if isInsMeth:
            if isPrivate:
                for cls in callerCls.__mro__:
                    clsNs.append(cls.__name__)
                    for attr in cls.__dict__.values():
                        if isinstance(attr, types.FunctionType) and attr.__name__ == methName and attr.func_code is fCode:
                            definerClsFound = True; break
                    if definerClsFound: break
            else:
                for cls in callerCls.__mro__:
                    clsNs.append(cls.__name__)
                    if methName in cls.__dict__:
                        method = cls.__dict__[methName]
                        if isinstance(method, property):
                            if method.fget.func_code is fCode: definerClsFound = True; break
                        elif method.func_code is fCode: definerClsFound = True; break
        elif isClsMeth:
            if isPrivate:
                for cls in callerCls.__mro__:
                    clsNs.append(cls.__name__)
                    for attr in cls.__dict__.values():
                        if isinstance(attr, classmethod) and attr.__func__.__name__ == methName and attr.__func__.__code__ is fCode:
                            definerClsFound = True; break
                    if definerClsFound: break
            else:
                for cls in callerCls.__mro__:
                    clsNs.append(cls.__name__)
                    if methName in cls.__dict__ and cls.__dict__[methName].__func__.__code__ is fCode:
                        definerClsFound = True; break

        if not definerClsFound: callChain.append(frame[1].split('/')[-1] + '.' + methName); continue
        if pMRO: clsNs[-1] = clsNs[-1] + '.' + methName + ')' * (len(clsNs) -1); callChain.append('('.join(clsNs))
        else: callChain.append(clsNs[-1] + '.' + methName)
    print ' <- '.join(callChain)


def testWrapper(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


class ITest(object):
    def testCallerOfCaller(self): raise NotImplementedError()
class TestGanny(object): pass
class TestDaddy(TestGanny):
    @testWrapper
    def test(self): oMROpOCS()
    def __testCaller(self): self.test()
    def testCaller(self): localVar = 1; self.__testCaller()
class Test(TestDaddy, ITest):
    @property
    def testPropCallerOfCallerOfCaller(self): return self.testCallerOfCaller()
    def testCallerOfCaller(self): self.testCaller()
class TestBro(TestDaddy): pass
class TestDawg(Test): pass
class ParentStatConf(object):
    @staticmethod
    def statMethTest(): ParentStatConf.__statMethTest()

    @staticmethod
    def __statMethTest(): TestOutcast.classMethTest()
class TestSomeSomeOtherClassWithSameNameStaticMeth(ParentStatConf):
    @staticmethod
    def statMethTest(): pass

class TestOutcast(ParentStatConf):
    def __init__(self): self.statMethTest()

    @classmethod
    def classMethTest(cls): cls.__classMethTest()

    @classmethod
    def __classMethTest(cls): TestDawg().testPropCallerOfCallerOfCaller
class TestSomeOtherClassWithSameNameStaticMeth(ParentStatConf):
    @staticmethod
    def statMethTest(): pass

SomeClass().someMeth()

class TestOutcastSon(TestOutcast): pass

def testFunc(): TestOutcastSon()

class TestOldStyle:
    @staticmethod
    def oldStyleStaticMeth(): testFunc()

    @classmethod
    def oldStyleClassMeth(cls): cls.oldStyleStaticMeth()

    def oldStyleInstanceMeth(self): self.oldStyleClassMeth()


TestOldStyle().oldStyleInstanceMeth()
