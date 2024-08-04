"""
Sometimes shell interactivity is not possible, not desirable, or simply just overkill, in such cases,
instead of using CALPACMRORSIDAM the functional, printing, subset of its functionality can be found here.

"""
import code
from datetime import datetime
from itertools import repeat
from random import randint
from time import sleep
from types import CodeType

from src.funcs.someCode import SomeClass

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import *
    from collections import *

    SuperSplitLink = Union[Tuple[List[str], str], Tuple[str, int, str]]
    SemiSplitLink  = Tuple[Union[List[str], str], str]

    EntryWithStrStamps = Tuple[Tuple[str, str, str, str], str, Union[SuperSplitLink, str]]

    StrLinkCallChainEntry   = Tuple[float, str, List[str]]


"""================================================ INITIALISING ================================================"""

import os as __os; from types import ClassType as __OldStyleClsType; from datetime import datetime as __dt
import time as __ti; import shutil as __shutil; import re as __re; from types import FunctionType as __FunctionType
from collections import defaultdict as __DefaultDict, OrderedDict as __OrderedDict; import sys as __sys
from itertools import izip as __izip

# init
__getFrame = __sys._getframe
__pathSplitChar = '/' if '/' in __getFrame(0).f_code.co_filename else '\\'

"""=============================================================================================================="""

"""================================================== OMROPOCS =================================================="""

def omropocs(silence=False):  # type: () -> None
    if silence: return
    print ' <- '.join(__jointLinksGen())

def __jointLinksGen():  # type: () -> Iterator[str]
    """ Custom for omropocs sometimes you just need a good old generator of strings !"""
    frame, mroClsNsGen, OldStyleClsType = __getFrame(2), __mroClsNsGen, __OldStyleClsType
    privInsMethCond, pubInsMethCond = __privInsMethCond, __pubInsMethCond
    privClsMethCond, pubClsMethCond = __privClsMethCond, __pubClsMethCond
    pathSplitChar = __pathSplitChar

    while frame:
        codeObj, fLocals = frame.f_code, frame.f_locals
        methName = codeObj.co_name

        callerCls = None
        if 'self' in fLocals:
            callerCls = fLocals['self'].__class__
            defClsCond = privInsMethCond if methName.startswith('__') and not methName.endswith('__') else pubInsMethCond
        elif 'cls' in fLocals:
            callerCls = fLocals['cls']
            defClsCond = privClsMethCond if methName.startswith('__') and not methName.endswith('__') else pubClsMethCond

        if callerCls is None or isinstance(callerCls, OldStyleClsType):
            yield '{}{}.{}'.format(codeObj.co_filename.split(pathSplitChar)[-1].rstrip('py'), frame.f_lineno, methName)
        else:
            # PyCharm thinks defClsCond could be undefined, but if callerCls is not None it must be defined
            mroClsNs = list(mroClsNsGen(callerCls, defClsCond, methName, codeObj))
            if mroClsNs[-1] == 'object':  # Sometimes definer class not found so follow inheritance tree to the root
                yield '{}{}.{}'.format(codeObj.co_filename.split(pathSplitChar)[-1].rstrip('py'), frame.f_lineno, methName)
            else:
                mroClsNs[-1] = '{}.{}{}'.format(mroClsNs[-1], methName, ')' * (len(mroClsNs) - 1))
                yield '('.join(mroClsNs)

        frame = frame.f_back

def __mroClsNsGen(
        callerCls,  # type: Type[Any]
        defClsCond,  # type: Callable[[Type[Any], str, CodeType], bool]
        methName,  # type: str
        codeObj  # type: CodeType
):  # type: (...) -> Iterator[str]

    for cls in callerCls.__mro__:
        yield cls.__name__
        if defClsCond(cls, methName, codeObj):
            return

def __privInsMethCond(defClsMaybe, methNameToFindDefClsOf, codeObjToFindDefClsOf):
    # type:          (Type[Any]  , str                   , CodeType             ) -> bool

    # This works even when the class defined __slots__ because we're iterating over the class objects' __dict__
    # not the object objects', & as far as I know class objects always have __dict__ even if they declare __slots__
    for attr in defClsMaybe.__dict__.values():
        if (
                isinstance(attr, __FunctionType) and
                attr.__name__ == methNameToFindDefClsOf and
                # If the code object is the same do we need to compare the meth name too??
                attr.func_code is codeObjToFindDefClsOf
        ):
            return True
    return False

def __pubInsMethCond (defClsMaybe, methNameToFindDefClsOf, codeObjToFindDefClsOf):
    # type:         (Type[Any]  , str                   , CodeType             ) -> bool

    # This works even when the class defined __slots__ because we're iterating over the class objects' __dict__
    # not the object objects', & as far as I know class objects always have __dict__ even if they declare __slots__
    if methNameToFindDefClsOf in defClsMaybe.__dict__:
        method = defClsMaybe.__dict__[methNameToFindDefClsOf]

        if isinstance(method, property):
            # PyCharm thinks func_code don't exist, it's wrong
            if method.fget.func_code is codeObjToFindDefClsOf:
                return True
        elif method.func_code is codeObjToFindDefClsOf:
            return True
    return False

def __privClsMethCond(defClsMaybe, methNameToFindDefClsOf, codeObjToFindDefClsOf):
    # type:          (Type[Any]  , str,                    CodeType             ) -> bool

    # This works even when the class defined __slots__ because we're iterating over the class objects' __dict__
    # not the object objects', & as far as I know class objects always have __dict__ even if they declare __slots__
    for attr in defClsMaybe.__dict__.values():
        if (
                isinstance(attr, classmethod)
                and attr.__func__.__name__ == methNameToFindDefClsOf
                # PyCharms thinks __code__ don't exist, it's wrong
                and attr.__func__.__code__ is codeObjToFindDefClsOf
        ):
            return True
    return False

def __pubClsMethCond (defClsMaybe, methNameToFindDefClsOf, codeObjToFindDefClsOf):
    # type:         (Type[Any]  , str                   , CodeType             ) -> bool

    # This works even when the class defined __slots__ because we're accessing class objects' __dict__ not the
    # object objects', & as far as I know class objects always have __dict__ even if they declare __slots__
    if (
            methNameToFindDefClsOf in defClsMaybe.__dict__
            and defClsMaybe.__dict__[methNameToFindDefClsOf].__func__.__code__ is codeObjToFindDefClsOf
    ):
        return True
    return False

"""=============================================================================================================="""



def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
class Interface(object):
    def testCallerOfCaller(self): raise NotImplementedError()
class Ganny(object): pass
class Daddy(Ganny):
    @decorator
    def test(self):
        omropocs()
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

