from functools import partial
from sys import _getframe
from time import time
from types import FunctionType, ClassType as OldStyleClsType

from .block00_typing import *
from .block02_commonData import stakFlags
from .block03_log import appendToLog
from .block04_pathOps import pathSplitChar


def privInsMethCond(defClsMaybe, methNameToFindDefClsOf, codeObjToFindDefClsOf):  # type: (Typ[Any], str, CodeType) -> bool
    # This works even when the class defined __slots__ because we're iterating over the class objects' __dict__
    # not the object objects', & as far as I know class objects always have __dict__ even if they declare __slots__
    for attr in defClsMaybe.__dict__.values():
        if (
                isinstance(attr, FunctionType) and
                attr.__name__ == methNameToFindDefClsOf and
                # If the code object is the same do we need to compare the meth name too??
                attr.func_code is codeObjToFindDefClsOf
        ):
            return True
    return False

def pubInsMethCond (defClsMaybe, methNameToFindDefClsOf, codeObjToFindDefClsOf):  # type: (Typ[Any], str, CodeType) -> bool
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

def privClsMethCond(defClsMaybe, methNameToFindDefClsOf, codeObjToFindDefClsOf):  # type: (Typ[Any], str, CodeType) -> bool
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

def pubClsMethCond (defClsMaybe, methNameToFindDefClsOf, codeObjToFindDefClsOf):  # type: (Typ[Any], str, CodeType) -> bool
    # This works even when the class defined __slots__ because we're accessing class objects' __dict__ not the
    # object objects', & as far as I know class objects always have __dict__ even if they declare __slots__
    if (
            methNameToFindDefClsOf in defClsMaybe.__dict__
            and defClsMaybe.__dict__[methNameToFindDefClsOf].__func__.__code__ is codeObjToFindDefClsOf
    ):
        return True
    return False

def mroClsNsGen(callerCls, defClsCond, methName, codeObj):
    # type: (Typ[Any], Cal[[Typ[Any], str, CodeType], bool], str, CodeType) -> Itrt[str]
    for cls in callerCls.__mro__:
        yield cls.__name__
        if defClsCond(cls, methName, codeObj):
            return

def linksFromFrame(
        joinMroLinksMaybe,   # type: Cal[[Lst[str], str], Uni[str, Tup[Lst[str], str]]]
        joinFileLinksMaybe,  # type: Cal[[str, int, str], Uni[str, Tup[str, int, str]]]
        frame,               # type: FrameType
):                           # type: (...) -> Uni[Tup[str, int, str], Tup[Lst[str], str], str]

    codeObj, fLocals = frame.f_code, frame.f_locals
    methName = codeObj.co_name

    if 'self' in fLocals:
        callerCls = fLocals['self'].__class__
        defClsCond = privInsMethCond if methName.startswith('__') and not methName.endswith('__') else pubInsMethCond
    elif 'cls' in fLocals:
        callerCls = fLocals['cls']
        defClsCond = privClsMethCond if methName.startswith('__') and not methName.endswith('__') else pubClsMethCond
    else:
        callerCls = None

    if callerCls is None or isinstance(callerCls, OldStyleClsType):
        return joinFileLinksMaybe(codeObj.co_filename, frame.f_lineno, methName)
    else:
        # PyCharm thinks defClsCond could be undefined, but if callerCls is not None it must be defined
        mroClsNs = list(mroClsNsGen(callerCls, defClsCond, methName, codeObj))
        if mroClsNs[-1] == 'object':  # Sometimes definer class not found so follow inheritance tree to the root
            return joinFileLinksMaybe(codeObj.co_filename, frame.f_lineno, methName)
        else:
            return joinMroLinksMaybe(mroClsNs, methName)

def joinFileLink(fullPath, lineno, methName, splitChar=pathSplitChar):
    # type: (str, int, str, str) -> str
    return '{}{}.{}'.format(fullPath.split(splitChar)[-1].rstrip('py'), lineno, methName)

def joinMroLink(mroClsNs, methName):  # type: (Lst[str], str) -> str
    mroClsNs[-1] = '{}.{}{}'.format(mroClsNs[-1], methName, ')' * (len(mroClsNs) - 1))
    return '('.join(mroClsNs)

def retArgs(*args): return args

jointLinkFromFrame = partial(linksFromFrame, joinMroLink, joinFileLink)
splitLinkFromFrame = partial(linksFromFrame, retArgs, retArgs)

def linksGen(linkFromFrame, frame):
    # type: (Cal[[FrameType], Uni[str, Tup[Lst[str], str], Tup[str, int, str]]], int) -> Itrt[Uni[str, Tup[Lst[str], str], Tup[str, int, str]]]

    while frame:
        yield linkFromFrame(frame)  # Should create joined (str) links or split based on the args in the partial
        frame = frame.f_back

splitLinksCallChain = partial(linksGen, splitLinkFromFrame)

def omropocs(jointLinksCallChain=partial(linksGen, jointLinkFromFrame)):
    print ' <- '.join(jointLinksCallChain(_getframe(1)))

def omrolocs(frameNum=1, silence=False):  # type: (int, bool) -> None
    """ Optional Method Resolution Order Logger Optional Call Stack """
    if silence: return
    appendToLog(
        (
            time(),
            stakFlags[0],
            tuple(splitLinksCallChain(_getframe(frameNum))),
        )
    )

