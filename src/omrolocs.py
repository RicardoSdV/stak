"""
How to use:
    - Paste STAK class definition and stak = STACK() object instantiation in some high level utils type file
    - Call stak.omrolocs() from any callable to debug, or even a file, anywhere
    - Optionally set the printMRO, adjust the callStackDepth optionally at a global level or by passing the args

Known issues:
    - Caller class cannot be found for wrapped methods & therefore definer class neither (with custom wrappers,
    not @property nor @classmethod, yes @staticmethod but for other reasons)

    - A private property will default to filename & lineno,

    - If the object object autopassed to an instance method is not called 'self' defaults to filename & lineno

    - If the class object autopassed to a class method is not called 'cls' defaults to filename & lineno

    - If the method is defined in an old style class, it defaults to filename & lineno

    - The spliceGenerator raises an error if any of the spliced logs is empty, which they normally shouldn't but yeah

    - The __log parser needs to be way more robust, can't rely on standard line formats because typing in the console
    messes with __log lines for some reason. (This is kind of solved but the solution sucks)

    - Due to the compression algorith some, potentially more profitable patterns, are lost e.g. A, A, A, B, A, B -> 3A, BAB

Unknown Issues:
    - If the game crashes I think there might be a problem, depending on how bad the crash.
        Possible solution: would be to add an option to either save then logs every so often, or ideally run this
        entire thing in a separate process which never crashes which I don't even know if possible


Cool potential features: (Rule: If I haven't thought that the new potential feature would be practical at least
a couple times when solving real problem abstain from ejaculating it all over this document)

    - If there are multiple methods in the call stack that have the same definer and caller class maybe print only
    one copy of the MRO and substitute in the other frames by ... or something. Actually might need the entire MRO. Why? wtf explain yourself

    - Support finding caller definer & mro classes for static methods, private properties & wrapped methods

    - Somehow better prints for wrappers, would be cool to have CallerCls(DefinerCls.@decorator.methName)
    but im not sure there is a good way of getting the decorator, only the wrapper

        The concept of closures & this function may or may not help
        def identify_function(func):
            if func.func_name == 'onCollect' and func.func_closure:
                closure_vars = {cell.cell_contents for cell in func.func_closure}
                return closure_vars


    - Add an option to print the stack in multiple lines with indentation (Seems like this would be better after the fact)

    - wrap long stacks

    - Print data structures automatically with wraparound & optionally formatting:
        - This would require adding __log flags to distinguish [STAK] from [PDS] or whatever, not to actually print them
        because who cares, but to distinguish in code, which could be inferred, but that's more complicated & less
        flexible in case other types of entries are added.

        - Also the wrapper method could be used to wrap every type of __log entry

        - The problem is that formatting random string datastructures is a pain, & limiting. Therefore, the actual
        datastructure should be formatted, which, brings some problems, either do it live, which brings the problem
        of not knowing if the datastructure needs formatting or not & speed, or, keeping a deep copy of the structure,
        which also brings issues, since objects in it should be copyable which we cannot guarantee. So, a potential
        solution would be to have a copy of the simple stuff in the structure, & a string of the complex stuff, for
        example:
        [1,2,3,{we call the __repr__ of the object & store the string, or whatever we want to call like func.__name__}]

    - Time stamps:
        - Re-introduce stamps in compressed logs.
        - Given that stamps are mostly the same, just log the parts that change

        for example:

            2024-07-02 20:23:52.903:
            3x
                None compromising logline 66
            None compromising logline 67

Working on right now:
    - make the commands one letter and properties, tiered of typing (maybe it's hard to remember one letter commands,
    maybe three letter commands is the sweet spot, maybe rare commands should be longer, common commands shorter)

    - Adding __log flags to stak.__log


Some details:
    - Definitions:
        - Trim: A __log without the timestamps & some or all __log type flags
        - Compress: A __log losslessly compressed into a readable format
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
                    to create said prints they should be in separate __log files.
                        |
                        trimNCL1Splice.__log
                        |                   <- The NCL.__log a program may produce spliced with stak.__log & trimmed
                        trimNCL2Splice.__log
                        |
                        variants_dir <- Different logs that might be needed only sometimes
                            |
                            NCL1Splice.__log
                            |               <- Untrimmed splices (with timestamps, flags & all)
                            NCL2Splice.__log
                            |
                            compNCL1.__log
                            |           ----|
                            compNCL2.__log    | <- Trimmed primitives, no splicing
                            |           ----|
                            compStak.__log

                        primitives_dir <- Dir to hold all the data used to create the above logs
                            |
                            stak.__log <- stak info by itself with timestamps
                            |
                            NCL1.__log
                            |       <- The normal logs but only in the stak.__log time period
                            NCL2.__log

        Since at the moment calling omrolocs requires modifying the code, and since modifying the code, at the moment
        requires restarting the program, some pathops will be triggered in the __init__


"""

# Imports used outside stak
import code
from datetime import datetime
from itertools import repeat
from random import randint
from time import sleep
from types import CodeType

from src.funcs.someCode import SomeClass
from typing import Tuple, Optional, List, Union, Iterator, Type, Any, Callable


# Types are defined outside the class since they are not necessary for running STAK, only for readability

# Something is considered a log line when it is a string which ends in \n otherwise it is a log entry

# Directory & file names & paths -------------------------------------------------------------------------------

StakRootDirName = str  # All logs generated by STAK
TaskDirName     = str  # Logs pertinent to a specific task, e.g. fixing a bug
PrintDirName    = str  # Logs that print the same things, but in different circumstances

PrimitivesDirName = str  # Holds representations of data used to create trimmed, spliced and/or compressed logs
VariantsDirName   = str  # The logs which have had some combination of the transforms applied

FileName = str  # Ends in file extension, e.g. '.log' but contains no dirs, i.e. it's not a filePath

StdLogFileName  = FileName  # Name of a log file which holds the logs normally produced by the app
StdLogFileNames = Tuple[StdLogFileName, ...]  # None or more standard log file names

StrFilePath     = str          # Relative path to a file created with os.path.join()
NoExistFilePath = StrFilePath  # A StrFilePath which known to not exist yet

StrDirPath = str  # Relative path to a dir created with os.path.join()
StrPathToPrintDir = StrDirPath
StrPathToPrimitivesDir = StrDirPath
StrPathToVariantsDir = StrDirPath
StrFilePathToStakLogPrimitive = StrDirPath

# ---------------------------------------------------------------------------------------------------------------

# Types of log lines
Line           = str  # A normal string that will become one or more lines in a log therefore ends in /n
StdLogLine     = str  # A line as found in the std logs, with time stamp, flags, etc.
StampedLine    = str  # Starts with a time stamp, contains flags, ends with \n
ProbParsedLine = str  # Probably time stamp & flag is trimmed, maybe not when parsing fails
ProbJoinedLine = str  # Probably rejoined parsed line, maybe not when parsing fails TODO: Reconsider interpolating stamp to avoid all these probs

# Components of a split link call chain
LineNum    = int  # Line number where the call to the callable can be found
CallerFile = str  # File where the call to this callable can be found TODO: Settle if this should be the abs filePath the name some part of the filePath or what
MethName   = str  # Callable name whose call triggered the creation of its link
ClassName  = str  # Name of a class
MroClsNs = List[ClassName]  # Method Resolution Order from caller to definer if definer found, else definer = object
SplitLink = Tuple[Optional[MroClsNs], MethName, CallerFile, LineNum]
SplitLinkCallChain = List[SplitLink]

# Components of a string link call chain
StrLink = str  # String links should end in \n since they are considered one or more log lines
StrLinkCallChain = List[StrLink]

# Components of different types of log entries
LogFlag = str
TimeStamp = datetime
SplitLinkCallChainEntry = Tuple[TimeStamp, LogFlag, SplitLinkCallChain]
StrLinkCallChainEntry   = Tuple[TimeStamp, LogFlag, StrLinkCallChain]
ParsedStdLogEntry       = Tuple[Optional[TimeStamp], Optional[LogFlag], ProbParsedLine]

# Log types including intermediate
CaptureReceptiveLog  = List[SplitLinkCallChainEntry]
StrLinkCallChainsLog = List[StrLinkCallChainEntry]
ParsedStdLog         = List[ParsedStdLogEntry]

ParsedStdLogs = List[ParsedStdLog]

ClassObject = Type[Any]
WasDefinerClsFound = bool
DefClsCond = Callable[[ClassObject, MethName, CodeType], WasDefinerClsFound]


class STAK(object):
    import time as __ti; import os as __os; from types import ClassType as __OldStyleClsType
    from datetime import datetime as __dt; from shutil import rmtree as __rmtree
    from sys import _getframe as __getFrame; from types import FunctionType as __FunctionType


    __slots__ = (  # Slots so that __weakref__ & __dict__ don't appear when calling help()
        '__log', '__dirRoot', '__dirTask', '__dirPrnt', '__dirPrimi', '__dirVari', '__nameLogStak',
        '__namesLogStd', '__maxGroupSize', '__isPrintingTimes', '__eventCnt', '__eventLabels'
    )

    def __init__(self):  # type: () -> None
        # Many attrs are private so they don't appear on help(stak), however, some can be changed live,
        # if a method exists to change them indirectly it should be used, otherwise probably not.

        self.__log = []  # type: CaptureReceptiveLog
        self.omrolocs()

        # Save Settings (cwd == bin, paths relative)
        self.__dirRoot     = '.STAK'
        self.__dirTask     = 'task'
        self.__dirPrnt     = 'print'
        self.__dirPrimi    = 'primitives'
        self.__dirVari     = 'variants'
        self.__nameLogStak = 'stak.log'
        self.__namesLogStd = ('stdLogA.log', 'stdLogB.log')

        # Compress settings
        self.__maxGroupSize = 100  # Main slow down factor when saving
        self.__isPrintingTimes = False

        # Labeling
        self.__eventCnt = 0
        self.__eventLabels = ['ARENA LOADED', 'VEHICLE CHANGED']

        self.__makeDirs()

    """============================================ CAPTURING LOGS PHASE ============================================"""

    def omrolocs(self, callStackDepth=None, silence=False):  # type: (Optional[int], bool) -> None
        """ Optional Method Resolution Order Logger Optional Call Stack """

        if silence: return

        self.__log.append(
            (
                self.__dt.now(),
                list(self.__linksGenerator(callStackDepth))
            )
        )

    def label(self):  # type: () -> None
        """ Print next label, in self.__eventLabels if some left, else print un-named label """

        if self.__eventCnt < len(self.__eventLabels):
            label = self.__eventLabels[self.__eventCnt]
            self.__eventCnt += 1
        else:
            label = 'NO NAME LABEL' + str(len(self.__eventLabels) - self.__eventCnt)

        print '\n===============================================',label,'===============================================\n'

    @classmethod
    def __linksGenerator(cls, maxCallStackDepth):  # type: (Optional[int]) -> Iterator[SplitLink]
        frame = cls.__getFrame(1)

        callStackDepth = 0
        while frame and callStackDepth != maxCallStackDepth:
            codeObj, fLocals, lineNum = frame.f_code, frame.f_locals, frame.f_lineno
            methName, filePath = codeObj.co_name, codeObj.co_filename

            callerCls = None
            if 'self' in fLocals:
                callerCls = fLocals['self'].__class__
                defClsCond = cls.__privInsMethCond if cls.__isPrivate(methName) else cls.__pubInsMethCond
            elif 'cls' in fLocals:
                callerCls = fLocals['cls']
                defClsCond = cls.__privClsMethCond if cls.__isPrivate(methName) else cls.__pubClsMethCond

            if callerCls is None or isinstance(callerCls, cls.__OldStyleClsType):
                yield None, methName, filePath, lineNum
            else:
                mroClsNs = list(cls.__mroClsNsGenerator(callerCls, defClsCond, methName, codeObj))
                if mroClsNs[-1] == 'object':  # Sometimes definer class not found so follow inheritance tree to the root
                    mroClsNs = None
                yield mroClsNs, methName, filePath, lineNum

            frame = frame.f_back
            callStackDepth += 1

    @staticmethod
    def __mroClsNsGenerator(callerCls, defClsCond, methName, fCode):  # type: (ClassObject, DefClsCond, str, CodeType) -> Iterator[str]
        for cls in callerCls.__mro__:
            yield cls.__name__
            if defClsCond(cls, methName, fCode):
                return

    @staticmethod
    def __privInsMethCond(callerCls, methName, fCode):  # type: (ClassObject, str, CodeType) -> WasDefinerClsFound
        for attr in callerCls.__dict__.values():
            if (
                    isinstance(attr, STAK.__FunctionType)
                    and attr.__name__ == methName
                    and attr.func_code is fCode
            ):
                return True
        return False

    @staticmethod
    def __pubInsMethCond(callerCls, methName, fCode):  # type: (ClassObject, str, CodeType) -> WasDefinerClsFound
        if methName in callerCls.__dict__:
            method = callerCls.__dict__[methName]

            if isinstance(method, property):
                if method.fget.func_code is fCode:
                    return True
            elif method.func_code is fCode:
                return True
        return False

    @staticmethod
    def __privClsMethCond(callerCls, methName, fCode):  # type: (ClassObject, str, CodeType) -> WasDefinerClsFound
        for attr in callerCls.__dict__.values():
            if (
                    isinstance(attr, classmethod)
                    and attr.__func__.__name__ == methName
                    and attr.__func__.__code__ is fCode
            ):
                return True
        return False

    @staticmethod
    def __pubClsMethCond(cls, methName, fCode):  # type: (ClassObject, str, CodeType) -> WasDefinerClsFound
        if (
                methName in cls.__dict__
                and cls.__dict__[methName].__func__.__code__ is fCode
        ):
            return True
        return False

    @staticmethod
    def __isPrivate(methName):  # type: (str) -> bool
        return methName.startswith('__') and not methName.endswith('__')

    """=============================================================================================================="""

    """============================================= SAVING LOGS PHASE =============================================="""
    def save(self):  # type: () -> None
        """ Save stak.__log, splice, trimmed & more """

        start = self.__ti.time()

        callChainsWithStrLinks = [(timeStamp, list(self.__strLinkGen(callChain))) for timeStamp, callChain in self.__log]
        doneCallChainsWithStrLinks = self.__ti.time()

        self.__saveRawStakLogToPrimitives(callChainsWithStrLinks)
        done__saveRawStakLogToPrimitives = self.__ti.time()

        stdLogsInStakPeriod = self.__readAndParseStdLogs()
        doneStdLogsInStakPeriod = self.__ti.time()

        self.__saveStdLogsToPrimitives(stdLogsInStakPeriod)
        done__saveStdLogsInStakPeriodToPrimitives = self.__ti.time()

        callChainsWithCompressedStrLinks = self.__compressLinks(callChainsWithStrLinks)  # type: List[Tuple[datetime, str]]
        doneCallChainsWithCompressedStrLinks = self.__ti.time()

        splicedLogs = self.__saveSplicedToVariants(stdLogsInStakPeriod, callChainsWithCompressedStrLinks)
        doneSplicedLogs = self.__ti.time()

        self.__saveCompressedSplicedLogs(splicedLogs)
        done__saveCompressedSplicedLogs = self.__ti.time()

        self.__saveCompressedStakLogToVariants(callChainsWithCompressedStrLinks)
        done__saveCompressedStakLogToVariants = self.__ti.time()

        self.__printTimes(
            start, doneCallChainsWithStrLinks, done__saveRawStakLogToPrimitives, doneStdLogsInStakPeriod,
            done__saveStdLogsInStakPeriodToPrimitives, doneCallChainsWithCompressedStrLinks, doneSplicedLogs,
            done__saveCompressedSplicedLogs, done__saveCompressedStakLogToVariants
        )

    def __saveRawStakLogToPrimitives(self, callChainsWithStrLinks):  # type: (StrLinkCallChainsLog) -> None
        with open(
                self.__ifPathExistsIncSuffix(
                    self.__pathLogStak
                ), 'w'
        ) as f:
            f.writelines(
                (self.__chainLinker(*el)
                 for el in callChainsWithStrLinks)
            )

    @classmethod
    def __chainLinker(cls, timeStamp, callChainWithStrLinks):  # type: (TimeStamp, StrLinkCallChain) -> StampedLine
        return cls.__stampToStr(timeStamp) + ': ' + ' <- '.join(callChainWithStrLinks) + '\n'

    @staticmethod
    def __strLinkGen(callChain):  # type: (SplitLinkCallChain) -> Iterator[StrLink]
        for mroClsNs, methName, fileName, lineNum in callChain:
            if mroClsNs is None:
                yield fileName.replace('.py', str(lineNum)) + '.' + methName
            else:
                mroClsNs = mroClsNs[:]
                mroClsNs[-1] = mroClsNs[-1] + '.' + methName + ')' * (len(mroClsNs) - 1)
                yield '('.join(mroClsNs)

    def __readAndParseStdLogs(self):  # type: () -> ParsedStdLogs
        # TODO: Rewrite, the entire concept is bogus

        def splitTimeStampAndLogTypeFromLine(line):  # type: (StdLogLine) -> ParsedStdLogEntry
            colonCnt, timeStrEndI, typeFlagEndI, timeStamp, typeFlag = 0, 0, 0, None, None
            # TODO: Wtf this sucks
            try:
                for i, char in enumerate(line):
                    if char == ':':
                        colonCnt += 1

                        if colonCnt == 3:
                            timeStamp = self.__dt.strptime(line[:i], '%Y-%m-%d %H:%M:%S.%f')
                            timeStrEndI = i

                        elif colonCnt == 4:
                            typeFlagEndI = i + 2
                            typeFlag = line[timeStrEndI: typeFlagEndI]
                            line = line[typeFlagEndI:]
                            break

                    if i > 34:
                        break

                return timeStamp, typeFlag, line

            except:
                return None, ': BROKEN: ', line

        def parsedLinesGenerator(lines):
            for line in lines:
                timeStamp, typeFlag, line = splitTimeStampAndLogTypeFromLine(line)
                yield timeStamp, typeFlag, line

        def parsedLogCreator(path, period):
            with open(path, 'r') as f:
                lines = f.readlines()
            return list(
                parsedLinesGenerator(lines, *period)
            )

        return [
            parsedLogCreator(path, self.__stakPeriod)
            for path in self.__namesLogStd
        ]

    def __saveStdLogsToPrimitives(self, stdLogs):  # type: ()
        """ Seems like the std log files could be simply copy-pasted into the new dir, but part of the point of saving
        primitives is debugging STAK itself not to keep pristine copies of the original logs, although maybe do both? """

        for log, logName in zip(stdLogs, self.__namesLogStd):
            path = self.__ifPathExistsIncSuffix(
                self.__os.path.join(
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
    def __stdLogLineCreator(cls, timeStamp, typeFlag, line):  # type: (TimeStamp, LogFlag, ProbParsedLine) -> str
        return str(cls.__stampToStr(timeStamp)) + str(typeFlag) + str(line)

    def __saveSplicedToVariants(self, stdLogs, stakLog):

        def spliceGenerator(stdLog, stakLog):
            stdI, stakI, stdElLeft, stakElLeft, lenStd, lenStak = 0, 0, True, True, len(stdLog), len(stakLog)

            stdTimeStamp, stdTypeFlag, stdLine = stdLog[stdI]
            stakTimeStamp, callChain = stakLog[stakI]

            while stdElLeft or stakElLeft:

                if stdElLeft is True and (stdTimeStamp <= stakTimeStamp or stakElLeft is False):
                    yield stdTimeStamp, stdTypeFlag, stdLine
                    stdI += 1
                    if stdI == lenStd:
                        stdElLeft = False
                    else:
                        newStamp, stdTypeFlag, stdLine = stdLog[stdI]
                        if newStamp is not None:
                            stdTimeStamp = newStamp

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
                self.__os.path.join(
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
                    self.__os.path.join(
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
                        self.__os.path.join(
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
    def __stakPeriod(self):
        return self.__log[0][0], self.__dt.now() # self.__log[-1][0]

    @staticmethod
    def __stampToStr(timeStamp):  # type: (datetime) -> str
        if timeStamp is not None:
            return timeStamp.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        return 'TIMESTAMP PARSING FAILED'

    """=============================================================================================================="""

    """================================================= COMPRESSION ================================================"""

    class __CompressionFormatList(list):
        """ List that holds extra attributes for internal use in compression"""

        def __init__(self, cnt=1, rep='', *args):
            super(STAK._STAK__CompressionFormatList, self).__init__(args)
            self.cnt = cnt
            self.rep = rep

    def __compressLinks(self, callChainsWithStrLinks):
        return [
            (
                timeStamp,
                self.__prettyfyLine(
                    self.__compress(
                        self.__CompressionFormatList(1, 'line', *callChain)
                    )
                ).rstrip(' <- ') + '\n'
            )
            for timeStamp, callChain in callChainsWithStrLinks
        ]

    def __compressLines(self, lines):  # type: (List[str]) -> List[str]
        return self.__prettyfyLines(
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
            if isinstance(el, cls.__CompressionFormatList):
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
            if isinstance(el, cls.__CompressionFormatList):
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
        return cls.__CompressionFormatList(1, 'lines', *lines)

    def __compress(self, postPassCfl):
        represents = postPassCfl.rep

        for groupSize in range(1, min(len(postPassCfl) // 2, self.__maxGroupSize)):

            prePassCfl = postPassCfl
            postPassCfl = self.__CompressionFormatList(cnt=prePassCfl.cnt, rep=prePassCfl.rep)

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

                        compressed_group = self.__CompressionFormatList(groups_cnt, represents, *thisGroup)
                        postPassCfl.append(compressed_group)

                        thisGroupStartI = nextGroupStartI
                        thisGroupEndI = nextGroupEndI

                        nextGroupStartI += groupSize
                        nextGroupEndI += groupSize

                        groups_cnt = 1

                thisGroup = prePassCfl[thisGroupStartI: thisGroupEndI + 1]
                nextGroup = prePassCfl[nextGroupStartI: nextGroupEndI + 1]

        return postPassCfl

    def __printTimes(self, start, doneCallChainsWithStrLinks, done__saveRawStakLogToPrimitives,
                     doneStdLogsInStakPeriod,
                     done__saveStdLogsInStakPeriodToPrimitives, doneCallChainsWithCompressedStrLinks,
                     doneSplicedLogs,
                     done__saveCompressedSplicedLogs, done__saveCompressedStakLogToVariants
                     ):
        if not self.__isPrintingTimes: return
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
    def changePath(
            self,
            prnt=None,    # type: Optional[PrintDirName]
            task=None,    # type: Optional[TaskDirName]
            prim=None,    # type: Optional[PrimitivesDirName]
            vari=None,    # type: Optional[VariantsDirName]
            root=None,    # type: Optional[StakRootDirName]
            stdLogs=None  # type: Optional[StdLogFileNames]
    ):
        """ Change dir &/or file name(s), new dirs are created if don't exist, pass only name(s) not paths """

        if prnt    is not None: self.__dirPrnt     = prnt
        if task    is not None: self.__dirTask     = task
        if prim    is not None: self.__dirPrimi    = prim
        if vari    is not None: self.__dirVari     = vari
        if root    is not None: self.__dirRoot     = root
        if stdLogs is not None: self.__namesLogStd = stdLogs

        self.__makeDirs()

    def rmPrint(self):  # type: () -> None
        """ Remove & recreate current print directory & all its logs """

        self.__rmtree(self.__pathDirPrint)
        self.__makeDirs()

    def clear(self):  # type: () -> None
        """ Clears current logs, stak & std. Also resets event count (label print count) """

        for logPath in self.__namesLogStd:
            with open(logPath, 'w'): pass

        self.__log = []
        self.__eventCnt = 0

        self.omrolocs()

    def __makeDirs(self):  # type: () -> None

        if not self.__os.path.isdir(self.__pathDirPrimi):
            self.__os.makedirs(self.__pathDirPrimi)

        if not self.__os.path.isdir(self.__pathDirVari):
            self.__os.makedirs(self.__pathDirVari)

    @classmethod
    def __addSuffix(cls, logName, suffix):  # type: (FileName, str) -> FileName
        name, ext = cls.__os.path.splitext(logName)
        return '{}{}{}'.format(name, suffix, ext)

    @classmethod
    def __ifPathExistsIncSuffix(cls, filePath):  # type: (StrFilePath) -> NonexistentPath
        fileName, ext = cls.__os.path.splitext(
            cls.__os.path.basename(filePath)
        )
        dirPath = cls.__os.path.dirname(filePath)
        cnt = 0

        while cls.__os.path.isfile(filePath):
            cnt += 1
            filePath = cls.__os.path.join(
                dirPath, '{}{}{}'.format(fileName, cnt, ext)
            )

        return filePath

    @property
    def __pathDirPrint(self):  # type: () -> StrPathToPrintDir
        return self.__os.path.join(self.__dirRoot, self.__dirTask, self.__dirPrnt)

    @property
    def __pathDirPrimi(self):  # type: () -> StrPathToPrimitivesDir
        return self.__os.path.join(self.__pathDirPrint, self.__dirPrimi)

    @property
    def __pathDirVari(self):  # type: () -> StrPathToVariantsDir
        return self.__os.path.join(self.__pathDirPrint, self.__dirVari)

    @property
    def __pathLogStak(self):  # type: () -> StrFilePathToStakLogPrimitive
        return self.__os.path.join(self.__pathDirPrimi, self.__nameLogStak)

    """=============================================================================================================="""

s = STAK()

def decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

class Interface(object):
    def testCallerOfCaller(self): raise NotImplementedError()
class Ganny(object): pass
class Daddy(Ganny):
    @decorator
    def test(self): s.omrolocs()
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

        with open(stdLogPaths[0], 'a') as f:
            l1 = 'fdStamp' + ': ' + nonCompromisingLines[randint(0, 5)]
            f.writelines(l1)

genLogs()
variables = globals().copy()
variables.update(locals())
shell = code.InteractiveConsole(variables)
shell.interact()


















































# end
