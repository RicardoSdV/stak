"""
How to use:
- Copy-paste STAK in some high level utils type file & instantiate
- Import the STAK object to make log entries by calling omrolocs & data
- Need an interactive terminal, import STAK instance into it, & call help(instanceName)

Known issues:
- When renaming print files the auto incrementer does not find the correct last file

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
- (Easy) Support methods that contain both self and cls, for example, debug funcs and __new__.

- (Easy) Sometimes just need to know what lines have or have not been run, so do something like label but less big & with lineno

- (Hard) Given a class find where all of its instances live

- (Easy) Make a timing decorator, to check out how much it takes for example to save, or init

- (Easy) Many names are entirely too long, make them short

- (Easy) omrolocsalad, sometimes uses entirely too many lines to print one datum, automatically detect this & print in one line

- (Mid) auto-deject calls to STAK interface. WFT

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

- (Mid) When multiple processes are running the logs are separate, to have them joined write directly to file on entry & give a
flag name to each process to understand which process is producing the logs

- (Mid) Given an object find the class who instantiated it, & the entire mro from it towards object, in the "auto", fashion, obj-auto-data

- (Mid)(Facilitator) Split the different entries each in their own log, to make processing simpler, also, optionally print each
in their own file, but must keep entry order since entries might happen at the same timestamp

- (Mid) Inherit from datastructures, (list, dict, etc) & override __getitem__ & __setitem__ to log who is messing with them.

- (Mid) Somehow auto override, or not auto, __getattr__ & __setattr__ to effectively log how attr are being added dynamically
to objects

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

THE NEW LINE PROBLEM:
    Inserting new lines in the right place has lead to an unexpected amount of bugs, therefore,
    a radical conclusion has been arrived at:

    - ALL new lines should be stripped on parsing
    - NO new lines should be added, EVER, except:
    - ONE function should add all the new lines at the last possible moment right before saving logs to file.
    - A log will be considered to be composed of lines when the elements of the iterable are strings that end in a new line
    otherwise they will be considered composed of entries

Some considerations on performance:
    - Perf is important
    - Perf is much more important when gathering logs, than when formatting or saving logs
    - Less slow code is harder to maintain & extend

Open question:

    Is it better to make all the log entries into one list? or have one list per flag??

    One list:
        - Keeps order of entry
        - Needs to separate lists to make individual log

    Many lists:
        - Makes formatting easier
        - Needs to join lists to make a global log

    Conclusion:
        I think the way to go will be to have one unique log for all the entries to be made, & then they be separated during
        formatting, to then be rejoined during saving. Yes, I know, lol.

"""

from collections import OrderedDict
from datetime import datetime
from functools import partial
from re import compile
from os import makedirs as makedirs
from os.path import isdir, exists, join, splitext, basename, dirname, isfile
from shutil import rmtree
from sys import _getframe, settrace, gettrace
from time import time
from types import FunctionType, ClassType as OldStyleClsType

from typing import TYPE_CHECKING

""" ======================================================== NAMES REFERENCED ========================================================= """


""" =================================================================================================================================== """

""" =========================================================== OLD INTERFACE ========================================================= """

# Call-from-code interface
def omropocs():  # type: () -> None
    """ Its back! sometimes u just need the good old omropocs! in new & improved form! """
    # TODO: Try to make static maybe?
    print ' <- '.join(jointLinksCallChain())


def omrolocs(silence=False):  # type: (bool) -> None
    """ Optional Method Resolution Order Logger Optional Call Stack """
    if silence: return
    appendToLog(
        (
            time(),
            stakFlags[0],
            tuple(splitLinksCallChain()),
        )
    )

def data(pretty=False, **dataForLogging):  # type: (bool, Any) -> None
    """ Log data structures, their callable & definer class names """

    strLink = next(jointLinksCallChain())
    __data(pretty, strLink, **dataForLogging)

def omrolocsalad(silence=False, pretty=False, **additionalDataForLogging):  # type: (bool, bool, Any) -> None
    """ Optional Method Resolution Order Logger Optional Call Stack And Locals Auto Data """
    if silence: return

    linksAndFirstFrameLocalsFromFrameGen = linksAndFirstFrameLocalsFromFrame()
    firstFrameLocals = next(linksAndFirstFrameLocalsFromFrameGen)  # type: Dict[str, Any]

    for key, value in firstFrameLocals.iteritems():
        if key != 'self' and key != 'cls':
            additionalDataForLogging[key] = value

    splitLinks = tuple(linksAndFirstFrameLocalsFromFrameGen)
    firstLinkAsStr = __splitLinkToStr(splitLinks[0])

    appendToLog(
        (
            time(),
            stakFlags[0],
            splitLinks,
        )
    )

    __data(
        pretty,
        firstLinkAsStr,
        **additionalDataForLogging
    )

def autoLocals(silence=False, pretty=False, **additionalDataForLogging):  # type: (bool, bool, Any) -> None
    """ Logs locals from frame from which this method was called, optionally other kwargs """
    if silence: return

    linksAndFirstFrameLocalsFromFrameGen = linksAndFirstFrameLocalsFromFrame()
    firstFrameLocals = next(linksAndFirstFrameLocalsFromFrameGen)  # type: Dict[str, Any]

    for key, value in firstFrameLocals.iteritems():
        if key != 'self' and key != 'cls':
            additionalDataForLogging[key] = value

    firstLinkAsStr = __splitLinkToStr(next(linksAndFirstFrameLocalsFromFrameGen))
    __data(
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
#         return _dict.iteritems()
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
#             self.appendToLog((now, flag, '{}('.format(strLink)))
#             self.extendLog(
#                 (now, flag, '    {}={},'.format(name, datum))
#                 for name, datum in dataForLogging.iteritems()
#             )
#             self.appendToLog((now, flag, ')'))
#         else:
#             self.appendToLog((now, flag, '(No data was passed)'))
#     else:
#         self.appendToLog(
#             (
#                 self.time(),
#                 self.stakFlags[2],
#                 (
#                     '{}('.format(strLink) +
#                     ', '.join(('{}={}'.format(name, datum) for name, datum in dataForLogging.iteritems())) +
#                     ')'
#                 ) if dataForLogging else '{}('.format(strLink) + 'No data was passed)'
#             )
#         )

def setTrace():
    oldTrace = gettrace()
    if oldTrace is not '':
        traceOriginatorEntry(_getframe(1))
        settrace()

def delTrace():
    traceTerminatorEntry(_getframe(1))
    settrace(None)

# Call-from-shell interface

def label(label=None):  # type: (Optional[str]) -> None
    """ Make a log entry with the passed label, else, with next label in eventLabels, if any, else print no-name label """
    global eventCnt

    if label is None:
        if eventCnt < len(eventLabels):
            label = eventLabels[eventCnt]
            eventCnt += 1
        else:
            label = 'NO-NAME-LABEL-{}'.format(str(len(eventLabels) - eventCnt))

    appendToLog(
        (
            time(),
            stakFlags[3],
            '\n========================================================= {} '
            '=========================================================\n'.format(label)
        )
    )

def clearAll():  # type: () -> None
    """ DANGER: Clears current logs, stak & std. Resets self.eventCnt (label print count) & more """
    global eventCnt, log, appendToLog, extendLog

    for logPath in stdLogFiles:
        with open(logPath, 'w'): pass

    log = []
    appendToLog = log.append
    extendLog   = log.extend
    eventCnt = 0

    _dateEntry()

def removeCurrentPrint():  # type: () -> None
    """ MUCH DANGER: Remove current print dir & all its logs """
    if exists(next(pathDirPrint())):
        rmtree(next(pathDirPrint()))

# Call-from-self autoface
def _dateEntry():
    # Since normal entries only log time, this one is used to log date, normally on logging session init
    appendToLog((time(), stakFlags[1], datetime.now().strftime('%Y-%m-%d')))

""" =================================================================================================================================== """


_dateEntry()  # First log entry to log current date
