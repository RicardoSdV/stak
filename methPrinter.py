"""
Call MROpOCS from a method in a new style class to print the name of this class and method from
were its being called from. Also prints a bunch of other related stuff run this file to find out, in python2.7 btw
"""

from inspect import stack


def MROpOCS(allMRO=False, CSD=2):
    frames, clsMethStrs = stack()[1:CSD+1], []

    for frame in frames:
        fLocals, methName = frame[0].f_locals, frame[3]

        Class = fLocals.get('self').__class__ if 'self' in fLocals else None

        if Class is None:
            clsMethStr = methName
        else:
            clsNames, startPrinting = [], False
            for ImroClass in reversed(Class.__mro__):

                print 'ImroClass.__dict__', ImroClass.__dict__
                print 'ImroClass.__name__', ImroClass.__name__

                if any(s.endswith(methName) for s in ImroClass.__dict__):
                    startPrinting = True
                    print 'startPrinting'
                if startPrinting:
                    clsNames.append(ImroClass.__name__)
                    if not allMRO:
                        break
            clsMethStr = '.'.join(clsNames) + '.' + methName
            print

        clsMethStrs.append(clsMethStr)

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


TestDawg().testCallerOfCaller()
