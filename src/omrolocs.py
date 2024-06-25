"""
How to use:
    - Paste STAK class definition and stak = STACK() object instantiation in some high level utils type file
    - Call stak.omrolocs() from any callable to debug, or even a file, anywhere
    - Optionally set the printMRO, adjust the callStackDepth optionally at a global level or by passing the args

Known issues:
    - Caller class cannot be found for wrapped methods and therefore definer class neither (with custom wrappers,
    not @property nor @classmethod, yes @staticmethod but for other reasons)

    - A private property will default to filename & lineno,

    - If the object object autopassed to an instance method is not called 'self' defaults to filename & lineno

    - If the class object autopassed to a class method is not called 'self' defaults to filename & lineno

    - If the method is defined in an old style class, it defaults to filename & lineno

    - The spliceGenerator raises an error if any of the spliced logs is empty, which they normally shouldn't but yeah

Unknown Issues:
    - What happens when the log parser encounters a different format? It will work and return part None links,
    but I think the rest of Stak is not prepared to handle part None links, which, might or might not be worth
    fixing

Cool potential features: (Rule: If I haven't thought that the new potential feature would be practical at least
a couple times when solving real problem abstain from ejaculating it all over this document)

    - If there are multiple methods in the call stack that have the same definer and caller class maybe print only
    one copy of the MRO and substitute in the other frames by ... or something. Actually might need the entire MRO.

    - Support finding caller definer & mro classes for static methods, private properties & wrapped methods

    - Somehow better prints for wrappers, would be cool to have CallerCls(DefinerCls.@decorator.methName)
    but im not sure there is a good way of getting the decorator, only the wrapper

    - Add an option to print the stack in multiple lines with indentation (Seems like this would be better after the fact)

    - wrap long stacks

Working on right now:
    - Add support for time stamping to be able to splice into standard logs

    - Definitions:
        - Trim: A log without the timestamps & some or all log type flags
        - Compress: A log losslessly compressed into a readable format
        - Splice: A combination of two logs based on their time stamps


    - Path ops:
        .STAK <- All logs produced by this class will be found in this dir
            |
            task_dir <- All task specific logs found here
                |
                print_dir <- Tasks require different prints, each print version should have one print_dir
                    |
                    .descr.txt <- Text file that should describe what is being printed in this print_dir
                    |
                    condition_specific_dir <- To solve a task different conditions have to be reproduced, for example,
                    reproduce a bug and then do something similar that doesn't reproduce the bug, since they print the
                    same things they should be found in the same print_dir, but since different things have happened
                    to create said prints they should be in separate log files.
                        |
                        trimNCL1Splice.log
                        |                   <- The NCL.log a program may produce spliced with stak.log & trimmed
                        trimNCL2Splice.log
                        |
                        variants_dir <- Different logs that might be needed only sometimes
                            |
                            NCL1Splice.log
                            |               <- Untrimmed splices (with timestamps, flags & all)
                            NCL2Splice.log
                            |
                            compNCL1.log
                            |           ----|
                            compNCL2.log    | <- Trimmed primitives, no splicing
                            |           ----|
                            compStak.log

                        primitives_dir <- Dir to hold all the data used to create the above logs
                            |
                            stak.log <- stak info by itself with timestamps
                            |
                            NCL1.log
                            |       <- The normal logs but only in the stak.log time period
                            NCL2.log

        Since at the moment calling omrolocs requires modifying the code, and since modifying the code, at the moment
        requires restarting the program, some pathops will be triggered in the __init__


"""

# Imports used outside stak
import code
from datetime import datetime
from itertools import repeat
from random import randint
from time import sleep

from src.funcs.someCode import SomeClass
from typing import Tuple, Optional, List, Union


class STAK(object):
    import shutil; import types; import datetime; import inspect; import time; import os

    def __init__(self):
        self.log = []
        self.omrolocs()

        # Save Settings (cwd == bin paths relative)
        self.__dirRoot     = '.STAK'
        self.__dirTask     = 'task'
        self.__dirPrnt     = 'print'
        self.__dirPrimi    = 'primitives'
        self.__dirVari     = 'variants'
        self.__nameLogStak = 'stak.log'
        self.__namesLogStd = ('stdLogA.log', 'stdLogB.log')

        # Compress settings
        self.maxGroupSize = 100
        self.printTimes = True

        self.__makeDirs()

    """============================================ CAPTURING LOGS PHASE ============================================"""

    def omrolocs(self, callStackDepth=999, silence=False):
        if silence: return
        timeStamp = self.datetime.datetime.now()

        callChain = [
            self.__linkCreator(*frame)
            for frame in self.inspect.stack()[1:callStackDepth]
        ]

        self.log.append(
            (timeStamp, callChain)
        )
    @classmethod
    def __linkCreator(cls, frameObj, filePath, lineNum, methName, _, __):
        """
        self.log = [(timeStamp, callChain), ...]

        callChain = [link1, link2, ...] Every link represents a call or, frame in the inspect.stack

        link = (
            i=0 -> mroClsNs: tuple -> (callerCls, ancestorOfCallerCls, ..., definerCls) if caller & definer found else None
            i=1 -> methName: str
            i=2 -> fileName: str
            i=3 -> lineNum: int
        )

        """
        fLocals = frameObj.f_locals

        callerCls = None
        if 'self' in fLocals:
            callerCls = fLocals['self'].__class__
            defClsCond = cls.__privInsMethCond if cls.__isPrivate(methName) else cls.__pubInsMethCond
        elif 'self' in fLocals:
            callerCls = fLocals['self']
            defClsCond = cls.__privClsMethCond if cls.__isPrivate(methName) else cls.__pubClsMethCond

        if callerCls is None or isinstance(callerCls, cls.types.ClassType):
            link = (None, methName, filePath.split('\\')[-1], lineNum)
        else:
            mroClsNs = list(cls.__mroClsNsGenerator(callerCls, defClsCond, methName, frameObj.f_code))
            if mroClsNs[-1] == 'object':
                mroClsNs = None
            link = (mroClsNs, methName, filePath.split('\\')[-1], lineNum)

        return link
    @staticmethod
    def __mroClsNsGenerator(callerCls, defClsCond, methName, fCode):
        for cls in callerCls.__mro__:
            yield cls.__name__
            if defClsCond(cls, methName, fCode):
                return
    @staticmethod
    def __privInsMethCond(cls, methName, fCode):
        for attr in cls.__dict__.values():
            if (
                isinstance(attr, STAK.types.FunctionType)
                and attr.__name__ == methName
                and attr.func_code is fCode
            ):
                return True
        return False
    @staticmethod
    def __pubInsMethCond(cls, methName, fCode):
        if methName in cls.__dict__:
            method = cls.__dict__[methName]

            if isinstance(method, property):
                if method.fget.func_code is fCode:
                    return True
            elif method.func_code is fCode:
                return True
        return False
    @staticmethod
    def __privClsMethCond(cls, methName, fCode):
        for attr in cls.__dict__.values():
            if (
                isinstance(attr, classmethod)
                and attr.__func__.__name__ == methName
                and attr.__func__.__code__ is fCode
            ):
                return True
        return False
    @staticmethod
    def __pubClsMethCond(cls, methName, fCode):
        if (
            methName in cls.__dict__
            and cls.__dict__[methName].__func__.__code__ is fCode
        ):
            return True
        return False
    @staticmethod
    def __isPrivate(methName):
        return methName.startswith('__') and not methName.endswith('__')

    """=============================================================================================================="""

    """============================================= SAVING LOGS PHASE =============================================="""

    def save(self):
        start = self.time.time()

        callChainsWithStrLinks = [(timeStamp, list(self.__strLinkGen(callChain))) for timeStamp, callChain in self.log]
        doneCallChainsWithStrLinks = self.time.time()

        self.__saveRawStakLogToPrimitives(callChainsWithStrLinks)
        done__saveRawStakLogToPrimitives = self.time.time()

        stdLogsInStakPeriod = self.__parseStdLogs()
        doneStdLogsInStakPeriod = self.time.time()

        self.__saveStdLogsInStakPeriodToPrimitives(stdLogsInStakPeriod)
        done__saveStdLogsInStakPeriodToPrimitives = self.time.time()

        callChainsWithCompressedStrLinks = self.__compressLinks(callChainsWithStrLinks)  # type: List[Tuple[datetime, str]]
        doneCallChainsWithCompressedStrLinks = self.time.time()

        splicedLogs = self.__saveSplicedToVariants(stdLogsInStakPeriod, callChainsWithCompressedStrLinks)
        doneSplicedLogs = self.time.time()

        self.__saveCompressedSplicedLogs(splicedLogs)
        done__saveCompressedSplicedLogs = self.time.time()

        self.__saveCompressedStakLogToVariants(callChainsWithCompressedStrLinks)
        done__saveCompressedStakLogToVariants = self.time.time()

        self.__printTimes(start, doneCallChainsWithStrLinks, done__saveRawStakLogToPrimitives, doneStdLogsInStakPeriod,
                          done__saveStdLogsInStakPeriodToPrimitives, doneCallChainsWithCompressedStrLinks,
                          doneSplicedLogs, done__saveCompressedSplicedLogs, done__saveCompressedStakLogToVariants
                          )
    def __saveRawStakLogToPrimitives(self, callChainsWithStrLinks):
        with open(
                self.__ifPathExistsIncSuffix(
                    self.__pathLogStak
                ), 'w'
        ) as f:
            f.writelines(
                (self.__stakChainLinker(*el)
                 for el in callChainsWithStrLinks)
            )
    @classmethod
    def __stakChainLinker(cls, timeStamp, callChainWithStrLinks):
        return cls.__stampToStr(timeStamp) + ': ' + ' <- '.join(callChainWithStrLinks) + '\n'
    @staticmethod
    def __strLinkGen(callChain):
        for mroClsNs, methName, fileName, lineNum in callChain:
            if mroClsNs is None:
                yield fileName.replace('.py', str(lineNum)) + '.' + methName
            else:
                mroClsNs = mroClsNs[:]
                mroClsNs[-1] = mroClsNs[-1] + '.' + methName + ')' * (len(mroClsNs) - 1)
                yield '('.join(mroClsNs)
    def __parseStdLogs(self):  # type: () -> List[List[Tuple[Optional[datetime], Optional[str], str]]]
        """ stdLogs = [parsedLines = [(timeStamp, logType, lineStr), ...], ...] """

        def splitTimeStampAndLogTypeFromLine(line):  # type: (str) -> Tuple[Optional[datetime], Optional[str], str]
            colonCnt, timeStrEndI, typeFlagEndI, timeStamp, typeFlag = 0, 0, 0, None, None
            for i, char in enumerate(line):
                if char == ':':
                    colonCnt += 1

                    if colonCnt == 3:
                        timeStamp = datetime.strptime(line[:i], '%Y-%m-%d %H:%M:%S.%f')
                        timeStrEndI = i

                    elif colonCnt == 4:
                        typeFlagEndI = i + 2
                        typeFlag = line[timeStrEndI: typeFlagEndI]
                        line = line[typeFlagEndI:]
                        break

                if i > 34:
                    break

            return timeStamp, typeFlag, line

        def parsedLinesGenerator(lines, start, end):
            started = False
            for line in lines:
                timeStamp, typeFlag, line = splitTimeStampAndLogTypeFromLine(line)

                if timeStamp is not None:
                    if not started:
                        if timeStamp >= start:
                            started = True
                    elif timeStamp >= end:
                        break

                if started:
                    yield timeStamp, typeFlag, line

        def parsedLogCreator(path, period):
            with open(path, 'r') as f:
                lines = f.readlines()
            return list(parsedLinesGenerator(lines, *period))

        return [
            parsedLogCreator(path, self.__stakPeriod)
            for path in self.__namesLogStd
        ]
    def __saveStdLogsInStakPeriodToPrimitives(self, stdLogs):

        for log, logName in zip(stdLogs, self.__namesLogStd):
            path = self.__ifPathExistsIncSuffix(
                self.os.path.join(
                    self.__pathDirPrimi, logName
                )
            )

            with open(path, 'w') as f:
                f.writelines(
                    (
                        self.__stdLogLineCreator(*el)
                        for el in log
                    )
                )
    @classmethod
    def __stdLogLineCreator(cls, timeStamp, typeFlag, line): return cls.__stampToStr(timeStamp) + typeFlag + line
    def __saveSplicedToVariants(self, stdLogs, stakLog):

        def spliceGenerator(stdLog, stakLog):
            stdI, stakI, stdElLeft, stakElLeft, lenStd, lenStak = 0, 0, True, True, len(stdLog), len(stakLog)

            stdTimeStamp,  stdTypeFlag,  stdLine   = stdLog[stdI]
            stakTimeStamp,               callChain = stakLog[stakI]

            while stdElLeft or stakElLeft:

                if stdElLeft is True and (stdTimeStamp <= stakTimeStamp or stakElLeft is False):
                    yield stdTimeStamp, stdTypeFlag, stdLine
                    stdI += 1
                    if stdI == lenStd:
                        stdElLeft = False
                    else:
                        stdTimeStamp, stdTypeFlag, stdLine = stdLog[stdI]

                if stakElLeft is True and (stdTimeStamp > stakTimeStamp or stdElLeft is False):
                    yield stakTimeStamp, callChain
                    stakI += 1
                    if stakI == lenStak:
                        stakElLeft = False
                    else:
                        stakTimeStamp, callChain = stakLog[stakI]
            return

        def jointGenerator(splicedLog):
            for line in splicedLog:
                if len(line) == 3:
                    yield self.__stdLogLineCreator(*line)
                else:
                    yield self.__stampToStr(line[0]) + ': ' + line[-1]
            return

        splicedLogs = []
        for stdLog, logName in zip(stdLogs, self.__namesLogStd):
            path = self.__ifPathExistsIncSuffix(
                self.os.path.join(
                    self.__pathDirVari, self.__addSuffix(logName, 'Splice')
                )
            )

            splicedLog = list(spliceGenerator(stdLog, stakLog))
            splicedLogs.append(splicedLog)

            with open(path, 'w') as f:
                f.writelines(jointGenerator(splicedLog))

        return splicedLogs
    def __saveCompressedStakLogToVariants(self, callChainsWithCompressedStrLinks):
        with open(
                self.__ifPathExistsIncSuffix(
                    self.os.path.join(
                        self.__pathDirVari, 'stakCompress.log')
                ),
                'w'
        ) as f:
            f.writelines(
                self.__compressLines(
                    [line for stamp, line in callChainsWithCompressedStrLinks]
                )
            )
    def __saveCompressedSplicedLogs(self, splicedLogs):
        # type: (List[List[Union[Tuple[datetime, str], Tuple[datetime, str, str]]]]) -> None

        for log, name in zip(splicedLogs, self.__namesLogStd):

            with open(
                    self.__ifPathExistsIncSuffix(
                        self.os.path.join(
                            self.__pathDirPrint, name
                        )
                    ), 'w'
            ) as f:
                f.writelines(
                    self.__compressLines(
                        [el[-1] for el in log]
                    )
                )
    @property
    def __stakPeriod(self): return self.log[0][0], self.log[-1][0]
    @staticmethod
    def __stampToStr(timeStamp): return timeStamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    """=============================================================================================================="""

    """================================================= COMPRESSION ================================================"""

    class CompressionFormatList(list):
        """ List that holds extra attributes for internal use in compression"""
        def __init__(self, cnt=1, rep='', *args):
            super(STAK.CompressionFormatList, self).__init__(args)
            self.cnt = cnt
            self.rep = rep
    def __compressLinks(self, callChainsWithStrLinks):
        return [
            (
                timeStamp,
                self.__prettyfyLine(
                    self.__compress(
                        self.CompressionFormatList(1, 'line', *callChain)
                    )
                ).rstrip(' <- ') + '\n'
            )
            for timeStamp, callChain in callChainsWithStrLinks
        ]
    def __compressLines(self, lines):  # type: (List[str]) -> List[str]
        return  self.__prettyfyLines(
                    self.__compress(
                        self.__formatLinesForLinesCompression(
                            lines
                        )
                    )
                )
    @classmethod
    def __prettyfyLine(cls, lineCfl):
        result = ''

        if lineCfl.cnt > 1:
            result += '{}x['.format(lineCfl.cnt)

        for el in lineCfl:
            if isinstance(el, cls.CompressionFormatList):
                assert el.rep == 'line'
                result += cls.__prettyfyLine(el)
            elif isinstance(el, str):
                result += (el + ' <- ')
            else:
                raise TypeError('Wrong type in compressed stack: type(el)', type(el))

        if lineCfl.cnt > 1:
            result = result.rstrip(' <- ')
            result += (']' + ' <- ')

        return result
    @classmethod
    def __prettyfyLines(cls, lines_cfl, depth=0):
        indent = depth * '    '
        result = []

        if lines_cfl.cnt > 1:
            result.append('{}{}x\n'.format((depth - 1) * '    ', lines_cfl.cnt))

        for el in lines_cfl:
            if isinstance(el, cls.CompressionFormatList):
                assert el.rep == 'lines'
                result.extend(cls.__prettyfyLines(el, depth + 1))
            elif isinstance(el, str):
                result.append(indent + el)
            else:
                raise TypeError('Wrong type in compressed list: type(el)', type(el))
        return result
    @classmethod
    def __formatLinesForLinesCompression(cls, lines):
        if not lines[-1].endswith('\n'):
            lines[-1] += '\n'
        return cls.CompressionFormatList(1, 'lines', *lines)
    def __compress(self, postPassCfl):
        represents = postPassCfl.rep

        for groupSize in range(1, min(len(postPassCfl) // 2, self.maxGroupSize)):

            prePassCfl = postPassCfl
            postPassCfl = self.CompressionFormatList(cnt=prePassCfl.cnt, rep=prePassCfl.rep)

            thisGroupStartI = 0
            thisGroupEndI = groupSize - 1

            nextGroupStartI = groupSize
            nextGroupEndI = 2 * groupSize - 1

            thisGroup = prePassCfl[thisGroupStartI: thisGroupEndI + 1]
            nextGroup = prePassCfl[nextGroupStartI: nextGroupEndI + 1]

            groups_cnt = 1

            while thisGroup:

                if thisGroup == nextGroup:
                    groups_cnt += 1

                    nextGroupStartI += groupSize
                    nextGroupEndI += groupSize

                else:
                    if groups_cnt == 1:
                        postPassCfl.append(thisGroup[0])

                        thisGroupStartI += 1
                        thisGroupEndI += 1

                        nextGroupStartI += 1
                        nextGroupEndI += 1

                    else:  # There has been one or more repetitions of thisGroup

                        compressed_group = self.CompressionFormatList(groups_cnt, represents, *thisGroup)
                        postPassCfl.append(compressed_group)

                        thisGroupStartI = nextGroupStartI
                        thisGroupEndI = nextGroupEndI

                        nextGroupStartI += groupSize
                        nextGroupEndI += groupSize

                        groups_cnt = 1

                thisGroup = prePassCfl[thisGroupStartI: thisGroupEndI + 1]
                nextGroup = prePassCfl[nextGroupStartI: nextGroupEndI + 1]

        return postPassCfl
    def __printTimes(self, start, doneCallChainsWithStrLinks, done__saveRawStakLogToPrimitives, doneStdLogsInStakPeriod,
                     done__saveStdLogsInStakPeriodToPrimitives, doneCallChainsWithCompressedStrLinks, doneSplicedLogs,
                     done__saveCompressedSplicedLogs, done__saveCompressedStakLogToVariants
                     ):
        if not self.printTimes: return
        print 'CallChainsWithStrLinks', doneCallChainsWithStrLinks - start
        print '__saveRawStakLogToPrimitives', done__saveRawStakLogToPrimitives - doneCallChainsWithStrLinks
        print 'StdLogsInStakPeriod', doneStdLogsInStakPeriod - done__saveRawStakLogToPrimitives
        print '__saveStdLogsInStakPeriodToPrimitives', done__saveStdLogsInStakPeriodToPrimitives - doneStdLogsInStakPeriod
        print 'CallChainsWithCompressedStrLinks', doneCallChainsWithCompressedStrLinks - done__saveStdLogsInStakPeriodToPrimitives
        print 'SplicedLogs', doneSplicedLogs - doneCallChainsWithCompressedStrLinks
        print '__saveCompressedSplicedLogs', done__saveCompressedSplicedLogs - doneSplicedLogs
        print '__saveCompressedStakLogToVariants', done__saveCompressedStakLogToVariants - done__saveCompressedSplicedLogs
        print 'totalTime: ', done__saveCompressedStakLogToVariants - start

    """=============================================================================================================="""

    """=================================================== PATH OPS ================================================="""

    def changePath(self, prnt=None, task=None, prim=None, vari=None, root=None, stdLogs=None):
        """ Can live change paths, new dirs are created if don't exist """
        if prnt is not None:    self.__dirPrnt     = prnt
        if task is not None:    self.__dirTask     = task
        if prim is not None:    self.__dirPrimi    = prim
        if vari is not None:    self.__dirVari     = vari
        if root is not None:    self.__dirRoot     = root
        if stdLogs is not None: self.__namesLogStd = stdLogs

        self.__makeDirs()
    def rmPrint(self):
        """ DANGER: Removes current print directory & all its logs """
        self.shutil.rmtree(self.__pathDirPrint)
        self.__makeDirs()
    def clearLogs(self):
        """ Clears current logs, stak & std """

        for logPath in self.__namesLogStd:
            with open(logPath, 'w'): pass

        self.log[:] = []
    def __makeDirs(self):

        if not self.os.path.isdir(self.__pathDirPrimi):
            self.os.makedirs(self.__pathDirPrimi)

        if not self.os.path.isdir(self.__pathDirVari):
            self.os.makedirs(self.__pathDirVari)
    @classmethod
    def __addSuffix(cls, logName, suffix):
        name, ext = cls.os.path.splitext(logName)
        return '{}{}{}'.format(name, suffix, ext)
    @classmethod
    def __ifPathExistsIncSuffix(cls, path):
        fileName, ext = cls.os.path.splitext(
            cls.os.path.basename(path)
        )
        dirPath = cls.os.path.dirname(path)
        cnt = 0

        while cls.os.path.isfile(path):
            cnt += 1
            path = cls.os.path.join(
                dirPath, '{}{}{}'.format(fileName, cnt, ext)
            )

        return path
    @property
    def __pathDirPrint(self): return self.os.path.join(self.__dirRoot, self.__dirTask, self.__dirPrnt)
    @property
    def __pathDirPrimi(self): return self.os.path.join(self.__pathDirPrint, self.__dirPrimi)
    @property
    def __pathDirVari(self):  return self.os.path.join(self.__pathDirPrint, self.__dirVari)
    @property
    def __pathLogStak(self):  return self.os.path.join(self.__pathDirPrimi, self.__nameLogStak)

    """=============================================================================================================="""

stak = STAK()


def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

class Interface(object):
    def testCallerOfCaller(self): raise NotImplementedError()
class Ganny(object): pass
class Daddy(Ganny):
    @decorator
    def test(self): stak.omrolocs()
    @property
    def __privProp(self): return self.test()
    def __testCaller(self): self.__privProp
    def testCaller(self): localVar = 1; self.__testCaller()
class SomeCls(Daddy, Interface):
    @property
    def propCallerOfCallerOfCaller(self): return self.testCallerOfCaller()
    def testCallerOfCaller(self): self.testCaller()
class Bro(Daddy): pass
class Dawg(SomeCls): pass
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
class OutcastSon(Outcast): pass
def func(): OutcastSon()

class OldStyle:
    @staticmethod
    def oldStyleStaticMeth(): func()
    @classmethod
    def oldStyleClassMeth(cls): cls.oldStyleStaticMeth()
    def oldStyleInstanceMeth(self): self.oldStyleClassMeth()


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

        sleep(randint(0, maxSleepTime)/1000.0)

genLogs()
variables = globals().copy()
variables.update(locals())
shell = code.InteractiveConsole(variables)
shell.interact()


















































# end
