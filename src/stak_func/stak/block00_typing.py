from time import clock; startTypesImport = clock()

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import os
    from _sre import SRE_Match
    from types import (
        CodeType,
        FrameType,
        ModuleType,
        TracebackType,
    )
    from typing import (
        Any,
        Callable  as Cal,
        Dict      as Dic,
        Deque     as Deq,
        Generator as Gen,
        Iterable  as Itrb,
        Iterator  as Itrt,
        List      as Lst,
        Literal   as Lit,
        Optional  as Opt,
        Sequence  as Seq,
        Set,
        Tuple     as Tup,
        Type      as Typ,
        Union     as Uni,
    )

    # Type Aliases: Use to abbreviate simplicity, not hide complexity.
    OptStr8 = Tup[Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str]]
    OptStr9 = Tup[Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str]]
    OptStr8PlusStr = Tup[Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], str]

    Int4 = Tup[int, int, int, int]
    Int6 = Tup[int, int, int, int, int, int]
    Int7 = Tup[int, int, int, int, int, int, int]
    Int8 = Tup[int, int, int, int, int, int, int, int]

    Str2 = Tup[str, str]
    Str4 = Tup[str, str, str, str]
    Str9 = Tup[str, str, str, str, str, str, str, str, str]

    None8 = Tup[None, None, None, None, None, None, None, None]
    None9 = Tup[None, None, None, None, None, None, None, None, None]

    TraceEvent = Uni[Lit['call'], Lit['line'], Lit['return'], Lit['exception']]

    # Lib types
    App      = Cal[[Any], None]                        # list.append
    Time     = Cal[[], float]                          # time.time
    Clock    = Time                                    # time.clock
    GF       = Cal[[int], FrameType]                   # sys._getframe
    Zip      = Cal[[Itrb, Itrb], Itrt[Tup[Any, Any]]]  # itertools.izip
    IsIns    = Cal[[Any], bool]                        # isinstance
    GetFrame = Cal[[int], FrameType]                   # sys._getframe
    Join     = Cal[[Itrb[str]], str]                   # AnyStr.join

    FileRename = Cal[[str, str], None]                 # os.rename
    PathJoin   = os.path.join

    AnyCls = Typ[Any]

#   splitLink      = (filePath, lineno, mroClsNs or None, calName, strData or None)
    SplitLink      = Tup[str, int, Opt[Tup[str, ...]], str, Opt[Tup[str, str]]]
    SplitLinkTrace = Tup[str, int, Opt[Tup[str, ...]], str, Opt[Tup[str, str]], Opt[int]]

    SplitLinkChain = Tup[SplitLink, ...]

    DataForLogging = Opt[Tup[Tup[str, str], ...]]

#   stakLog = [(unixStamp, splitLinkChain), ...]
    StakLog = Lst[Tup[float, SplitLinkChain]]

#   traceLog = [(unixStamp, traceFlag, splitLink)]
    TraceLog = Deq[Tup[float, str, SplitLink]]

    Self = Cal[[Any], 'Self']

    __all__ = locals().keys()
else:
    __all__ = ()

__all__ += ('clock', )


print '[STAK]', __name__, 'import', clock() - startTypesImport, 's'
