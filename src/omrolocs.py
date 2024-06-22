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

    - If the class object autopassed to a class method is not called 'cls' defaults to filename & lineno

    - If the method is defined in an old style class, it defaults to filename & lineno


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
                        trimLog1Splice.log
                        |                   <- The normal non_compromising.log a program may or may not produce spliced with stak.log & trimmed
                        trimLog2Splice.log
                        |
                        primitives_dir <- Dir to hold all the data used to create the above logs
                            |
                            stak.log <- stak info by itself
                            |
                            non_compromising_1.log
                            |                       <- The normal logs but only in the stak.log time period
                            non_compromising_2.log

        Since at the moment calling omrolocs requires modifying the code, and since modifying the code, at the moment
        requires restarting the program, some pathops will be triggered in the __init__

"""

import code
import os
import re
import types
from datetime import datetime
from inspect import stack
from pathlib import Path

from src.funcs.someCode import SomeClass


class STAK(object):
    """
    self.log = [(timeStr, callChain), ...]

    callChain = [link1, link2, ...] Every link represents a call or, frame in the inspect.stack

    link = (
        i=0 -> mroClsNs: tuple -> (callerCls, ancestorOfCallerCls, ..., definerCls) if caller & definer found else None
        i=1 -> methName: str
        i=2 -> fileName: str
        i=3 -> lineNum: int
    )

    """

    def __init__(self):
        self.__log = []

        # Save Settings (cwd == bin paths relative)
        self.__dirRoot    = '.STAK'
        self.__dirTask    = 'task'
        self.__dirPrnt    = 'print'
        self.__dirPrim    = 'primitives'
        self.__dirStdLogs = ('stdLog1.log', 'stdLog2.log')

        self.__makeDirs()

    """============================================ CAPTURING LOGS PHASE ============================================"""

    def omrolocs(self, callStackDepth=999, silence=False, flags=()):
        if silence: return
        now = datetime.now()
        timeStr = now.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

        callChain = [self.__linkCreator(*frame)for frame in stack()[1:callStackDepth]]

        self.__log.append((timeStr, callChain))
    @classmethod
    def __linkCreator(cls, frameObj, filePath, lineNum, methName, _, __):
        fLocals = frameObj.f_locals

        callerCls = None
        if 'self' in fLocals:
            callerCls = fLocals['self'].__class__
            defClsCond = cls.__privInsMethCond if cls.__isPrivate(methName) else cls.__pubInsMethCond
        elif 'cls' in fLocals:
            callerCls = fLocals['cls']
            defClsCond = cls.__privClsMethCond if cls.__isPrivate(methName) else cls.__pubClsMethCond

        if callerCls is None or isinstance(callerCls, types.ClassType):
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
                isinstance(attr, types.FunctionType)
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

    def save(self, path=None, name=None, forceNewDepthOf=None, inclMRO=True, trim=False):
        self.__saveRawStakLogToPrimitives()
        self.__saveStdLogsInStakPeriodToPrimitives()

    def __saveRawStakLogToPrimitives(self):
        def linesGenerator():
            for timeStr, callChain in self.__log:
                yield timeStr + ': ' + ' <- '.join(lineGenerator(callChain))
        def lineGenerator(callChain):
            for mroClsNs, methName, fileName, lineNum in callChain:
                if mroClsNs is None:
                    yield fileName.replace('.py', str(lineNum)) + '.' + methName
                else:
                    mroClsNs = mroClsNs[:]
                    mroClsNs[-1] = mroClsNs[-1] + '.' + methName + ')' * (len(mroClsNs) - 1)
                    yield '('.join(mroClsNs)

        rawStakLogPath = os.path.join(self.__dirRoot, self.__dirTask, self.__dirPrnt, self.__dirPrim, 'stak.log')
        rawStakLogPath = self.__ifPathExistsIncSuffix(rawStakLogPath)

        with open(rawStakLogPath, 'w') as f:
            f.writelines(linesGenerator())
    def __saveStdLogsInStakPeriodToPrimitives(self):
        pass

    """=============================================================================================================="""

    """==================================================COMPRESSION================================================="""

    class CompressionFormatList(list):
        """ List that holds extra attributes for internal use in compression"""
        def __init__(self, cnt=1, rep='', *args):
            super(STAK.CompressionFormatList, self).__init__(*args)
            self.cnt = cnt
            self.rep = rep
    @classmethod
    def __compressStackLinesByTravAndModInPlace(cls, cfl):
        for i, el in enumerate(cfl):
            if isinstance(el, str):
                cfl[i] = cls.__compress(
                    cls.__formatLineForCallstackComp(el)
                )

            elif isinstance(el, cls.CompressionFormatList) and el.rep == 'lines':
                cls.__compressStackLinesByTravAndModInPlace(el)

            else:
                raise TypeError('Elements traversed in compress_stack_lines_by_trav_and_mod_in_place '
                                "should only be str or CompressionFormatList with cfl.rep == 'lines'")
    @classmethod
    def __run(cls, force_retrim=True, log_dir_path=r'C:\prjs\trimLog_develop\logs_dir_example'):
        log_paths = cls.__findReadAndWriteLogPaths(force_retrim, log_dir_path)

        for read_path, write_path in log_paths:

            with open(read_path, 'r') as f:
                lines = f.readlines()
            if len(lines) < 1: continue

            cls.__removeDatetimeAndLogTypePrefixesFromLinesInPlace(lines)

            lines_cfl = cls.__formatLinesForLinesCompression(lines)
            lines_cfl = cls.__compress(lines_cfl)

            cls.__compressStackLinesByTravAndModInPlace(lines_cfl)
            cls.__travLinesPrettyStackInPlace(lines_cfl)

            prettyLines = cls.__prettyfyLines(lines_cfl)

            with open(write_path, 'w') as f:
                f.writelines(prettyLines)
    @classmethod
    def __travLinesPrettyStackInPlace(cls, linesCfl):
        for i, el in enumerate(linesCfl):
            if isinstance(el, cls.CompressionFormatList):
                if el.rep == 'line':
                    linesCfl[i] = cls.__prettyfyLine(el).rstrip(' <- ') + '\n'
                elif el.rep == 'lines':
                    cls.__travLinesPrettyStackInPlace(el)
                else:
                    raise TypeError("At the moment of writing this error there was only "
                                    "two types of CompressionFormatList: 'line' & 'lines'")
            else:
                raise TypeError(
                    'In trav_lines_mod_cs_lines_in_place for loop there should only be CompressionFormatLists')
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
    def __formatLineForCallstackComp(cls, line):
        return cls.CompressionFormatList(
            line.rstrip('\n').split(' <- '),
            rep='line'
        )
    @classmethod
    def __removeDatetimeAndLogTypePrefixesFromLinesInPlace(cls, lines):
        prefixPattern = r"(\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2}):(\d{2}).(\d{3,4}): (DEBUG:|INFO:|WARNING:|ERROR:).*$"

        for i, line in enumerate(lines):
            match = re.match(prefixPattern, line)
            if match:
                ymd, hour, minute, sec, msec, log_flag = match.groups()

                line = line.replace(
                    '{}{}{}{}{}{}{}{}{}{}{}{}'.format(
                        ymd, ' ', hour, ':', minute, ':', sec, '.', msec, ': ', log_flag, ' '
                    ), '')

                lines[i] = line
    @classmethod
    def __formatLinesForLinesCompression(cls, lines):
        if not lines[-1].endswith('\n'):
            lines[-1] += '\n'
        return cls.CompressionFormatList(lines, rep='lines')
    @classmethod
    def __findReadAndWriteLogPaths(cls, forceRetrim, logDirPath):
        result = []
        for logPath in Path(logDirPath).rglob('**/*.log'):

            if not logPath.name.startswith('t_'):
                trimmedLogPath = logPath.with_name('t_' + logPath.name)

                if not trimmedLogPath.exists() or forceRetrim:
                    result.append((logPath, trimmedLogPath))
        return result
    @classmethod
    def __compress(cls, postPassCfl):
        represents = postPassCfl.rep

        for groupSize in range(1, len(postPassCfl) // 2):

            prePassCfl = postPassCfl
            postPassCfl = cls.CompressionFormatList(cnt=prePassCfl.cnt, rep=prePassCfl.rep)

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

                        compressed_group = cls.CompressionFormatList(cnt=groups_cnt, rep=represents, *thisGroup)
                        postPassCfl.append(compressed_group)

                        thisGroupStartI = nextGroupStartI
                        thisGroupEndI = nextGroupEndI

                        nextGroupStartI += groupSize
                        nextGroupEndI += groupSize

                        groups_cnt = 1

                thisGroup = prePassCfl[thisGroupStartI: thisGroupEndI + 1]
                nextGroup = prePassCfl[nextGroupStartI: nextGroupEndI + 1]

        return postPassCfl

    """=============================================================================================================="""

    """=================================================== PATH OPS ================================================="""

    def changePath(self, root=None, task=None, prnt=None, prim=None, stdLogs=None):
        """ Can live change paths, new dirs are created if don't exist """
        if root is not None: self.__dirRoot    = root
        if task is not None: self.__dirTask    = task
        if prnt is not None: self.__dirPrnt    = prnt
        if prim is not None: self.__dirStdLogs = stdLogs
        self.__makeDirs()
    def __makeDirs(self):
        fullPath = os.path.join(self.__dirRoot, self.__dirTask, self.__dirPrnt, self.__dirPrim)
        if not os.path.isdir(fullPath):
            os.makedirs(fullPath)
    @staticmethod
    def __ifPathExistsIncSuffix(path):
        fileName, ext = os.path.splitext(os.path.basename(path))
        dirPath = os.path.dirname(path)
        cnt = 0
        while os.path.isfile(path):
            cnt += 1
            path = os.path.join(dirPath, '{}{}{}'.format(fileName, cnt, ext))
        return path

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
OldStyle().oldStyleInstanceMeth()



while True:
    variables = globals().copy()
    variables.update(locals())
    shell = code.InteractiveConsole(variables)
    shell.interact()


















































# end
