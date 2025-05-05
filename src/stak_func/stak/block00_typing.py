from typing import TYPE_CHECKING


if TYPE_CHECKING:
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

    App = Cal[[Any], None]            # list.append
    Time = Cal[[], float]             # time.time
    GF = Cal[[int], FrameType]        # sys._getframe
    Zip = Cal                         # itertools.izip
    IsIns = Cal[[Any], bool]          # isinstance
    GetFrame = Cal[[int], FrameType]  # sys._getframe

    AnyCls = Typ[Any]

#   splitLink = (filePath, lineno, mroClsNs or None, calName, strData or None)
    SplitLink = Tup[str, int, Opt[Tup[str, ...]], str, Opt[Tup[str, str]]]

#   stakLog = [(unixStamp, splitLink), ...]
    StakLog = Lst[Tup[int, SplitLink]]

    Self = Cal[[Any], 'Self']

    __all__ = locals().keys()
else:
    __all__ = ()