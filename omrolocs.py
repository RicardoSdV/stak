"""
How to use:
    - Paste STAK class definition and stak = STACK() object instantiation in some high level utils type file
    - Call stak.omrolocs() from any callable to debug, or even a file, anywhere
    - Optionally set the printMRO, adjust the callStackDepth optionally at a global level or by passing the args

Known issues:
    - Caller class cannot be found for wrapped methods and therefore definer class neither (with custom wrappers,
    not @property nor @classmethod, yes @staticmethod but for other reasons)

    - A private property will default to filename & lineno,

    - If the object object autopassed to an instance method is not called 'self' defaults to filename & lineno

    - If the class object autopassed to a class method is not called 'cls' defaults to filename & lineno

    - If the method is defined in an old style class, it defaults to filename & lineno


Cool potential features:
    - If there are multiple methods in the call stack that have the same definer and caller class maybe print only
    one copy of the MRO and substitute in the other frames by ... or something. Actually might need the entire MRO.

    - Support finding caller definer & mro classes for static methods, private properties & wrapped methods

    - Somehow better prints for wrappers, would be cool to have CallerCls(DefinerCls.@decorator.methName)
    but im not sure there is a good way of getting the decorator, only the wrapper

    - Add an option to print the stack in multiple lines with indentation

    - wrap long stacks

    - Write a class do
"""

import code
import types
from inspect import stack

from someCode import SomeClass


class STAK(object):
    """
    callChain = [link1, link2, ...] Every link represents a call or, frame in the inspect.stack

    link = (
        i=0 -> mroClsNs: tuple -> (callerCls, ancestorOfCallerCls, ..., definerCls) if caller & definer found else None
        i=1 -> methName: str
        i=2 -> fileName: str
        i=3 -> lineNum: int
    )

    """

    def __init__(self):
        self.log = []

        # Capture Settings
        None

        # Save Settings (cwd == bin paths relative)
        self.savePath = 'default.log'
        self.saveFile = 'default.log'
        self.saveFolder = ''


    """============================================ CAPTURING LOGS PHASE ============================================"""

    def omrolocs(self, callStackDepth=999, silence=False, flags=()):
        if silence: return

        callChain = [self.__linkCreator(*frame) for frame in stack()[1:callStackDepth]]

        self.log.append(callChain)

    @classmethod
    def __linkCreator(cls, frameObj, filePath, lineNum, methName, _, __):
        fLocals = frameObj.f_locals

        callerCls = None
        if 'self' in fLocals:
            callerCls = fLocals['self'].__class__
            defClsCond = cls.__privInsMethCond if cls.__isPrivate(methName) else cls.__pubInsMethCond
        elif 'cls' in fLocals:
            callerCls = fLocals['cls']
            defClsCond = cls.__privClsMethCond if cls.__isPrivate(methName) else cls.__pubClsMethCond

        if callerCls is None or isinstance(callerCls, types.ClassType):
            link = (None, methName, filePath.split('\\')[-1], lineNum)
        else:
            mroClsNs = list(cls.__mroClsNsGenerator(callerCls, defClsCond, methName, frameObj.f_code))
            if mroClsNs[-1] == 'object':
                mroClsNs = None
            link = (mroClsNs, methName, filePath.split('\\')[-1], lineNum)

        return link

    @staticmethod
    def __mroClsNsGenerator(callerCls, defClsCond, methName, fCode):
        for cls in callerCls.__mro__:
            yield cls.__name__
            if defClsCond(cls, methName, fCode):
                return

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
    def __pubClsMethCond(cls, methName, fCode):
        if (
            methName in cls.__dict__
            and cls.__dict__[methName].__func__.__code__ is fCode
        ):
            return True
        return False

    @staticmethod
    def __isPrivate(methName):
        return methName.startswith('__') and not methName.endswith('__')

    """=============================================================================================================="""

    """============================================= SAVING LOGS PHASE =============================================="""

    def save(self, path=None, name=None, forceNewDepthOf=None, inclMRO=True):
        if path is None:
            if name is None:
                path = self.savePath
            else:
                path = self.saveFolder + name

        with open(path, 'w') as f:
            f.writelines(self.__linesGenerator(forceNewDepthOf, inclMRO))

    def __linesGenerator(self, forceNewDepthOf, inclMRO):
        for callChain in self.log:
            if isinstance(forceNewDepthOf, int):
                callChain = callChain[:forceNewDepthOf]

            yield ' <- '.join(self.__lineGenerator(callChain, forceNewDepthOf, inclMRO))

    @staticmethod
    def __lineGenerator(callChain, forceNewDepthOf, inclMRO):
        for mroClsNs, methName, fileName, lineNum in callChain[: forceNewDepthOf]:
            if mroClsNs is None:
                yield fileName.replace('.py', str(lineNum)) + '.' + methName
            elif inclMRO:
                mroClsNs[-1] = mroClsNs[-1] + '.' + methName + ')' * (len(mroClsNs) - 1)
                yield '('.join(mroClsNs)
            else:
                yield mroClsNs[-1] + '.' + methName

    """=============================================================================================================="""


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


while True:
    variables = globals().copy()
    variables.update(locals())
    shell = code.InteractiveConsole(variables)
    shell.interact()


















































# end
