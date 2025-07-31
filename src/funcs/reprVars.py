"""

if (isClass and (traverseMro or not hasDict)) or (not isClass and (traverseMRO or not hasSlots)):
    use dir()

if isClass and not traverseMRO and hasDict:
    use vars()

if not isClass and hasSlots:
    use slots

"""
from itertools import chain
from traceback import print_exc
from types import ClassType, MemberDescriptorType


# TODO: Maybe not for stak specifically, but sometimes you need to override certain attrs
#  to make the reprs more readable, and so there must be a system to override sometimes
def reprAll(
        obj,
        includeProtected=True,
        includePrivate=True,
        includeDunder=False,
        includeCallable=False,
        traverseMRO=True,
        failLoud=True,
):
    """ Returns a string with the className(attrName=attrVal, ...)
    falls back on repr(). """

    try:
        isClass = isinstance(obj, (type, ClassType))
        hasDict = hasattr(obj, '__dict__')
        className = obj.__name__ if isClass else obj.__class__.__name__

        insClass = obj if isClass else obj.__class__

        if traverseMRO:
            MRO = [_class for _class in insClass.__mro__ if _class is not object]
        else:
            MRO = (insClass, )

        if len(MRO) == 1:
            traverseMRO = False

        mangledPrefixes = [
            '_' + _class.__name__.lstrip('_')
            for _class in MRO
        ]

        res = [className, '(']
        app = res.append

        # Use slots when it's an instance, and it has slots:
        # -------------------------------------------------------------------------
        if not isClass and hasattr(obj, '__slots__'):
            for mangledPrefix in mangledPrefixes:
                lenMangledPrefix = len(mangledPrefix)

                # TODO: This is broken, do only one dict in total.
                slots = getattr(insClass, '__slots__', ())
                if hasDict and '__dict__' not in slots:
                    slots = chain(slots, ('__dict__', ))

                for name in slots:
                    isFunder = name[:2] == '__'
                    isDunder = isFunder and name[-2:] == '__'

                    if isDunder:
                        # Always include __dict__ if __slots__ have dict.
                        if not includeDunder and not name == '__dict__':
                            continue

                    elif isFunder:
                        if includePrivate:
                            mangledName = mangledPrefix + name
                            val = getattr(obj, mangledName, 'Not Initialised')
                            if traverseMRO:
                                name = mangledName
                            app('%s=%r, ' % (name, val))
                        continue

                    elif name[:1] == '_':
                        if not includeProtected:
                            continue

                    val = getattr(obj, name, 'Not Initialised')
                    if not includeCallable and callable(val):
                        continue

                    if not traverseMRO and isFunder and not isDunder:
                        name = name[lenMangledPrefix:]

                    app('%s=%r, ' % (name, val))
        # -------------------------------------------------------------------------

        # Use vars(), only for classes when not traversing MRO, this is
        # why the name can be demangled without collisions.
        # -------------------------------------------------------------------------
        elif isClass and hasDict and not traverseMRO:

            for mangledPrefix in mangledPrefixes:
                lenMangledPrefix = len(mangledPrefix)

                for name, val in vars(obj).iteritems():
                    if not includeCallable and callable(val):
                        continue

                    if name.startswith(mangledPrefix):
                        if not includePrivate:
                            continue

                        name = name[lenMangledPrefix:]

                    elif name[:2] == '__' and name[-2:] == '__':
                        if not includeDunder:
                            continue

                    elif name[:1] == '_':
                        if not includeProtected:
                            continue

                    if isinstance(val, MemberDescriptorType):
                        continue

                    app('%s=%r, ' % (name, val))
        # -------------------------------------------------------------------------


        # Use dir(), as a fallback for C classes which can, not have slots nor dict
        # but dir() still works, and also when traversing MROs and, it's not an instance
        # with slots, because slots don't include callables so its mostly more accurate.
        # -------------------------------------------------------------------------
        else:
            for name in dir(obj):
                if name[:2] == '__' and name[-2:] == '__':
                    if not includeDunder:
                        continue

                else:
                    startsWith = name.startswith
                    for prefix in mangledPrefixes:
                        if startsWith(prefix):
                            isPrivate = True
                            break
                    else:
                        isPrivate = False

                    if isPrivate:
                        if not includePrivate:
                            continue

                    elif name[1:] == '_':
                        if not includeProtected:
                            continue

                val = getattr(obj, name, 'Not Found')
                if not includeCallable and callable(val):
                    continue

                if isinstance(val, MemberDescriptorType):
                    continue

                app('%s=%r, ' % (name, val))
        # -------------------------------------------------------------------------

        if len(res) == 2:  # Nothing found
            return repr(obj)

        res[-1] = res[-1][:-2]
        app(')')
        return ''.join(res)

    except Exception as e:
        if failLoud:
            print_exc()
            raise e
        return repr(obj)


class NewA(object):
    ca, _cb, __cc = 1, 2, 3
    def __init__(self):
        self.ia, self._ib, self.__ic = 4, 5, '6'

    def pubMethA(self): return
    def _protMethA(self): return
    def __privMethA(self): return

class NewB(NewA):
    cd, _ce, __cc = 7, 8, 9

    def __init__(self):
        super(NewA, self).__init__()
        self.id, self._ie, self.__ic = 10, 11, '12'

    def pubMethB(self): return
    def _protMethB(self): return
    def __privMethB(self): return


class SlotsA(object):
    ca, _cb, __cc = 1, 2, 3

    __slots__ = ('ia', '_ib', '__ic',)

    def __init__(self):
        self.ia, self._ib, self.__ic = 4, 5, '6'

    def pubMethA(self): return
    def _protMethA(self): return
    def __privMethA(self): return

class SlotsB(SlotsA):
    cd, _ce, __cc = 7, 8, 9

    __slots__ = ('id', '_ie', '__ic',)

    def __init__(self):
        super(SlotsB, self).__init__()
        self.id, self._ie, self.__ic = 10, 11, '12'

    def pubMethB(self): return
    def _protMethB(self): return
    def __privMethB(self): return

class SlotsAndDict(SlotsB):

    def __init__(self):
        super(SlotsAndDict, self).__init__()
        self.iF, self._ig, self.__ic = 13, 14, '15'


newA = NewA()
newB = NewB()

slotsA = SlotsA()
slotsB = SlotsB()

slotsAndDict = SlotsAndDict()

print 'NewA', reprAll(NewA)
print 'newA', reprAll(newA)
print
print 'NewB', reprAll(NewB)
print 'newB', reprAll(newB)
print
print 'SlotsA', reprAll(SlotsA)
print 'slotsA', reprAll(slotsA)
print
print 'SlotsB', reprAll(SlotsB)
print 'slotsB', reprAll(slotsB)
print
print 'SlotsAndDict', reprAll(SlotsAndDict)
print 'slotsAndDict', reprAll(slotsAndDict)

