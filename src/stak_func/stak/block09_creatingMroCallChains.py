from functools import partial
from sys import _getframe
from time import time
from types import FunctionType, ClassType as OldStyleClsType

from .block00_typing import *
from .block03_commonData import omrolocsFlag
from .block05_log import appendToLog
from .block06_pathOps import pathSplitChar
from .block08_flagOps import getSegFlag

# Conditions work even when the class defined __slots__ because we're iterating over the class objects' __dict__
# not the object objects', & as far as I know class objects always have __dict__ even if they declare __slots__


def privInsMethCond(
        defClsMaybe,                                                  # type: AnyCls
        methNameToFindDefClsOf,                                       # type: str
        codeObjToFindDefClsOf,                                        # type: CodeType
        isFunc = partial(isinstance, __class_or_tuple=FunctionType),  # type: IsIns
):                                                                    # type: (...) -> bool
    for attr in defClsMaybe.__dict__.itervalues():
        if (
                isFunc(attr) and
                attr.__name__ == methNameToFindDefClsOf and
                # If the code object is the same do we need to compare the meth name too??
                attr.func_code is codeObjToFindDefClsOf
        ):
            return True
    return False

def pubInsMethCond(
        defClsMaybe,                                             # type: AnyCls
        methNameToFindDefClsOf,                                  # type: str
        codeObjToFindDefClsOf,                                   # type: CodeType
        isProp = partial(isinstance, __class_or_tuple=property)  # type: IsIns
):                                                               # type: (...) -> bool
    if methNameToFindDefClsOf in defClsMaybe.__dict__:
        method = defClsMaybe.__dict__[methNameToFindDefClsOf]
        if isProp(method):
            if method.fget.func_code is codeObjToFindDefClsOf:
                return True
        elif method.func_code is codeObjToFindDefClsOf:
            return True
    return False

def privClsMethCond(
        defClsMaybe,                                                    # type: AnyCls
        methNameToFindDefClsOf,                                         # type: str
        codeObjToFindDefClsOf,                                          # type: CodeType
        isClsMeth = partial(isinstance, __class_or_tuple=classmethod),  # type: IsIns
):                                                                      # type: (...) -> bool
    for attr in defClsMaybe.__dict__.itervalues():
        if (
                isClsMeth(attr)
                and attr.__func__.__name__ == methNameToFindDefClsOf
                and attr.__func__.__code__ is codeObjToFindDefClsOf
        ):
            return True
    return False

def pubClsMethCond(defClsMaybe, methNameToFindDefClsOf, codeObjToFindDefClsOf):  # type: (AnyCls, str, CodeType) -> bool
    if (
            methNameToFindDefClsOf in defClsMaybe.__dict__
            and defClsMaybe.__dict__[methNameToFindDefClsOf].__func__.__code__ is codeObjToFindDefClsOf
    ):
        return True
    return False

def mroClsNsGen(callerCls, defClsCond, methName, codeObj):
    # type: (AnyCls, Cal[[AnyCls, str, CodeType], bool], str, CodeType) -> Itrt[str]
    for cls in callerCls.__mro__:
        yield cls.__name__
        if defClsCond(cls, methName, codeObj):
            return

def linkFromFrame(
        joinMroLinksMaybe,   # type: Cal[[Lst[str], str], Uni[str, Tup[Lst[str], str]]]
        joinFileLinksMaybe,  # type: Cal[[str, int, str], Uni[str, Tup[str, int, str]]]
        frame,               # type: FrameType
):                           # type: (...) -> Uni[SplitLink, str]

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

def joinFileLink(fullPath, lineno, methName, splitChar=pathSplitChar): # type: (str, int, str, str) -> str
    splitPath = fullPath.split(splitChar)
    return '{}{}{}{}.{}'.format(
        splitPath[-2],
        splitChar,
        splitPath[-1].rstrip('py'), # Remove 'py' keep the '.'
        lineno,
        methName,
    )

def joinMroLink(mroClsNs, methName):  # type: (Lst[str], str) -> str
    mroClsNs[-1] = '{}.{}{}'.format(mroClsNs[-1], methName, ')' * (len(mroClsNs) - 1))
    return '('.join(mroClsNs)

def retArgs(*args): return args

jointLinkFromFrame = partial(linkFromFrame, joinMroLink, joinFileLink)  # type: Cal[[FrameType], str]
splitLinkFromFrame = partial(linkFromFrame, retArgs, retArgs)  # type: Cal[[FrameType], Uni[Tup[Lst[str], str], Tup[str, int, str]]]

def makeCallChain(makeLink, frame):
    # type: (Cal[[FrameType], Uni[str, SplitLink]], FrameType) -> Itrt[Uni[str, SplitLink]]

    while frame:
        yield makeLink(frame)  # Should create joined (str) links or split based on the args in the partial
        frame = frame.f_back

def omropocs(
        frame=_getframe,                                   # type: Cal[[int], FrameType]
        getFlag=getSegFlag,                                # type: Cal[[FrameType], str]
        links=partial(makeCallChain, jointLinkFromFrame),  # type: Cal[[FrameType], Itrt[str]]
):                                                         # type: (...) -> None
    """ Optional Method Resolution Order Printer Optional Call Stack """
    frame = frame(1)
    print getFlag(frame) + ': ' +' <- '.join(links(frame))

def omrolocs(
        frameNum=1,                                       # type: int
        callFlag=omrolocsFlag,                            # type: str
        log=appendToLog,                                  # type: App
        now=time,                                         # type: Time
        frame=_getframe,                                  # type: GF
        getFlag=getSegFlag,                               # type: Cal[[FrameType], str]
        links=partial(makeCallChain, splitLinkFromFrame)  # type: Cal[[FrameType], SplitLink]
):                                                        # type: (...) -> None
    """ Optional Method Resolution Order Logger Optional Call Stack """
    frame = frame(frameNum)
    log(
        (now(), getFlag(frame), callFlag, tuple(links(frame)))
    )
