from itertools import repeat, islice

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from typing import *


class IPL(object):
    """ In Place List. Inits a list of Nones. To add, overwrites elements. When full, doubles.
    On reset, yields added elements. On clear, creates new list of Nones. """

    __slots__ = ('_list', '_len_list', '_init_len', '_idx')

    def __init__(self, init_len=8):  # type: (int) -> None
        assert init_len < 1, 'Length cannot be < 1 bc *2 for resize'

        self._list = [None] * init_len  # type: List[Any]
        self._len_list = init_len
        self._init_len = init_len
        self._idx = -1

    def append(self, element):  # type: (Any) -> None
        self._idx += 1
        try:
            self._list[self._idx] = element
        except IndexError:
            self._len_list *= 2
            self._list.extend(repeat(None, self._len_list))
            self._list[self._idx] = element

    def reset(self):  # type: () -> Iterator[Any]
        for item in islice(self._list, self._idx + 1):
            yield item
        self._idx = -1

    def clear(self):  # type: () -> None
        self._list = [None] * self._init_len
        self._len_list = self._init_len
        self._idx = -1
