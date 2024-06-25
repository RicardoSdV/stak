"""
How to use:
    - Paste def omropocs in some high level utils type file
    - Call omropocs() from the callable to debug
    - Optionally set the printMRO and adjust the callStackDepth optionally at a global level or by passing the args

Known issues:
    - Wrappers & static methods

Unknown issues:
    - How does this behave when a method overrides its predecessor and also calls it with super()?

Cool potential features:
    - If there are multiple methods in the call stack that have the same definer and caller class maybe print only
    one copy of the MRO and substitute in the other frames by ... or something

    - Support finding caller definer & mro classes for static methods

    - Somehow better prints for wrappers, maybe skip? compress?

    - Support force passing the definer class as kwarg, to have good prints if there are static methods or wrappers
    in the meanwhile

    - Add an option to print the stack in multiple lines with indentation

    - Add option to print a trimmed version of the callstack, only the first and last frame
"""

import types
from inspect import stack

from someCode import SomeClass


def privateInsMethCond(cls, methName, fCode):
    for attr in cls.__dict__.values():
        if isinstance(attr, types.FunctionType) and attr.__name__ == methName and attr.func_code is fCode:
            return True
    return False


def privateClsMethCond(cls, methName, fCode):
    for attr in cls.__dict__.values():
        if isinstance(attr, classmethod) and attr.__func__.__name__ == methName and attr.__func__.__code__ is fCode:
            return True
    return False


def publicInsMethCond(cls, methName, fCode):
    if methName in cls.__dict__:
        method = cls.__dict__[methName]
        if isinstance(method, property):
            if method.fget.func_code is fCode:
                return True
        elif method.func_code is fCode:
            return True
    return False


def publicClsMethCond(cls, methName, fCode):
    if methName in cls.__dict__ and cls.__dict__[methName].__func__.__code__ is fCode:
        return True
    return False


def getDefinerClsFoundCond(isInsMeth, isClsMeth, isPrivate):
    if isInsMeth:
        if isPrivate:
            return privateInsMethCond
        else:
            return publicInsMethCond
    elif isClsMeth:
        if isPrivate:
            return privateClsMethCond
        else:
            return publicClsMethCond
    else:
        return None




def omropocs(pMRO=True, callStackDepth=999, silence=False):
    if silence: return

    callChain = []
    for frameObj, filePath, lineNum, methName, _, _ in stack()[1:callStackDepth+1]:

        fLocals = frameObj.f_locals
        fCode = frameObj.f_code

        isInsMeth = True if 'self' in fLocals else False
        isClsMeth = True if 'self'  in fLocals else False
        callerCls = fLocals['self'].__class__ if isInsMeth else fLocals['self'] if isClsMeth else None

        if not (isInsMeth or isClsMeth) or isinstance(callerCls, types.ClassType):
            callChain.append(filePath.split('/')[-1].replace('.py', str(lineNum)) + '.' + methName); continue

        definerClsFound, clsNs = False, []
        isPrivate = True if methName.startswith('__') and not methName.endswith('__') else False

        isDefinerClsFoundCond = getDefinerClsFoundCond(isInsMeth, isClsMeth, isPrivate)
        if isDefinerClsFoundCond is not None:
            for cls in callerCls.__mro__:
                if isDefinerClsFoundCond(cls, methName, fCode):
                    definerClsFound = True
                    break

        if not definerClsFound:
            print 'Definer self not found'
            callChain.append(filePath.split('/')[-1].replace('.py', str(lineNum)) + '.' + methName); continue
        if pMRO: clsNs[-1] = clsNs[-1] + '.' + methName + ')' * (len(clsNs) -1); callChain.append('('.join(clsNs))
        else: callChain.append(clsNs[-1] + '.' + methName)

    print ' <- '.join(callChain)


def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


class Interface(object):
    def testCallerOfCaller(self): raise NotImplementedError()
class Ganny(object): pass
class Daddy(Ganny):
    @decorator
    def test(self): omropocs()
    def __testCaller(self): self.test()
    def testCaller(self): localVar = 1; self.__testCaller()
class SomeCls(Daddy, Interface):
    @property
    def propCallerOfCallerOfCaller(self): return self.testCallerOfCaller()
    def testCallerOfCaller(self): self.testCaller()
class Bro(Daddy): pass
class Dawg(SomeCls): pass
class ParentStatConf(object):
    @staticmethod
    def statMeth(): ParentStatConf.__statMeth()

    @staticmethod
    def __statMeth(): Outcast.classMeth()
class SomeSomeOtherClassWithSameNameStaticMeth(ParentStatConf):
    @staticmethod
    def statMeth(): pass

class Outcast(ParentStatConf):
    def __init__(self): self.statMeth()

    @classmethod
    def classMeth(cls): cls.__classMeth()

    @classmethod
    def __classMeth(cls): Dawg().propCallerOfCallerOfCaller
class SomeOtherClassWithSameNameStaticMeth(ParentStatConf):
    @staticmethod
    def statMeth(): pass

SomeClass().someMeth()

class OutcastSon(Outcast): pass

def func(): OutcastSon()

class OldStyle:
    @staticmethod
    def oldStyleStaticMeth(): func()

    @classmethod
    def oldStyleClassMeth(cls): cls.oldStyleStaticMeth()

    def oldStyleInstanceMeth(self): self.oldStyleClassMeth()


OldStyle().oldStyleInstanceMeth()
