"""
How to use:
    - Copy-paste STAK in some high level utils type file & instantiate
    - Import the STAK object to make log entries by calling omrolocs & data
    - Need an interactive terminal, import STAK instance into it, & call help(instanceName)

Known issues:
    - Caller & definer classes can't be found for partials either

    - Caller class cannot be found for wrapped methods & therefore definer class neither (with custom wrappers,
    not @property nor @classmethod, yes @staticmethod but for other reasons)

    - A private property will default to filename & lineno,

    - If the object object autopassed to an instance method is not called 'self' defaults to filename & lineno

    - If the class object autopassed to a class method is not called 'cls' defaults to filename & lineno

    - If the method is defined in an old style class, it defaults to filename & lineno

    - The spliceGenerator raises an error if any of the spliced logs is empty, which they normally shouldn't but yeah

    - Due to the compression algorith some, potentially more profitable patterns, are lost e.g. A, A, A, B, A, B -> 3A, BAB

    - If some feels the need to write his own cached property then this will break omrolocs and omropocs

    - STAK.clear() is bugged

    - There seems to be a problem when the standard logs are empty

    - Seems like the std log parsing fails to parse the last entries

Unknown Issues:
    - If the program crashes there might be a problem

Cool potential features:
    - (Mid) Sometimes a single task requires more than one set of prints, so, divide the prints by set, with name.

    - (Hard) Split the entire project into logical sections, make each section into a pip installable library,
    refactor the code to split the generic library code from the project specific. And make all python3 compatible.

    - (Mid) delta-auto-attrs, log all the instance attrs on change, e.g. when initialised, when changed etc...

    - (Hard) Make a "class decorator" metaclass which omrolocsalads the entire class ??

    - (Easy) Make a timing decorator, to check out how much it takes for example to save, or init

    - (Easy) Many names are entirely too long, make them short

    - (Easy) omrolocsalad, sometimes uses entirely too many lines to print one datum, automatically detect this & print in one line

    - (Mid) auto-deject calls to STAK interface. (Like, remove s.omrolocs from the code)

    - (Easy) Add appropriate flags for each interface method, AUTOLOCALS, OMROLOCSALAD, ...

    - (Easy) Sometimes prints bogus add auto-delete specific print

    - (Easy) Add auto-incr flag for print dir, also add a string to auto-write the .descr.txt

    - (Mid) In similar fashion to locals-auto-data, do something like func-auto-ret, to be able to log what a function is returning
    without having to add an extra result local & combine both into func-auto-log.

    - (Hard) Take inspiration from the TDV logger, and have a process logger and an instance logger, and somehow save that clusterfuck

    - (Hard) Trace setter.

    - (Hard) Add the flags back to the compressed logs. More generally add comprehensive settings, such that all the parts of the
    logs can be added or taken away with some flags.

    - (Easy) Sometimes certain prints are hard to obtain therefore to avoid accidental destruction some sort of mechanism to protect
    them must be established

    - (Mid) different outs:
        - When multiple processes are running the logs are separate, to have them joined write directly to file on entry & give a
    flag name to each process to understand which process is producing the logs

    - (Mid) Given an object find the class who instantiated it, & the entire mro from it towards object, in the "auto", fashion, obj-auto-data

    - (Mid)(Facilitator) Split the different entries each in their own log, to make processing simpler, also, optionally print each
    in their own file, but must keep entry order since entries might happen at the same timestamp

    - (Mid) Inherit from datastructures, (list, dict, etc) & override __getitem__ & __setitem__ to log who is messing with them.

    - (Easy) Add an option to print the stack in multiple lines with indentation

    - (Mid) Pretty print data structures

    - (Hard) If there are multiple methods in the call stack that have the same MRO compress that

    - (Hard) Somehow better prints for wrappers, e.g. CallerCls(DefinerCls.@decoratorName.methNameToFindDefClsOf) (Look at closures? maybe?)

    - (Hard) Reconstruct a class based on inheritance, i.e. "superHelp" similar to the built-in help, but print the code of all the methods
    all into one class and save that into a .py file such that any class that inherits from any number of classes or uses a metaclass
    can be substituted for the output of superHelp and have it behave in the same way

    Facilitator - Doing this task will make future tasks easier
    Easy - I definitely know how to do this, & shouldn't take long.
    Mid  - Either I know how but will take a long time or there is some part I don't know how to do but recon it won't be too hard.
    Hard - Either I don't know how to do this & I recon it'd be pretty hard or impossible or I kind of know & know it will take for-ever.


    Open question:

        Is it better to make all the log entries into one list? or have one list per flag??

        One list:
            - Keeps order of entry
            - Needs to separate lists to make individual log

        Many lists:
            - Makes formatting easier
            - Needs to join lists to make a global log

        Conclusion:
            I've tried with one list & it is a pain in the ass, I'll try with many
            (probably still is a pain in the ass)

"""

# Imports used outside STAK
import code
from datetime import datetime
from itertools import repeat
from random import randint
from time import sleep
from types import CodeType, FrameType, ClassType

from src.funcs.someCode import SomeClass

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import *
    from collections import *

    # Type Aliases: Use sparingly bc hiding complexity behind a type alias looks good but makes it harder to decypher,
    # & so counter-productively more complex. Therefore, use to abbreviate simplicity, not hide complexity.
    ##################################################################
    StrsStamp = Tuple[str, str, str, str]
    IntsStamp = Tuple[int, int, int, int]

    PathGen = Callable[[], Iterator[str]]

    OptStr9 = Tuple[Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str], Optional[str]]

    NestedIterable = Union[Any, Iterable['NestedIterable']]


testingWhat = 'trace'

class STAK(object):
    __doc__ = None
    """ ==================== DATA THAT IS REFERENCED BY THE INSTANCE BUT NOT MODIFIED, SO, CAN BELONG TO THE CLASS ==================== """
    from os.path import (isdir as __isdir, exists as __exists, join as __join, splitext as __splitext, basename as __basename,
                         dirname as __dirname, isfile as __isfile); from os import makedirs as __makedirs
    from types import ClassType as __OldStyleClsType; from datetime import datetime as __dt; from time import time as __time
    from shutil import rmtree as __rmtree; from types import FunctionType as __FunctionType
    from sys import _getframe as __getFrame, settrace as __setTrace, gettrace as getTrace

    __slots__ = ('printDir', 'taskDir', 'eventCnt', 'eventLabels', '_rootDir', '_primitivesDir', '_variantsDir', '_stakLogFile', '_traceLogFile', '_stdLogFiles', '_maxCompressGroupSize', '__log', '__appendToLog', '__extendLog', '__traceLog', '__openFuncs', '__appendToTraceLog', '__jointLinkFromFrame', '__splitLinkFromFrame', '__jointLinksGen', '__splitLinksGen', '__traceOriginatorEntry', '__traceTerminatorEntry', '__saveStakLogToPrimitives', '__saveTraceLogToPrimitives', '__saveStdLogsToPrimitives')  # This line was injected by injectors.py

    # OS specific details
    __pathSplitChar = '/' if '/' in __getFrame(0).f_code.co_filename else '\\'

    # Flags
    _stakFlags = ('OMROLOCS', 'DATE', 'DATA', 'LABEL')
    __pStakFlags = (': OMROLOCS: ', ': DATE    : ', ': DATA    : ', ': LABEL   : ')  # This line was injected by injectors.py

    _stdFlags = ('DEBUG', 'INFO', 'NOTICE', 'WARNING', 'ERROR', 'CRITICAL', 'HACK', 'TRACE', 'ASSET')
    __paddedStdFlags = (': DEBUG   : ', ': INFO    : ', ': NOTICE  : ', ': WARNING : ', ': ERROR   : ', ': CRITICAL: ', ': HACK    : ', ': TRACE   : ', ': ASSET   : ')  # This line was injected by injectors.py

    __pStdFlagsByStdFlags = {'INFO': ': INFO    : ', 'CRITICAL': ': CRITICAL: ', 'NOTICE': ': NOTICE  : ', 'TRACE': ': TRACE   : ', 'HACK': ': HACK    : ', 'WARNING': ': WARNING : ', 'ASSET': ': ASSET   : ', 'ERROR': ': ERROR   : ', 'DEBUG': ': DEBUG   : '}  # This line was injected by injectors.py
    __allPflagsByFlags = {'INFO': ': INFO    : ', 'CRITICAL': ': CRITICAL: ', 'NOTICE': ': NOTICE  : ', 'TRACE': ': TRACE   : ', 'CUTOFF': ': CUTOFF  : ', 'OMROLOCS': ': OMROLOCS: ', 'HACK': ': HACK    : ', 'LABEL': ': LABEL   : ', 'DEBUG': ': DEBUG   : ', 'WARNING': ': WARNING : ', 'ASSET': ': ASSET   : ', 'ERROR': ': ERROR   : ', 'DATE': ': DATE    : ', 'DATA': ': DATA    : '}  # This line was injected by injectors.py

    __pStdFlagsByStdFlags['CUTOFF'] = ': CUTOFF  : '  # Manually padding ain't great
    _cutoffFlag = 'CUTOFF'

    __traceFlag = 'TRACE'

    # Parsing standard logs
    from re import compile; __matcher = compile(
        r'(?:(\d{4})-)?' r'(?:(\d{2})-)?' r'(?:(\d{2}) )?' r'(?:(\d{2}):)?' r'(?:(\d{2}):)?' r'(?:(\d{2})\.)?' r'(?:(\d{3}))?' r': ([A-Z]+):'
    ).search; del compile

    from collections import OrderedDict; __cutoffCombos = OrderedDict((('CRITICAL', 1), ('WARNING', 1), ('RITICAL', 1), ('NOTICE', 1), ('ITICAL', 1), ('ARNING', 1), ('RNING', 1), ('OTICE', 1), ('ASSET', 1), ('TICAL', 1), ('ERROR', 1), ('DEBUG', 1), ('TRACE', 1), ('HACK', 1), ('TICE', 1), ('RACE', 1), ('NING', 1), ('RROR', 1), ('INFO', 1), ('SSET', 1), ('ICAL', 1), ('EBUG', 1), ('ACE', 1), ('ACK', 1), ('CAL', 1), ('SET', 1), ('ICE', 1), ('ROR', 1), ('BUG', 1), ('NFO', 1), ('ING', 1), ('FO', 1), ('NG', 1), ('CK', 1), ('AL', 1), ('CE', 2), ('ET', 1), ('UG', 1), ('OR', 1), ('E', 2), ('G', 2), ('K', 1), ('O', 1), ('L', 1), ('R', 1), ('T', 1))); del OrderedDict  # This line was injected by injectors.py
    __wholeEnoughs = {'NOTICE': 'NOTICE', 'RNING': 'WARNING', 'ACE': 'TRACE', 'ACK': 'HACK', 'HACK': 'HACK', 'EBUG': 'DEBUG', 'TICE': 'NOTICE', 'CAL': 'CRITICAL', 'OTICE': 'NOTICE', 'ASSET': 'ASSET', 'RACE': 'TRACE', 'FO': 'INFO', 'SET': 'ASSET', 'ITICAL': 'CRITICAL', 'NG': 'WARNING', 'WARNING': 'WARNING', 'NING': 'WARNING', 'ROR': 'ERROR', 'BUG': 'DEBUG', 'CK': 'HACK', 'CRITICAL': 'CRITICAL', 'TICAL': 'CRITICAL', 'NFO': 'INFO', 'K': 'HACK', 'AL': 'CRITICAL', 'O': 'INFO', 'L': 'CRITICAL', 'R': 'ERROR', 'ICE': 'NOTICE', 'ERROR': 'ERROR', 'DEBUG': 'DEBUG', 'ET': 'ASSET', 'ARNING': 'WARNING', 'INFO': 'INFO', 'SSET': 'ASSET', 'TRACE': 'TRACE', 'T': 'ASSET', 'RITICAL': 'CRITICAL', 'ICAL': 'CRITICAL', 'UG': 'DEBUG', 'ING': 'WARNING', 'OR': 'ERROR', 'RROR': 'ERROR'}  # This line was injected by injectors.py

    # Trace log stuff
    __callableNames = {'appendToLog', 'extendLog', 'appendToTraceLog', 'jointLinkFromFrame', 'splitLinkFromFrame', 'jointLinksCallChain', 'splitLinksCallChain', 'traceOriginatorEntry', 'traceTerminatorEntry', 'saveStakLogToPrimitives', 'saveTraceLogToPrimitives', 'saveStdLogsToPrimitives', 'basename', 'delTrace', 'gettrace', '__spliceGen', 'join', '__pubClsMethCond', 'clear', '__saveSplicedToVariants', '__prettyfyLine', '__interpolStampGen', '__trimFlag', '_dateEntry', '__partStrLinkCreator', '__trimFlagIfPoss', 'rmtree', '__linksAndFirstFrameLocalsGen', 'makedirs', 'setTrace', '__joinFileLink', 'dirname', 'exists', '__unixStampToTupleOfInts', 'settrace', '__strLinkCallChainGen', 'save', '__parseAndInterpolLines', '__joinTraceEntriesUntilReversal', '__mroClsNsGen', '__OldStyleClsType', '__formatLinesForLinesCompression', 'matcher', '__retArgs', '__formatStakLog', 'FunctionType', 'omropocs', '__call__', '__formatParsedStdLog', '__genPathDirPrimi', '__compress', 'autoLocals', '__trimFilePathAddLinenoGen', '_getframe', '__mroLinkToStrLink', '__compressLinksGen', 'l', '__data', '__tupleOfIntsToTupleOfStrs', '__parsedLinesGen', 'datetime', '__datetimeToTupleOfInts', '__pubInsMethCond', '__prettyfyLines', '__privClsMethCond', '__genPathDirPrint', '__tupleOfStrsToStr', 'time', '__init__', '__parsedStdLogGen', '__privInsMethCond', 'rp', '__joinMroLink', '__splitStampFromTheRest', '__saveCompressedStakLogToVariants', 'label', '__preProcessLogGen', '__saveCompressedSplicedLogs', '__trimTime', '__addSuffix', '__unixStampToTupleOfStrs', 'omrolocs', '__saveLogsToFile', '__linksGen', 'splitext', 'rmPrint', 'isdir', '__compressLines', '__genPathDirVari', '__genPathLogStak', 'data', '__traceEntry', 'c', 'isfile', '__splitLinkToStr', '__genPathLogTrace', '__formatTraceLog', '__fileUnique', '__genPathLogsStd', 's', '__linkFromFrame', 'omrolocsalad', 'unixStampToDatetime', '__unixStampToStr', 'CompressionFormatList', '__midStampToStr'}  # This line was injected by injectors.py

    """ =============================================================================================================================== """

    def __init__(self):  # type: () -> None
        # Names that should change relatively often
        self.printDir    = 'print'
        self.taskDir     = 'task'
        self.eventCnt    = 0
        self.eventLabels = ['PRE-EVENT-1', 'POST-EVENT-1', 'PRE-EVENT-2', 'POST-EVENT-2']

        # Names that can but really shouldn't change that often
        self.rootDir       = '.STAK'
        self.primitivesDir = 'primitives'
        self.variantsDir   = 'variants'
        self.stakLogFile   = 'stak.log'
        self.traceLogFile  = 'trace.log'
        self.stdLogFiles   = ('stdLogA.log', 'stdLogB.log')
        self.maxCompressGroupSize = 100  # Increases compress times exponentially

        # Stak log stuff
        self.log = []  # type: List[Tuple[float, str, Union[str, Tuple[Union[Tuple[str, int, str], Tuple[List[str], str]], ...]]]]
        self.appendToLog = self.log.append
        self.extendLog   = self.log.extend

        # Trace log stuff
        self.traceLog = []
        self.openFuncs = set()  # type: Set[FrameType]
        self.appendToTraceLog = self.traceLog.append

        #### Partials ####
        #### CAUTION: All callables should be either methods or instance attributes, so that the tracing callable knows to skip them
        #### Intermediate callables such that they will have the same methName in their frame as some class callable are valid
        from functools import partial

        # Call stack creating partials
        linkerArgs = (self.__privInsMethCond, self.__privClsMethCond, self.__pubInsMethCond,
                      self.__pubClsMethCond, self.__OldStyleClsType, self.__mroClsNsGen,)

        joinFileLink = partial(self.__joinFileLink, self.pathSplitChar)
        self.jointLinkFromFrame = partial(self.linksFromFrame, self.__joinMroLink, joinFileLink, *linkerArgs)
        self.splitLinkFromFrame = partial(self.linksFromFrame, self.__retArgs, self.__retArgs, *linkerArgs)

        self.jointLinksCallChain = partial(self.linksGen, self.jointLinkFromFrame)
        self.splitLinksCallChain = partial(self.linksGen, self.splitLinkFromFrame)

        # Trace partials
        self.traceOriginatorEntry = partial(self.traceEntry, 'originator')
        self.traceTerminatorEntry = partial(self.traceEntry, 'terminator')

        # Saving logs partials
        saver = partial(self.writeLogsToFile, self.makeFilePathUnique, 'w')
        self.saveStakLogToPrimitives  = partial(
            saver, self.pathLogStak , partial(self.formatStakLog, self.stakFlags, self.pStakFlags, self.__midStampToStr)
        )
        self.saveTraceLogToPrimitives = partial(saver, self.pathLogTrace, self.formatTraceLog)

        self.saveStdLogsToPrimitives  = partial(
            saver, self.pathLogsStd , partial(self.formatParsedStdLog, self.__midStampToStr, self.pStdFlagsByStdFlags)
        )

        # First log entry to log current date
        self._dateEntry()

    """ =========================================================== INTERFACE ========================================================= """

    # Call-from-code interface
    def omropocs(self):  # type: () -> None
        """ Its back! sometimes u just need the good old omropocs! in new & improved form! """
        # TODO: Try to make static maybe?
        print ' <- '.join(self.jointLinksCallChain())

    def omrolocs(self, silence=False):  # type: (bool) -> None
        """ Optional Method Resolution Order Logger Optional Call Stack """
        if silence: return
        self.appendToLog(
            (
                self.time(),
                self.stakFlags[0],
                tuple(self.splitLinksCallChain()),
            )
        )

    def data(self, pretty=False, **dataForLogging):  # type: (bool, Any) -> None
        """ Log data structures, their callable & definer class names """

        strLink = next(self.jointLinksCallChain())
        self.__data(pretty, strLink, **dataForLogging)

    def omrolocsalad(self, silence=False, pretty=False, **additionalDataForLogging):  # type: (bool, bool, Any) -> None
        """ Optional Method Resolution Order Logger Optional Call Stack And Locals Auto Data """
        if silence: return

        linksAndFirstFrameLocalsGen = self.linksAndFirstFrameLocalsFromFrame()
        firstFrameLocals = next(linksAndFirstFrameLocalsGen)  # type: Dict[str, Any]

        for key, value in firstFrameLocals.items():
            if key != 'self' and key != 'cls':
                additionalDataForLogging[key] = value

        splitLinks = tuple(linksAndFirstFrameLocalsGen)
        firstLinkAsStr = self.splitLinkToStr(splitLinks[0])

        self.appendToLog(
            (
                self.time(),
                self.stakFlags[0],
                splitLinks,
            )
        )

        self.__data(
            pretty,
            firstLinkAsStr,
            **additionalDataForLogging
        )

    def autoLocals(self, silence=False, pretty=False, **additionalDataForLogging):  # type: (bool, bool, Any) -> None
        """ Logs locals from frame from which this method was called, optionally other kwargs """
        if silence: return

        linksAndFirstFrameLocalsGen = self.linksAndFirstFrameLocalsFromFrame()
        firstFrameLocals = next(linksAndFirstFrameLocalsGen)  # type: Dict[str, Any]

        for key, value in firstFrameLocals.items():
            if key != 'self' and key != 'cls':
                additionalDataForLogging[key] = value

        firstLinkAsStr = self.splitLinkToStr(next(linksAndFirstFrameLocalsGen))
        self.__data(
            pretty,
            firstLinkAsStr,
            **additionalDataForLogging
        )
    # WIP for pretty recursive
    # @staticmethod
    # def isIter(_iter):  # type: (Any) -> bool
    #     try:
    #         iter(_iter)
    #         return True
    #     except TypeError:
    #         return False
    #
    # @staticmethod
    # def hasKeysAndValues(_dict):  # type: (Any) -> Optional[List[Tuple[Hashable, Any]]]
    #     try:
    #         return _dict.items()
    #     except AttributeError:
    #         return
    #
    # def dataIterPretty(self, iterForPretty):  # type: (NestedIterable) -> None
    #     try:
    #         iterable = iterForPretty.iteritems()
    #     except AttributeError:
    #         try:
    #             iterable = iter(iterForPretty)
    #         except TypeError:
    #             return
    #
    #     prettyfied = [el for el in iterable]
    #
    #     if pretty:
    #         now, flag = self.time(), self.stakFlags[2]
    #
    #         if dataForLogging:
    #             self.appendToLog((now, flag, '{}(\n'.format(strLink)))
    #             self.extendLog(
    #                 (now, flag, '    {}={},\n'.format(name, datum))
    #                 for name, datum in dataForLogging.items()
    #             )
    #             self.appendToLog((now, flag, ')\n'))
    #         else:
    #             self.appendToLog((now, flag, '(No data was passed)\n'))
    #     else:
    #         self.appendToLog(
    #             (
    #                 self.time(),
    #                 self.stakFlags[2],
    #                 (
    #                     '{}('.format(strLink) +
    #                     ', '.join(('{}={}'.format(name, datum) for name, datum in dataForLogging.items())) +
    #                     ')\n'
    #                 ) if dataForLogging else '{}('.format(strLink) + 'No data was passed)\n'
    #             )
    #         )

    def setTrace(self):
        oldTrace = self.__getTrace()
        if oldTrace is not self:
            self.__traceOriginatorEntry(self.__getFrame(1))
            self.__setTrace(self)

    def delTrace(self):
        self.__traceTerminatorEntry(self.__getFrame(1))
        self.__setTrace(None)

    # Call-from-shell interface
    def save(self):  # type: () -> None
        """ Save stak.log, spliced, trimmed & more """

        # Make paths if don't exist just in time bc on innit might cause collisions (Yeah wtf, but I'm not messing with this)
        if not self.isdir(next(self.pathDirPrimi())):
            self.makedirs(next(self.pathDirPrimi()))
        if not self.isdir(next(self.pathDirVari())):
            self.makedirs(next(self.pathDirVari()))

        log = tuple(
            self.preProcessLog(
                self.log  # type: List[Tuple[float, str, Union[str, Tuple[Union[Tuple[str, int, str], Tuple[List[str], str]], ...]]]]
            )
        )  # type: Tuple[Tuple[float, str, Union[str, Tuple[Union[Tuple[str, str], Tuple[List[str], str]], ...]]], ...]

        # partStrLinkCallChains = tuple(self.__strLinkCallChainGen(log, self.__partStrLinkCreator))

        fullStrLinkCallChains = tuple(
            self.strLinkCallChain(
                log, self.mroLinkToStrLink
            )
        )  # type: Tuple[Tuple[StrsStamp, str, Union[Tuple[str, ...], str]], ...]

        self.saveStakLogToPrimitives(fullStrLinkCallChains)

        self.saveTraceLogToPrimitives(self.traceLog)

        callChainsWithCompressedStrLinks = tuple(self.compressLinksGen(fullStrLinkCallChains))
        self.saveCompressedStakLogToVariants(callChainsWithCompressedStrLinks)

        parsedStdLogs = tuple(  # Flags not padded yet
            self.parseStdLogs()
        )  # type: Tuple[Tuple[Tuple[StrsStamp, str, str]]]

        self.saveStdLogsToPrimitives(*parsedStdLogs)
        splicedLogs = self.saveSplicedToVariants(parsedStdLogs, callChainsWithCompressedStrLinks)

        self.saveCompressedSplicedLogs(splicedLogs)

    def label(self, label=None):  # type: (Optional[str]) -> None
        """ Make a log entry with the passed label, else, with next label in eventLabels, if any, else print no-name label """
        if label is None:
            if self.eventCnt < len(self.eventLabels):
                label = self.eventLabels[self.eventCnt]
                self.eventCnt += 1
            else:
                label = 'NO-NAME LABEL' + str(len(self.eventLabels) - self.eventCnt)

        self.appendToLog(
            (
                self.time(),
                self.stakFlags[3],
                '\n========================================================= {} '
                '=========================================================\n\n'.format(label)
            )
        )

    def clear(self):  # type: () -> None
        """ DANGER: Clears current logs, stak & std. Resets self.eventCnt (label print count) & more """
        for logPath in self.stdLogFiles:
            with open(logPath, 'w'): pass

        self.log = []
        self.appendToLog = self.log.append
        self.extendLog    = self.log.extend
        self.eventCnt = 0

        self._dateEntry()

    def rmPrint(self):  # type: () -> None
        """ MUCH DANGER: Remove current print dir & all its logs """
        if self.exists(next(self.pathDirPrint())):
            self.rmtree(next(self.pathDirPrint()))

    # Call-from-self autoface
    def _dateEntry(self):
        # Since normal entries only log time, this one is used to log date, normally on logging session init
        self.__appendToLog((self.__time(), self._stakFlags[1], self.__dt.now().strftime('%Y-%m-%d\n')))

    """ =============================================================================================================================== """

    """ =================================================== CREATING MRO CALL CHAINS ================================================== """

    @staticmethod
    def __linkFromFrame(
            joinMroLinksMaybe, # type: Callable[[List[str], str], Union[str, Tuple[List[str], str]]]
            joinFileLinksMaybe,# type: Callable[[str, int, str], Union[str, Tuple[str, int, str]]]
            privInsMethCond,   # type: Callable[[Type[Any], str, CodeType], bool]
            privClsMethCond,   # type: Callable[[Type[Any], str, CodeType], bool]
            pubInsMethCond,    # type: Callable[[Type[Any], str, CodeType], bool]
            pubClsMethCond,    # type: Callable[[Type[Any], str, CodeType], bool]
            OldStyleClsType,   # type: ClassType
            mroClsNsGen,       # type: Callable[[Type[Any], Callable[[Type[Any], str, CodeType], bool], str, CodeType], Iterator[str]]
            frame,             # type: FrameType
    ):  # type: (...) -> Union[Tuple[str, int, str], Tuple[List[str], str], str]

        codeObj, fLocals = frame.f_code, frame.f_locals
        methName = codeObj.co_name

        callerCls = None
        if 'self' in fLocals:
            callerCls = fLocals['self'].__class__
            defClsCond = privInsMethCond if methName.startswith('__') and not methName.endswith('__') else pubInsMethCond
        elif 'cls' in fLocals:
            callerCls = fLocals['cls']
            defClsCond = privClsMethCond if methName.startswith('__') and not methName.endswith('__') else pubClsMethCond

        if callerCls is None or isinstance(callerCls, OldStyleClsType):
            return joinFileLinksMaybe(codeObj.co_filename, frame.f_lineno, methName)
        else:
            # PyCharm thinks defClsCond could be undefined, but if callerCls is not None it must be defined
            mroClsNs = list(mroClsNsGen(callerCls, defClsCond, methName, codeObj))
            if mroClsNs[-1] == 'object':  # Sometimes definer class not found so follow inheritance tree to the root
                return joinFileLinksMaybe(codeObj.co_filename, frame.f_lineno, methName)
            else:
                return joinMroLinksMaybe(mroClsNs, methName)

    def __linksGen(self,
            linkFromFrame,  # type: Callable[[FrameType], Union[str, Tuple[List[str], str], Tuple[str, int, str]]]
    ):  # type: (...) -> Iterator[Union[str, Tuple[List[str], str], Tuple[str, int, str]]]

        frame = self._getframe(2)
        while frame:
            yield linkFromFrame(frame)  # Should create joined (str) links or split based on the args in the partial
            frame = frame.f_back

    @staticmethod
    def __mroClsNsGen(callerCls, defClsCond, methName, codeObj):
        # type: (Type[Any], Callable[[Type[Any], str, CodeType], bool], str, CodeType) -> Iterator[str]
        for cls in callerCls.__mro__:
            yield cls.__name__
            if defClsCond(cls, methName, codeObj):
                return

    @staticmethod
    def __privInsMethCond(defClsMaybe, methNameToFindDefClsOf, codeObjToFindDefClsOf):  # type: (Type[Any], str, CodeType) -> bool
        # This works even when the class defined __slots__ because we're iterating over the class objects' __dict__
        # not the object objects', & as far as I know class objects always have __dict__ even if they declare __slots__
        for attr in defClsMaybe.__dict__.values():
            if (
                    isinstance(attr, STAK.__FunctionType) and
                    attr.__name__ == methNameToFindDefClsOf and
                    # If the code object is the same do we need to compare the meth name too??
                    attr.func_code is codeObjToFindDefClsOf
            ):
                return True
        return False

    @staticmethod
    def __pubInsMethCond (defClsMaybe, methNameToFindDefClsOf, codeObjToFindDefClsOf):  # type: (Type[Any], str, CodeType) -> bool
        # This works even when the class defined __slots__ because we're iterating over the class objects' __dict__
        # not the object objects', & as far as I know class objects always have __dict__ even if they declare __slots__
        if methNameToFindDefClsOf in defClsMaybe.__dict__:
            method = defClsMaybe.__dict__[methNameToFindDefClsOf]

            if isinstance(method, property):
                # PyCharm thinks func_code don't exist, it's wrong
                if method.fget.func_code is codeObjToFindDefClsOf:
                    return True
            elif method.func_code is codeObjToFindDefClsOf:
                return True
        return False

    @staticmethod
    def __privClsMethCond(defClsMaybe, methNameToFindDefClsOf, codeObjToFindDefClsOf):  # type: (Type[Any], str, CodeType) -> bool
        # This works even when the class defined __slots__ because we're iterating over the class objects' __dict__
        # not the object objects', & as far as I know class objects always have __dict__ even if they declare __slots__
        for attr in defClsMaybe.__dict__.values():
            if (
                    isinstance(attr, classmethod)
                    and attr.__func__.__name__ == methNameToFindDefClsOf
                    # PyCharms thinks __code__ don't exist, it's wrong
                    and attr.__func__.__code__ is codeObjToFindDefClsOf
            ):
                return True
        return False

    @staticmethod
    def __pubClsMethCond (defClsMaybe, methNameToFindDefClsOf, codeObjToFindDefClsOf):  # type: (Type[Any], str, CodeType) -> bool
        # This works even when the class defined __slots__ because we're accessing class objects' __dict__ not the
        # object objects', & as far as I know class objects always have __dict__ even if they declare __slots__
        if (
                methNameToFindDefClsOf in defClsMaybe.__dict__
                and defClsMaybe.__dict__[methNameToFindDefClsOf].__func__.__code__ is codeObjToFindDefClsOf
        ):
            return True
        return False

    @staticmethod
    def __joinMroLink(mroClsNs, methName):  # type: (List[str], str) -> str
        mroClsNs[-1] = '{}.{}{}'.format(mroClsNs[-1], methName, ')' * (len(mroClsNs) - 1))
        return '('.join(mroClsNs)

    @staticmethod
    def __joinFileLink(pathSplitChar, fullPath, lineno, methName):  # type: (str, str, int, str) -> str
        return '{}{}.{}'.format(fullPath.split(pathSplitChar)[-1].rstrip('py'), lineno, methName)

    @staticmethod
    def __retArgs(*args): return args  # Yes, this should be here to be skipped from tracing

    """ =============================================================================================================================== """

    """ ===================================== METHS CREATED IN RESPONSE TO LOCALS AUTO-LOGGING  ======================================= """

    def __data(self, pretty, strLink, **dataForLogging):  # type: (bool, str, Any) -> None
        if pretty:
            now, flag = self.time(), self.stakFlags[2]

            if dataForLogging:
                self.appendToLog((now, flag, '{}(\n'.format(strLink)))
                self.extendLog(
                    (now, flag, '    {}={},\n'.format(name, datum))
                    for name, datum in dataForLogging.items()
                )
                self.appendToLog((now, flag, ')\n'))
            else:
                self.appendToLog((now, flag, '(No data was passed)\n'))
        else:
            self.appendToLog(
                (
                    self.time(),
                    self.stakFlags[2],
                    (
                        '{}('.format(strLink) +
                        ', '.join(('{}={}'.format(name, datum) for name, datum in dataForLogging.items())) +
                        ')\n'
                    ) if dataForLogging else '{}('.format(strLink) + 'No data was passed)\n'
                )
            )

    def __linksAndFirstFrameLocalsGen(self):  # type: () -> Iterator[Union[Dict[str, Any], Tuple[List[str], str], Tuple[str, int, str]]]
        """ Must call next once to get the locals before it starts yielding links """
        frame, mroClsNsGen, OldStyleClsType = self._getframe(2), self.__mroClsNsGen, self.__OldStyleClsType
        privInsMethCond, pubInsMethCond = self.__privInsMethCond, self.__pubInsMethCond
        privClsMethCond, pubClsMethCond = self.__privClsMethCond, self.__pubClsMethCond

        codeObj, fLocals = frame.f_code, frame.f_locals
        methName = codeObj.co_name
        yield fLocals

        while True:
            callerCls = None
            if 'self' in fLocals:
                callerCls = fLocals['self'].__class__
                defClsCond = privInsMethCond if methName.startswith('__') and not methName.endswith('__') else pubInsMethCond
            elif 'cls' in fLocals:
                callerCls = fLocals['cls']
                defClsCond = privClsMethCond if methName.startswith('__') and not methName.endswith('__') else pubClsMethCond

            if callerCls is None or isinstance(callerCls, OldStyleClsType):
                yield codeObj.co_filename, frame.f_lineno, methName
            else:
                # PyCharm thinks defClsCond could be undefined, but if callerCls is not None it must be defined
                mroClsNs = list(mroClsNsGen(callerCls, defClsCond, methName, codeObj))
                if mroClsNs[-1] == 'object':  # Sometimes definer class not found so follow inheritance tree to the root
                    yield codeObj.co_filename, frame.f_lineno, methName
                else:
                    yield mroClsNs, methName

            frame = frame.f_back
            if not frame: break
            codeObj, fLocals = frame.f_code, frame.f_locals
            methName = codeObj.co_name

    @staticmethod
    def __splitLinkToStr(splitLink):  # type: (Union[Tuple[List[str], str], Tuple[str, int, str]]) -> str
        # REMINDER: Always add new line at the last possible moment, it's been tried before, it does not work!
        if len(splitLink) == 3:
            filePath, lineno, methName = splitLink
            splitFilePath = filePath.split(STAK.__pathSplitChar)
            if len(splitFilePath) > 1:
                return '{}{}.{}'.format(STAK.__join(splitFilePath[-2], splitFilePath[-1]).rstrip('py'), lineno, methName)
            else:
                return '{}{}.{}'.format(STAK.__join(splitFilePath[-1]).rstrip('py'), lineno, methName)
        else:
            return STAK.__mroLinkToStrLink(*splitLink)

    """ =============================================================================================================================== """

    """ ========================================= METHS CREATED IN RESPONSE TO FOMROLOCS  ============================================= """

    def __call__(self, frame, event, arg):  # type: (FrameType, str, Any) -> 'STAK'
        """ Used only to set an instance of STAK as a trace """

        if event == 'call' or event == 'return':
            print self.jointLinkFromFrame(frame), id(frame)
            self.traceEntry(event, frame)
        elif event == 'line' or event == 'exception':
            pass
        else:
            print 'ERROR: from STAK.__call__ unforeseen event string: {}'.format(event)

        return self

    def __traceEntry(self, flag, frame):  # type: (FrameType, str) -> None
        # All entries to trace log made through this method
        self.appendToTraceLog(
            (self.time(), flag, self.splitLinkFromFrame(frame))
        )

    @classmethod
    def __joinTraceEntriesFrom(cls):  # type: () -> Generator[None, Tuple[float, str, str], List[Union[int, str]]]
        oldTime, flag, jointLink = (yield)
        newTime = oldTime
        depth = 0
        callChain = [cls.unixStampToStr(oldTime), cls.traceFlag]

        while flag == 'call':
            if oldTime != newTime:
                callChain.append('<{}>{}'.format(int((newTime - oldTime) * 1000), jointLink))
                oldTime = newTime
            else:
                callChain.append(jointLink)
            depth += 1

            newTime, flag, jointLink = (yield)

        oldTime = newTime
        returnChain = [cls.unixStampToStr(oldTime), cls.traceFlag]

        while flag == 'return':
            pass

    @staticmethod
    def __formatTraceLog(
            callableNames,  # type: Set[str]
            splitLinkToStr,  # type: Callable[[Union[Tuple[List[str], str], Tuple[str, int, str]]], str]
            joinTraceEntriesUntilReversal,  # type: Callable[[], Generator[None, Tuple[float, str, str], List[Union[int, str]]]]
            traceLog,  # type: List[Tuple[float, str, Union[Tuple[List[str], str], Tuple[str, int, str]]]]
    ):  # type: (...) -> Iterator[str]

        # Receives the raw trace log, sends all the elements into the joiner, it joins one set of call entries &
        # one set of return entries, returning them as two log lines using the StopIteration exception.
        # Also in the return comes the final depth, which is used to start the next two lines at the right indent.
        # Once the joiner is exhausted it creates a new one, to handle the next two lines, and so on.

        joiner = joinTraceEntriesUntilReversal(); joiner.next()
        for unixStamp, flag, splitLink in traceLog:
            if splitLink[-1] in callableNames:
                continue  # If tracing any of STAKS' callables skip that

            try:
                joiner.send((unixStamp, flag, splitLink))
            except StopIteration as exc:
                callLine, returnLine, finalDepth = exc.message

    """ =============================================================================================================================== """

    """ ======================================================== SAVING LOGS ========================================================== """

    @staticmethod
    def __saveLogsToFile(makePathUnique, fileOpenMode, pathYielder, formatter, *logs):
        # type: (Callable[[str], str], str, PathGen, Callable[[Iterable], Iterable[str]], Iterable) -> None
        # Generic save method, most args populated by partial on init

        for path, log in zip(pathYielder(), logs):
            with open(makePathUnique(path), fileOpenMode) as logFile:
                logFile.writelines(formatter(log))

    def __trimFilePathAddLinenoGen(self,
        callChain,  # type: Tuple[Union[Tuple[str, int, str], Tuple[List[str], str]], ...]
    ):              # type: (...) -> Tuple[Union[Tuple[str, str], Tuple[List[str], str]], ...]

        pathSplitChar = self.pathSplitChar
        for link in callChain:
            if len(link) == 2:
                yield link
            else:
                filePath, lineno, methName = link
                splitPath = filePath.split(pathSplitChar)
                yield (
                    '{}{}{}{}'.format(
                        splitPath[-2],
                        pathSplitChar,
                        splitPath[-1].rstrip('py'),
                        lineno
                    ),
                    methName
                )

    def __preProcessLogGen(self,
            log,  # type: List[Tuple[float, str, Union[str, Tuple[Union[Tuple[str, int, str], Tuple[List[str], str]], ...]]]]
    ):  # type: (...) -> Iterator[Tuple[StrsStamp, str, Union[str, Tuple[Union[Tuple[str, str], Tuple[List[str], str]], ...]]]]

        unixStampToMid, omrolocsFlag = self.unixStampToTupleOfStrs, self.stakFlags[0]
        for unixStamp, flag, theRest in log:
            if flag == omrolocsFlag:
                yield unixStampToMid(unixStamp), flag, tuple(self.trimFilePathAddLineno(theRest))
            else:
                yield unixStampToMid(unixStamp), flag, theRest

    def __strLinkCallChainGen(self,
            log,  # type: Tuple[Tuple[StrsStamp, str, Union[Tuple[List[str], str], Tuple[str, int, str], str]]]
            linker  # type: Callable[List[str], str]
    ):  # type: (...) -> Iterator[Tuple[StrsStamp, str, Union[str, Tuple[str, ...]]]]

        omrolocsFlag = self.stakFlags[0]
        for stamp, flag, theRest in log:
            if flag == omrolocsFlag:
                yield stamp, flag, tuple(  # At this point theRest is the splitLinkCallChain
                    (
                        '{}.{}'.format(bigNameSpace, methName) if isinstance(bigNameSpace, str)
                        else linker(bigNameSpace[:], methName)
                        for bigNameSpace, methName in theRest
                    )
                )
            else:
                yield stamp, flag, theRest

    @staticmethod
    def __mroLinkToStrLink(mroClsNs, methName):  # type: (List[str], str) -> str
        mroClsNs[-1] = '{}.{}{}\n'.format(mroClsNs[-1], methName, ')' * (len(mroClsNs) - 1))
        return '('.join(mroClsNs)

    @staticmethod
    def __partStrLinkCreator(mroClsNs, methName):  # type: (List[str], str) -> str
        return '{}.{}'.format(mroClsNs[-1], methName)

    @staticmethod
    def __formatStakLog(
            stakFlags,      # type: Tuple[str, str, str, str]
            pStakFlags,     # type: Tuple[str, str, str, str]
            midStampToStr,  # type: Callable[[StrsStamp], str]
            logWhereIfCallChainStrLinks,  # type: Tuple[Tuple[StrsStamp, str, Union[str, List[str]]], ...]
    ):  # type: (...) -> Iterator[str]

        omrolocsFlag , dateFlag , dataFlag , labelFlag  = stakFlags
        pOmrolocsFlag, pDateFlag, pDataFlag, pLabelFlag = pStakFlags

        for stamp, flag, theRest in logWhereIfCallChainStrLinks:
            if flag == omrolocsFlag:
                yield '{}{}{}\n'.format(midStampToStr(stamp), pOmrolocsFlag, ' <- '.join(theRest))
            elif flag == dataFlag:
                yield '{}{}{}'.format(midStampToStr(stamp), pDataFlag, theRest)
            elif flag == labelFlag:
                yield theRest
            elif flag == dateFlag:
                yield '{}{}{}'.format(midStampToStr(stamp), pDateFlag, theRest)
            else:
                raise ValueError('Unsupported flag: {}'.format(flag))

    @staticmethod
    def __formatParsedStdLog(midStampToStr, pStdFlagsByStdFlags, parsedStdLog):
        # type: (Callable[[StrsStamp], str], Dict[str, str], Sequence[Tuple[StrsStamp, str, str]]) -> Iterator[str]

        for midStamp, stdFlag, theRest in parsedStdLog:
            yield '{}{}{}'.format(
                midStampToStr(midStamp),
                pStdFlagsByStdFlags[stdFlag],
                theRest,
            )

    @staticmethod
    def __midStampToStr(midStamp):  # type: (Tuple[str, str, str, str]) -> str
        return '{}:{}:{}.{}'.format(*midStamp)

    def __spliceGen(self,
        stdLog,  # type: Tuple[Tuple[StrsStamp, str, str]]
        log,     # type: Tuple[Tuple[StrsStamp, str, str]]
    ):           # type: (...) -> Iterator[Tuple[StrsStamp, str, str]]

        stdIdx, stakIdx = 0, 0
        stdElLeft, stakElLeft = True, True
        lenStd, lenStak = len(stdLog), len(log)
        allPflagsByFlags = self.allPflagsByFlags

        stdStamp, stdFlag, stdTheRest = stdLog[stdIdx]
        stamp   , flag   , theRest    = log[stakIdx]

        while stdElLeft or stakElLeft:

            if stdElLeft is True and (stdStamp <= stamp or stakElLeft is False):
                yield stdStamp, allPflagsByFlags[stdFlag], stdTheRest
                stdIdx += 1
                if stdIdx == lenStd:
                    stdElLeft = False
                else:
                    newStamp, stdFlag, stdTheRest = stdLog[stdIdx]
                    if newStamp is not None:
                        stdStamp = newStamp

            if stakElLeft is True and (stdStamp > stamp or stdElLeft is False):
                yield stamp, allPflagsByFlags[flag], theRest
                stakIdx += 1
                if stakIdx == lenStak:
                    stakElLeft = False
                else:
                    stamp, flag, theRest = log[stakIdx]

    def __saveSplicedToVariants(self,
        stdLogs,  # type: Tuple[Tuple[Tuple[StrsStamp, str, str]]]
        stakLog,  # type: Tuple[Tuple[StrsStamp, str, str]]
    ):            # type: (...) -> List[List[Tuple[StrsStamp, str, str]]]
        splicedLogs, pStdFlagsByStdFlags = [], self.pStdFlagsByStdFlags
        for stdLog, logName in zip(stdLogs, self.stdLogFiles):

            path = self.makeFilePathUnique(
                self.join(
                    next(self.pathDirVari()), self.addSuffix(logName, 'Splice')
                )
            )

            # Need this to be list bc compression
            splicedLog = list(self.spliceStakLogWithStdLog(stdLog, stakLog))
            splicedLogs.append(splicedLog)

            with open(path, 'w') as f:
                f.writelines(
                    (
                        '{}:{}:{}.{}'.format(*stamp) + flag + theRest
                        for stamp, flag, theRest in splicedLog
                    )
                )

        return splicedLogs

    def __saveCompressedStakLogToVariants(self,
        logWhereIfCallChainItsStrLinksAreCompressed  # type: Tuple[Tuple[StrsStamp, str, str]]
    ):
        with open(
                self.__fileUnique(
                    self.__join(
                        next(self.__genPathDirVari()), 'stakCompress.log')
                ),
                'w'
        ) as f:
            f.writelines(
                self.__compressLines(
                    [entry[-1] for entry in logWhereIfCallChainItsStrLinksAreCompressed]
                )
            )

    def __saveCompressedSplicedLogs(self, splicedLogs):
        # type: (List[List[Union[Tuple[datetime, str], Tuple[datetime, str, str]]]]) -> None

        for log, name in zip(splicedLogs, self.stdLogFiles):
            with open(
                    self.makeFilePathUnique(
                        self.join(
                            next(self.pathDirPrint()), name
                        )
                    ), 'w'
            ) as f:
                f.writelines(
                    self.compressLines(
                        [el[-1] for el in log]
                    )
                )

    """ =============================================================================================================================== """

    """ ========================================================= COMPRESSION ========================================================= """

    class _CompressionFormatList(list):
        # List that holds extra attributes for internal use in compression

        def __init__(self, cnt=1, rep='', *args):  # type: (int, str, Any) -> None
            super(STAK._CompressionFormatList, self).__init__(args)
            self.cnt = cnt
            self.rep = rep

    def __compressLinksGen(self,
        callChainsWithStrLinks  # type: Tuple[Tuple[StrsStamp, str, Union[str, Tuple[str, ...]]]]
    ):                          # type: (...) -> Iterator[Tuple[StrsStamp, str, str]]

        omrolocsFlag, prettyfyLine, compress = self.stakFlags[0], self.prettyfyLine, self.compress
        CompressionFormatList = self.CompressionFormatList
        return (
            (
                stamp,
                flag,
                prettyfyLine(
                    compress(
                        CompressionFormatList(1, 'line', *theRest)
                    )
                ).rstrip(' <- ') + '\n'
                if flag == omrolocsFlag else theRest,
            )
            for stamp, flag, theRest in callChainsWithStrLinks
        )

    def __compressLines(self, lines):  # type: (List[str]) -> List[str]
        return self.prettyfyLines(
            self.compress(
                self.formatLinesForLinesCompression(
                    lines
                )
            )
        )

    @classmethod
    def __prettyfyLine(cls, lineCfl):  # type: (_CompressionFormatList) -> str
        result = ''

        if lineCfl.cnt > 1:
            result += '{}x['.format(lineCfl.cnt)

        for el in lineCfl:
            if isinstance(el, cls.CompressionFormatList):
                assert el.rep == 'line'
                result += cls.prettyfyLine(el)
            elif isinstance(el, str):
                result += (el + ' <- ')
            else:
                raise TypeError('Wrong type in compressed stack: type(el)', type(el))

        if lineCfl.cnt > 1:
            result = result.rstrip(' <- ')
            result += (']' + ' <- ')

        return result

    @classmethod
    def __prettyfyLines(cls, linesCfl, depth=0):
        indent = depth * '    '
        result = []

        if linesCfl.cnt > 1:
            result.append('{}{}x\n'.format((depth - 1) * '    ', linesCfl.cnt))

        for el in linesCfl:
            if isinstance(el, cls._CompressionFormatList):
                assert el.rep == 'parsedLines'
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
        return cls._CompressionFormatList(1, 'parsedLines', *lines)

    def __compress(self, postPassCfl):
        represents = postPassCfl.rep

        for groupSize in range(1, min(len(postPassCfl) // 2, self._maxCompressGroupSize)):

            prePassCfl = postPassCfl
            postPassCfl = self._CompressionFormatList(cnt=prePassCfl.cnt, rep=prePassCfl.rep)

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

                        compressed_group = self._CompressionFormatList(groups_cnt, represents, *thisGroup)
                        postPassCfl.append(compressed_group)

                        thisGroupStartI = nextGroupStartI
                        thisGroupEndI = nextGroupEndI

                        nextGroupStartI += groupSize
                        nextGroupEndI += groupSize

                        groups_cnt = 1

                thisGroup = prePassCfl[thisGroupStartI: thisGroupEndI + 1]
                nextGroup = prePassCfl[nextGroupStartI: nextGroupEndI + 1]

        return postPassCfl

    """ =============================================================================================================================== """

    """ ======================================================= PARSING STD LOGS ===================================================== """

    @staticmethod
    def __interpolStampGen(prevLine, thisLine, nextLine):  # type: (OptStr9, OptStr9, OptStr9) -> Iterator[str]
        expectedChars = (4, 2, 2, 2, 2, 2, 3)
        for i, numChars in enumerate(expectedChars):
            prevEl, nextEl = prevLine[i], nextLine[i]
            if prevEl is None and nextEl is None:
                yield ' ' * numChars
            if prevEl is not None:
                if nextEl is not None:
                    yield str((int(prevEl) + int(nextEl)) // 2).zfill(numChars)
                else:
                    yield prevEl
            else:
                yield nextEl

        yield thisLine[-2]
        yield thisLine[-1]

    def __parseAndInterpolLines(self, lines):  # type: (List[str]) -> List[OptStr9]
        parsedLines = list(self.parseLines(lines))

        range6 = range(6)
        def isStampCutoff(parsedLine): # type: (OptStr9) -> bool
            """ This makes sense, trust me bro """
            for j in range6:
                if parsedLine[j] is None:
                    return True
            return False

        interpolStampGen = self.interpolMissingStamps
        lenLines, nones9 = len(parsedLines), (None, None, None, None, None, None, None, None, None)
        for parsedLine in parsedLines:

            if isStampCutoff(parsedLine):
                thisLineIndex = parsedLines.index(parsedLine)  # Only expecting to interpolate < 1% of parsedLines
                prevLineIndex, nextLineIndex = thisLineIndex - 1, thisLineIndex + 1
                prevLine, nextLine = nones9, nones9

                while isStampCutoff(prevLine) and prevLineIndex < lenLines:
                    prevLine = parsedLines[prevLineIndex]
                    prevLineIndex -= 1

                while isStampCutoff(nextLine) and nextLineIndex < lenLines:
                    nextLine = parsedLines[nextLineIndex]
                    nextLineIndex += 1

                parsedLines[thisLineIndex] = tuple(
                    interpolStampGen(prevLine, parsedLine, nextLine)
                )

        return parsedLines

    @staticmethod
    def __splitStampFromTheRest(lines):  # type: (List[Str9]) -> Iterator[Tuple[Str4, str, str]]
        for year, month, day, hour, minute, second, millisec, flag, theRest in lines:
            yield (
                (hour, minute, second, millisec),
                flag,
                theRest,
            )

    def __trimFlagIfPoss(self, line):  # type: (str) -> Tuple[str, str]
        wholeEnoughs, cutoffCombos, cutoffFlag = self.wholeEnoughs, self.cutoffCombos, self.cutoffFlag
        line = line.lstrip()
        for combo in cutoffCombos:
            if line.startswith(combo):
                line = line.lstrip(combo)
                if cutoffCombos[combo] > 1:
                    return line, cutoffFlag
                return line, wholeEnoughs[combo]
        return line, cutoffFlag

    def __trimFlag(self, line):  # type: (str) -> str
        for combo in self.stdFlags:
            if line.startswith(combo):
                return line.lstrip(combo)
        return line

    @staticmethod
    def __trimTime(line, matchTuple):  # type: (str, OptStr8) -> str
        numsTrimChars = (25, 20, 17, 14, 11, 8, 5, 0)
        for i, prefixEl in enumerate(matchTuple):
            if prefixEl is not None:

                while not line.startswith(prefixEl):
                    line = line[1:]

                return line[numsTrimChars[i + 1] if i < 7 and matchTuple[i + 1] is None else numsTrimChars[i]:]

    def __parsedLinesGen(self, lines):
        # type: (List[str]) -> Iterator[OptStr, OptStr, OptStr, OptStr, OptStr, OptStr, OptStr, OptStr, str]
        matcher, trimTime, trimFlag = self.matcher, self.trimTime, self.trimFlag
        trimFlagIfPoss = self.trimFlagIfPoss
        nones8 = (None, None, None, None, None, None, None, None)

        for line in lines:
            match = matcher(line)
            matchTuple = match.groups() if match else nones8

            if matchTuple[4] is None and matchTuple[3] is not None:
                # Hour & minute may be mixed up if cutoff at certain point
                #            (year, month, day , hour  , minute       , second       , millisec     , flag
                matchTuple = (None, None , None, None  , matchTuple[3], matchTuple[5], matchTuple[6], matchTuple[7])

            if matchTuple[-1] is not None:
                line = trimTime(line, matchTuple)
                line = trimFlag(line)
                yield matchTuple + (line.lstrip(': '), )
            else:
                line, flag = trimFlagIfPoss(line)
                result = None, None, None, None, None, None, None, flag, line.lstrip(': ')
                yield result

    def __parsedStdLogGen(self):  # type: () -> Iterator[Tuple[Tuple[StrsStamp, str, str]]]
        for path in self.stdLogFiles:
            with open(path, 'r') as f:
                lines = f.readlines()
            parsedLines = self.parseAndInterpolLines(lines)
            yield tuple(self.splitStampFromTheRest(parsedLines))

    """ =============================================================================================================================== """

    """ =========================================================== PATH OPS ========================================================== """

    @classmethod
    def __addSuffix(cls, logName, suffix):  # type: (str, str) -> str
        name, ext = cls.splitext(logName)
        return '{}{}{}'.format(name, suffix, ext)

    @classmethod
    def __fileUnique(cls, path):  # type: (str) -> str
        # Increment an integer suffix until path of file (not dir) is unique
        fileName, ext = cls.splitext(
            cls.basename(path)
        )
        dirPath = cls.dirname(path)
        cnt = 0

        while cls.isfile(path):
            cnt += 1
            path = cls.join(
                dirPath, '{}{}{}'.format(fileName, cnt, ext)
            )

        return path

    # All path yielders should be methods, not properties, so they can be passed to other methods & called just in time.
    # Also, should be generators to make it easier to handle multiple & single path yields.
    ###################################################################################################################
    def __genPathDirPrint(self):  # type: () -> Iterator[str]
        yield self.join(self.rootDir, self.taskDir, self.printDir)

    def __genPathDirPrimi(self):  # type: () -> Iterator[str]
        yield self.join(next(self.pathDirPrint()), self.primitivesDir)

    def __genPathDirVari(self):  # type: () -> Iterator[str]
        yield self.join(next(self.pathDirPrint()), self.variantsDir)

    def __genPathLogStak(self):  # type: () -> Iterator[str]
        yield self.join(next(self.pathDirPrimi()), self.stakLogFile)

    def __genPathLogsStd(self):  # type: () -> Iterator[str]
        for logName in self.stdLogFiles:
            yield self.join(next(self.pathDirPrimi()), logName)

    def __genPathLogTrace(self):  # type: () -> Iterator[str]
        yield self.join(next(self.pathDirPrimi()), self.traceLogFile)

    """ =============================================================================================================================== """

    """ =========================================================== STAMP OPS ========================================================== """

    __unixStampToDatetime = __dt.fromtimestamp  # type: Callable[[float], datetime]

    @staticmethod
    def __datetimeToTupleOfInts(dtStamp):  # type: (datetime) -> Tuple[int, int, int, int]
        return dtStamp.hour, dtStamp.minute, dtStamp.second, dtStamp.microsecond//1000

    @staticmethod
    def __tupleOfIntsToTupleOfStrs(intsStamp):  # type: (Tuple[int, int, int, int]) -> Tuple[str, str, str, str]
        return (
            '{:02}'.format(intsStamp[0]),
            '{:02}'.format(intsStamp[1]),
            '{:02}'.format(intsStamp[2]),
            '{:03}'.format(intsStamp[3]),
        )

    @staticmethod
    def __tupleOfStrsToStr(strsStamp):  # type: (Tuple[str, str, str, str]) -> str
        return '{}:{}:{}.{}'.format(*strsStamp)

    @classmethod
    def __unixStampToTupleOfInts(cls, unixStamp):  # type: (float) -> Tuple[int, int, int, int]
        dtStamp = cls.unixStampToDatetime(unixStamp)
        return dtStamp.hour, dtStamp.minute, dtStamp.second, dtStamp.microsecond//1000

    @classmethod
    def __unixStampToTupleOfStrs(cls, unixStamp):  # type: (float) -> Tuple[str, str, str, str]
        dt = cls.unixStampToDatetime(unixStamp)
        return '{:02}'.format(dt.hour), '{:02}'.format(dt.minute), '{:02}'.format(dt.second), '{:03}'.format(dt.microsecond//1000)

    @classmethod
    def __unixStampToStr(cls, unixStamp):  # type: (float) -> str
        dtStamp = cls.unixStampToDatetime(unixStamp)
        return '{:02}:{:02}:{:02}.{:03}'.format(dtStamp.hour, dtStamp.minute, dtStamp.second, dtStamp.microsecond//1000)

    """ =============================================================================================================================== """

    """ =========================================================== SHORTCUTS ========================================================= """

    @property
    def s(self):
        """ Short for save() """
        self.save()

    @property
    def l(self):
        """ Short for label() """
        self.label()

    @property
    def c(self):
        """ Short for clear() """
        self.clear()

    @property
    def rp(self):
        """ Short for rmPrint() """
        self.rmPrint()

    """ =============================================================================================================================== """


if __name__ == '__main__':
    s = STAK()

    if testingWhat == 'stak':
        def decorator(func):
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)
            return wrapper
        class Interface(object):
            def testCallerOfCaller(self): raise NotImplementedError()
        class Ganny(object): pass
        class Daddy(Ganny):
            def forMethNameDupBug(self): s.omrolocs()
            @decorator
            def test(self, someLocalParam=69):
                someOtherLocal = 'yesDaddy'
                s.omrolocsalad(someDatumForExtraLogging='420')
                somePostOmrolocsaladLocal = 'yes this is post the salad'
                s.omrolocs()
                s.data()
                s.data(someDatum=[1, 2, 3, 4])
                s.data(someDatum=[1, 2, 3, 4], someDatum2=[1, 2, 3, 4])
                s.data(pretty=True, someDatum=[1, 2, 3, 4], someDatum2=[1, 2, 3, 4])
                s.omropocs()
                s.autoLocals()
                s.data(SOME_SEPARATOR='================================================================================================')
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

                sleep(randint(0, maxSleepTime)/1000.0)

                with open(stdLogPaths[0], 'a') as f:
                    l1 = 'fdStamp' + ': ' + nonCompromisingLines[randint(0, 5)]
                    f.writelines(l1)

            with open(stdLogPaths[0], 'a') as f:
                f.writelines(cutOffLogs())
            with open(stdLogPaths[1], 'a') as f:
                f.writelines(cutOffLogs())

        def func2():
            a, b = 1, 2
            s.omrolocsalad()
            s.data(a=a, b=b)
            s.autoLocals()
        func2()
        Bro().forMethNameDupBug()

        genLogs()

    elif testingWhat == 'trace':

        def A():
            s.setTrace()
            B()
            s.delTrace()

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

