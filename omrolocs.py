"""
The idea is to speed up & make more readable omropocs & potentially future functionality & combine with trimLog, by
putting everything in a class, hold future logs as attributes & interact with them though the live command line of
whatever application it's being used in, like I don't know, a tank game, who knows.
"""
import types
from inspect import stack

from someCode import SomeClass


class STAK(object):

    def __init__(self):
        self.isPrinting = False
        self.isSaving = False
        self.currentLog = 'default'
        self.logs = {}

    @staticmethod
    def __privInsMethCond(cls, methName, fCode):
        for attr in cls.__dict__.values():
            if (
                isinstance(attr, types.FunctionType)
                and attr.__name__ == methName
                and attr.func_code is fCode
            ):
                return True
        return False

    @staticmethod
    def __privClsMethCond(cls, methName, fCode):
        for attr in cls.__dict__.values():
            if (
                isinstance(attr, classmethod)
                and attr.__func__.__name__ == methName
                and attr.__func__.__code__ is fCode
            ):
                return True
        return False

    @staticmethod
    def __pubInsMethCond(cls, methName, fCode):
        if methName in cls.__dict__:
            method = cls.__dict__[methName]

            if isinstance(method, property):
                if method.fget.func_code is fCode:
                    return True
            elif method.func_code is fCode:
                return True
        return False

    @staticmethod
    def __pubClsMethCond(cls, methName, fCode):
        if (
            methName in cls.__dict__
            and cls.__dict__[methName].__func__.__code__ is fCode
        ):
            return True
        return False

    @staticmethod
    def __default_to_file_name_and_lineno(filePath, lineNum, methName):
        return filePath.split('\\')[-1].replace('.py', str(lineNum)) + '.' + methName

    @staticmethod
    def __isPrivate(methName):
        return methName.startswith('__') and not methName.endswith('__')

    @staticmethod
    def __mroClsNsGenerator(callerCls, defClsCond, methName, fCode):
        for cls in callerCls.__mro__:
            yield cls.__name__
            if defClsCond(cls, methName, fCode):
                yield True
                return
        yield False

    def callChainElementCreator(self, inclMro, frameObj, filePath, lineNum, methName, _, __):
        fLocals = frameObj.f_locals

        if 'self' in fLocals:
            callerCls = fLocals['self'].__class__
            defClsCond = self.__privInsMethCond if self.__isPrivate(methName) else self.__pubInsMethCond
        elif 'cls' in fLocals:
            callerCls = fLocals['cls']
            defClsCond = self.__privClsMethCond if self.__isPrivate(methName) else self.__pubClsMethCond
        else:
            return self.__default_to_file_name_and_lineno(filePath, lineNum, methName)

        if isinstance(callerCls, types.ClassType):  # Old style classes
            return self.__default_to_file_name_and_lineno(filePath, lineNum, methName)

        mroClsNs = list(self.__mroClsNsGenerator(callerCls, defClsCond, methName, frameObj.f_code))
        print 'methName', methName
        print 'mroClsNs', mroClsNs
        print ''

        if mroClsNs.pop():  # Last element True if definer class found, else, False
            if inclMro:
                mroClsNs[-1] = mroClsNs[-1] + '.' + methName + ')' * (len(mroClsNs)-1)
                return '('.join(mroClsNs)
            else:
                return mroClsNs[-1] + '.' + methName
        else:
            return filePath.split('\\')[-1].replace('.py', str(lineNum)) + '.' + methName



    def omrolocs(self, inclMro=True, callStackDepth=999, silence=False):
        if silence: return

        callChain = [self.callChainElementCreator(inclMro, *frame) for frame in stack()[1:callStackDepth]]

        print ' <- '.join(callChain)


stak = STAK()

def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper


class Interface(object):
    def testCallerOfCaller(self): raise NotImplementedError()
class Ganny(object): pass
class Daddy(Ganny):
    @decorator
    def test(self): stak.omrolocs()
    @property
    def __privProp(self): return self.test()
    def __testCaller(self): self.__privProp
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
