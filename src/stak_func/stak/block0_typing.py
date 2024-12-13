__doc__ = None; """
Holds all names to be used as type hints, & imports all the blocks
such that the only import needed is this one *
"""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import (
        Any,
        Callable  as Cal,
        cast,
        Dict      as Dic,
        Generator as Gen,
        Iterable  as Itrb,
        Iterator  as Itrt,
        List      as Lst,
        Optional  as Opt,
        Sequence  as Seq,
        Set,
        Tuple     as Tup,
        Type      as Typ,
        Union     as Uni,
    )
    from types import CodeType, FrameType
    from datetime import datetime

    # Type Aliases: Use to abbreviate simplicity, not hide complexity.
    PathGen = Cal[[], Itrt[str]]

    OptStr8 = Tup[Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str]]
    OptStr9 = Tup[Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str]]
    OptStr8PlusStr = Tup[Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], Opt[str], str]

    NestedIterable = Uni[Any, Itrb['NestedIterable']]

    Int4 = Tup[int, int, int, int]
    Int6 = Tup[int, int, int, int, int, int]
    Int8 = Tup[int, int, int, int, int, int, int, int]

    Str2 = Tup[str, str]
    Str4 = Tup[str, str, str, str]
    Str9 = Tup[str, str, str, str, str, str, str, str, str]

    None8 = Tup[None, None, None, None, None, None, None, None]
    None9 = Tup[None, None, None, None, None, None, None, None, None]

#### Import logic
    __all__ = locals().keys()
else:
    __all__ = ()
#####################