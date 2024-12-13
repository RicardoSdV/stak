
if __name__ == '__main__':
    import code
    from datetime import datetime
    from itertools import repeat
    from random import randint
    from time import sleep

    from src.funcs.someCode import SomeClass
    from src.stak_func.stak import *

    testingWhat = 'stak'

    if testingWhat == 'stak':
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        class Interface(object):
            def testCallerOfCaller(self): raise NotImplementedError()
        class Ganny(object):
            pass
        class Daddy(Ganny):
            def forMethNameDupBug(self): omrolocs()
            @decorator
            def test(self, someLocalParam=69):
                someOtherLocal = 'yesDaddy'
                omrolocsalad(someDatumForExtraLogging='420')
                somePostOmrolocsaladLocal = 'yes this is post the salad'
                omrolocs()
                data()
                data(someDatum=[1, 2, 3, 4])
                data(someDatum=[1, 2, 3, 4], someDatum2=[1, 2, 3, 4])
                data(pretty=False, someDatum=[1, 2, 3, 4], someDatum2=[1, 2, 3, 4])
                omropocs()
                autoLocals()
                data(SOME_SEPARATOR='================================================================================================')
            @property
            def __privProp(self): return self.test()
            def __testCaller(self): self.__privProp
            def testCaller(self): localVar = 1; self.__testCaller()
        class SomeCls(Daddy, Interface):
            @property
            def propCallerOfCallerOfCaller(self): return self.testCallerOfCaller()
            def testCallerOfCaller(self): self.testCaller()
        class Bro(Daddy):
            pass
        class Dawg(SomeCls):
            pass
        class ParentStatConf(object):
            @staticmethod
            def statMeth(): ParentStatConf.__statMeth()
            @staticmethod
            def __statMeth(): Outcast.classMeth()
        class SomeSomeOtherClassWithSameNameStaticMeth(ParentStatConf):
            @staticmethod
            def statMeth(): pass
        class Outcast(ParentStatConf):
            def __init__(self): self.statMeth()
            @classmethod
            def classMeth(cls): cls.__classMeth()
            @classmethod
            def __classMeth(cls): Dawg().propCallerOfCallerOfCaller
        class SomeOtherClassWithSameNameStaticMeth(ParentStatConf):
            @staticmethod
            def statMeth(): pass
        SomeClass().someMeth()
        class OutcastSon(Outcast):
            pass
        def func():
            OutcastSon()
        class OldStyle:
            @staticmethod
            def oldStyleStaticMeth(): func()
            @classmethod
            def oldStyleClassMeth(cls): cls.oldStyleStaticMeth()
            def oldStyleInstanceMeth(self): self.oldStyleClassMeth()

        def cutOffLogs():
            """
            Assumption: The log may be cutoff but the format won't change, the flag will be a certain min and max number
            of chars, there will be a space and colon before the flag, there will be a colon and space after
            the flag, etc
            """
            return (
                '2024-07-04 13:17:45.269: INFO: [CORRECTLOG] This is a log line which is expected and correct\n',
                '2024-07-04 13:17:45.269: DEBUG: A debug line \n',
                '2024-07-04 13:17:45.269: CRITICAL: Longest expected flag\n',
                '024-07-04 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
                '24-07-04 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
                '4-07-04 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
                '-07-04 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
                '07-04 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
                '7-04 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
                '-04 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
                '04 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
                '4 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
                ' 13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
                '13:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
                '3:17:45.269: CRITICAL: Some flag of the log is cutoff\n',
                ':17:45.269: CRITICAL: Some flag of the log is cutoff\n',
                '17:45.269: CRITICAL: Some flag of the log is cutoff\n',
                '7:45.269: CRITICAL: Some flag of the log is cutoff\n',
                ':45.269: CRITICAL: Some flag of the log is cutoff\n',
                '45.269: CRITICAL: Some flag of the log is cutoff\n',
                '5.269: CRITICAL: Some flag of the log is cutoff\n',
                '.269: CRITICAL: Some flag of the log is cutoff\n',
                '269: CRITICAL: Some flag of the log is cutoff\n',
                '69: CRITICAL: Some flag of the log is cutoff\n',
                '9: CRITICAL: Some flag of the log is cutoff\n',
                ': CRITICAL: Some flag of the log is cutoff\n',
                ' CRITICAL: Some flag of the log is cutoff\n',
                'CRITICAL: Some flag of the log is cutoff\n',
                'RITICAL: Some flag of the log is cutoff\n',
                'ITICAL: Some flag of the log is cutoff\n',
                'TICAL: Some flag of the log is cutoff\n',
                'ICAL: Some flag of the log is cutoff\n',
                'CAL: Some flag of the log is cutoff\n',
                'AL: Some flag of the log is cutoff\n',
                'L: Some flag of the log is cutoff\n',
                ': Some flag of the log is cutoff\n',
                ' Some flag of the log is cutoff\n',
                'Some flag of the log is cutoff\n',
            )
        def genLogs():
            stdLogPaths = ('stdLogA.log', 'stdLogB.log')

            for stdLogPath in stdLogPaths:
                with open(stdLogPath, 'w'): pass

            nonCompromisingLines = (
                'INFO: None compromising logline 68\n',
                'INFO: None compromising logline 67\n',
                'INFO: None compromising logline 66\n',
                'INFO: None compromising logline 65\n',
                'INFO: None compromising logline 64\n',
                'INFO: None compromising logline 63\n',
                'INFO: None compromising logline 419\n',
                'INFO: None compromising logline 418\n',
                'INFO: None compromising logline 417\n',
                'INFO: None compromising logline 416\n',
            )
            maxNonCompLogLines = 53
            maxOmrolocs = 10
            maxSleepTime = 150

            for _ in repeat(None, 40):
                print 'Generating logs'

                for _ in repeat(None, randint(1, maxNonCompLogLines)):
                    with open(stdLogPaths[0], 'a') as f:
                        l1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + ': ' + nonCompromisingLines[randint(0, 5)]
                        f.writelines(l1)
                    with open(stdLogPaths[1], 'a') as f:
                        f.writelines((l1, datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] + ': ' + nonCompromisingLines[randint(0, 9)]))

                for _ in repeat(None, randint(1, maxOmrolocs)):
                    OldStyle().oldStyleInstanceMeth()

                sleep(randint(0, maxSleepTime) / 1000.0)

                with open(stdLogPaths[0], 'a') as f:
                    l1 = 'fdStamp' + ': ' + nonCompromisingLines[randint(0, 5)]
                    f.writelines(l1)

            with open(stdLogPaths[0], 'a') as f:
                f.writelines(cutOffLogs())
            with open(stdLogPaths[1], 'a') as f:
                f.writelines(cutOffLogs())

        def func2():
            a, b = 1, 2
            omrolocsalad()
            data(a=a, b=b)
            autoLocals()
        func2()
        Bro().forMethNameDupBug()

        genLogs()

    elif testingWhat == 'trace':

        def A():
            setTrace()
            B()
            delTrace()
        def B(): C(); E()
        def C(): D()
        def D(): pass
        def E(): F()
        def F(): G()
        def G(): pass

        A()

variables = globals().copy()
variables.update(locals())
shell = code.InteractiveConsole(variables)
shell.interact()