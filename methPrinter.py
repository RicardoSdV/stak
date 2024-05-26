from inspect import stack
from types import ClassType, FunctionType

from testCode import SomeClass


def MROpOCS(printMRO=False, callStackDepth=4):
    frames, clsMethStrs = stack()[1:callStackDepth+1], []

    callChain = []
    for frame in frames:
        fObj, methName, = frame[0], frame[3]; fLocals = fObj.f_locals

        isInsMeth = True if 'self' in fLocals else False
        isClsMeth = True if 'cls' in fLocals else False
        callerCls = fLocals['self'].__class__ if isInsMeth else fLocals['cls'] if isClsMeth else None

        if not (isInsMeth or isClsMeth) or isinstance(callerCls, ClassType):
            callChain.append(frame[1] + '.' + methName)
            continue

        fCode = fObj.f_code
        clsNs = []
        isPrivate = True if methName.startswith('__') and not methName.endswith('__') else False
        if isInsMeth:
            if isPrivate:
                found = False
                for cls in callerCls.__mro__:
                    clsNs.append(cls.__name__)
                    for attr in cls.__dict__.values():
                        if isinstance(attr, FunctionType) and attr.__name__ == methName and attr.func_code is fCode:
                            found = True; break
                    if found: break
            else:
                for cls in callerCls.__mro__:
                    clsNs.append(cls.__name__)
                    if methName in cls.__dict__ and cls.__dict__[methName].func_code is fCode:
                        break
        elif isClsMeth:
            if isPrivate:
                found = False
                for cls in callerCls.__mro__:
                    clsNs.append(cls.__name__)
                    for attr in cls.__dict__.values():
                        if isinstance(attr, classmethod) and attr.__func__.__name__ == methName and attr.__func__.__code__ is fCode:
                            found = True; break
                    if found: break
            else:
                for cls in callerCls.__mro__:
                    clsNs.append(cls.__name__)
                    if methName in cls.__dict__ and cls.__dict__[methName].__func__.__code__ is fCode:
                        break

        if printMRO:
            clsNs[-1] = clsNs[-1] + '.' + methName + ')' * (len(clsNs) -1); callChain.append('('.join(clsNs))
        else:
            callChain.append(clsNs[-1] + '.' + methName)

    print ' <- '.join(callChain)


class ITest(object):
    def testCallerOfCaller(self): raise NotImplementedError()
class TestGanny(object): pass
class TestDaddy(TestGanny):
    def test(self): MROpOCS()
    def __testCaller(self): self.test()
    def testCaller(self):
        localVar = 1
        self.__testCaller()
class Test(TestDaddy, ITest):
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
    def __classMethTest(cls): TestDawg().testCallerOfCaller()

class TestSomeOtherClassWithSameNameStaticMeth(ParentStatConf):
    @staticmethod
    def statMethTest(): pass

SomeClass().someMeth()

class TestOutcastSon(TestOutcast): pass

def testFunc():
    TestOutcastSon()

class TestOldStyle:
    @staticmethod
    def oldStyleStaticMeth():
        testFunc()

    @classmethod
    def oldStyleClassMeth(cls):
        cls.oldStyleStaticMeth()

    def oldStyleInstanceMeth(self):
        self.oldStyleClassMeth()


TestOldStyle().oldStyleInstanceMeth()
