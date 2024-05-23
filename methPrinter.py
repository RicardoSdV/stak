"""
Call MROpOCS from a method in a new style class to print the name of this class and method from
were its being called from. Also prints a bunch of other related stuff run this file to find out, in python2.7 btw
"""

from inspect import stack


def MROpOCS(MroDepth=True, callStackDepth=9999):
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
                if hasattr(val, '__dict__') and methName in val.__dict__:
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
                    if not MroDepth:
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


TestOutcast.statMethTest()
