from inspect import stack


def MROpOCS(MRO=True, callStackDepth=999):
    """
    :param MRO: If False will print name of the class in which the method definition lives only. If True it will also
    print this definer class name followed by its descendants following MRO up to the descendant from which the
    method that called MROpOCS was called.

    :param callStackDepth: Just the depth of the call stack to print.
    """

    frames, clsMethStrs = stack()[1:callStackDepth+1], []

    for frame in frames:
        fInfo, methName, clsNames, startPrinting = frame[0], frame[3], [], False; fLocals = fInfo.f_locals

        if 'self' in fLocals:
            revMRO = reversed(fLocals['self'].__class__.__mro__)
        elif 'cls' in fLocals:
            revMRO = reversed(fLocals['cls'].__mro__)
        else:
            fGlobals = fInfo.f_globals
            for val in fGlobals.values():
                if hasattr(val, '__dict__') and methName in val.__dict__ and hasattr(val, '__mro__'):
                    revMRO = reversed(val.__mro__)
                    break
            else:
                revMRO = None

        if revMRO is not None:
            for Class in revMRO:
                if any(s.endswith(methName) for s in Class.__dict__):
                    startPrinting = True
                if startPrinting:
                    clsNames.append(Class.__name__)
                    if not MRO:
                        break

        clsMethStrs.append('.'.join(clsNames) + '.' + methName)

    print ' <- '.join(clsMethStrs)


class TestGanny(object): pass
class TestDaddy(TestGanny):
    def test(self): MROpOCS()
    def __testCaller(self): self.test()
    def testCaller(self): self.__testCaller()
class Test(TestDaddy):
    def testCallerOfCaller(self): self.testCaller()
class TestBro(TestDaddy): pass
class TestDawg(Test): pass

class TestOutcast(object):
    @classmethod
    def classMethTest(cls): TestDawg().testCallerOfCaller()

    @staticmethod
    def statMethTest(): TestOutcast.classMethTest()


def testFunc():
    TestOutcast.statMethTest()


testFunc()
