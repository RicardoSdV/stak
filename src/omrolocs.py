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


Cool potential features:
    - If there are multiple methods in the call stack that have the same definer and caller class maybe print only
    one copy of the MRO and substitute in the other frames by ... or something. Actually might need the entire MRO.

    - Support finding caller definer & mro classes for static methods, private properties & wrapped methods

    - Somehow better prints for wrappers, would be cool to have CallerCls(DefinerCls.@decorator.methName)
    but im not sure there is a good way of getting the decorator, only the wrapper

    - Add an option to print the stack in multiple lines with indentation

    - wrap long stacks

    - Write a class do
"""

import code
import re
import types
from inspect import stack

from pathlib import Path

INDENT_STR = '    '


def compress_stack_lines_by_trav_and_mod_in_place(cfl):
    for i, el in enumerate(cfl):
        if isinstance(el, str):
            cfl[i] = compress(
                format_line_for_callstack_comp(el)
            )

        elif isinstance(el, CompressionFormatList) and el.rep == 'lines':
            compress_stack_lines_by_trav_and_mod_in_place(el)

        else:
            raise TypeError('Elements traversed in compress_stack_lines_by_trav_and_mod_in_place '
                            "should only be str or CompressionFormatList with cfl.rep == 'lines'")


def run(force_retrim=True, log_dir_path=r'C:\prjs\trimLog_develop\logs_dir_example'):
    log_paths = find_read_and_write_log_paths(force_retrim, log_dir_path)

    for read_path, write_path in log_paths:

        print 'read_path, write_path', read_path, write_path

        with open(read_path, 'r') as f:
            lines = f.readlines()
        if len(lines) < 1: continue

        remove_datetime_and_log_type_prefixes_from_lines_in_place(lines)

        lines_cfl = format_lines_for_lines_compression(lines)
        lines_cfl = compress(lines_cfl)

        compress_stack_lines_by_trav_and_mod_in_place(lines_cfl)
        trav_lines_pretty_stack_in_place(lines_cfl)

        pretty_lines = prettyfy_lines(lines_cfl)

        with open(write_path, 'w') as f:
            f.writelines(pretty_lines)



def trav_lines_pretty_stack_in_place(lines_cfl):
    for i, el in enumerate(lines_cfl):
        if isinstance(el, CompressionFormatList):
            if el.rep == 'line':
                lines_cfl[i] = prettyfy_line(el).rstrip(' <- ') + '\n'
            elif el.rep == 'lines':
                trav_lines_pretty_stack_in_place(el)
            else:
                raise TypeError("At the moment of writing this error there was only "
                                "two types of CompressionFormatList: 'line' & 'lines'")
        else:
            raise TypeError('In trav_lines_mod_cs_lines_in_place for loop there should only be CompressionFormatLists')


def prettyfy_line(line_cfl):
    result = ''

    if line_cfl.cnt > 1:
        result += '{}x['.format(line_cfl.cnt)

    for el in line_cfl:
        if isinstance(el, CompressionFormatList):
            assert el.rep == 'line'
            result += prettyfy_line(el)
        elif isinstance(el, str):
            result += (el + ' <- ')
        else:
            raise TypeError('Wrong type in compressed stack: type(el)', type(el))

    if line_cfl.cnt > 1:
        result = result.rstrip(' <- ')
        result += (']' + ' <- ')

    return result


def prettyfy_lines(lines_cfl, depth=0):
    indent = depth * INDENT_STR
    result = []

    if lines_cfl.cnt > 1:
        result.append('{}{}x\n'.format((depth-1) * INDENT_STR, lines_cfl.cnt))

    for el in lines_cfl:
        if isinstance(el, CompressionFormatList):
            assert el.rep == 'lines'
            result.extend(prettyfy_lines(el, depth + 1))
        elif isinstance(el, str):
            result.append(indent + el)
        else:
            raise TypeError('Wrong type in compressed list: type(el)', type(el))
    return result


def format_line_for_callstack_comp(line):
    return CompressionFormatList(
        line.rstrip('\n').split(' <- '),
        rep='line'
    )


def remove_datetime_and_log_type_prefixes_from_lines_in_place(lines):
    prefix_pattern = r"(\d{4}-\d{2}-\d{2}) (\d{2}):(\d{2}):(\d{2}).(\d{3,4}): (DEBUG:|INFO:|WARNING:|ERROR:).*$"

    for i, line in enumerate(lines):
        match = re.match(prefix_pattern, line)
        if match:
            ymd, hour, minute, sec, msec, log_flag = match.groups()

            line = line.replace(
                '{}{}{}{}{}{}{}{}{}{}{}{}'.format(
                    ymd, ' ', hour, ':', minute, ':', sec, '.', msec, ': ', log_flag, ' '
                ), '')

            lines[i] = line


def format_lines_for_lines_compression(lines):
    if not lines[-1].endswith('\n'):
        lines[-1] += '\n'
    return CompressionFormatList(lines, rep='lines')


def find_read_and_write_log_paths(force_retrim, log_dir_path):

    result = []
    for log_path in Path(log_dir_path).rglob('**/*.log'):

        if not log_path.name.startswith('t_'):
            trimmed_log_path = log_path.with_name('t_' + log_path.name)

            if not trimmed_log_path.exists() or force_retrim:
                result.append((log_path, trimmed_log_path))

    return result



def compress(post_pass_cfl):
    represents = post_pass_cfl.rep

    for group_size in range(1, len(post_pass_cfl) // 2):

        pre_pass_cfl = post_pass_cfl
        post_pass_cfl = CompressionFormatList(cnt=pre_pass_cfl.cnt, rep=pre_pass_cfl.rep)

        this_group_start_i = 0
        this_group_end_i = group_size - 1

        next_group_start_i = group_size
        next_group_end_i = 2 * group_size - 1

        this_group = pre_pass_cfl[this_group_start_i: this_group_end_i + 1]
        next_group = pre_pass_cfl[next_group_start_i: next_group_end_i + 1]

        groups_cnt = 1

        while this_group:

            if this_group == next_group:
                groups_cnt += 1

                next_group_start_i += group_size
                next_group_end_i += group_size

            else:
                if groups_cnt == 1:
                    post_pass_cfl.append(this_group[0])

                    this_group_start_i += 1
                    this_group_end_i += 1

                    next_group_start_i += 1
                    next_group_end_i += 1

                else:  # There has been one or more repetitions of this_group

                    compressed_group = CompressionFormatList(this_group, cnt=groups_cnt, rep=represents)
                    post_pass_cfl.append(compressed_group)

                    this_group_start_i = next_group_start_i
                    this_group_end_i = next_group_end_i

                    next_group_start_i += group_size
                    next_group_end_i += group_size

                    groups_cnt = 1

            this_group = pre_pass_cfl[this_group_start_i: this_group_end_i + 1]
            next_group = pre_pass_cfl[next_group_start_i: next_group_end_i + 1]

    return post_pass_cfl



class CompressionFormatList(list):
    def __init__(self, cnt=1, rep='', *args):
        super(CompressionFormatList).__init__(*args)
        self.cnt = cnt
        self.rep = rep


class STAK(object):
    """
    callChain = [link1, link2, ...] Every link represents a call or, frame in the inspect.stack

    link = (
        i=0 -> mroClsNs: tuple -> (callerCls, ancestorOfCallerCls, ..., definerCls) if caller & definer found else None
        i=1 -> methName: str
        i=2 -> fileName: str
        i=3 -> lineNum: int
    )

    """

    def __init__(self):
        self.log = []

        # Capture Settings
        None

        # Save Settings (cwd == bin paths relative)
        self.savePath = 'default.log'
        self.saveFile = 'default.log'
        self.saveFolder = ''


    """============================================ CAPTURING LOGS PHASE ============================================"""

    def omrolocs(self, callStackDepth=999, silence=False, flags=()):
        if silence: return

        callChain = [self.__linkCreator(*frame) for frame in stack()[1:callStackDepth]]

        self.log.append(callChain)

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

    def save(self, path=None, name=None, forceNewDepthOf=None, inclMRO=True):
        if path is None:
            if name is None:
                path = self.savePath
            else:
                path = self.saveFolder + name

        with open(path, 'w') as f:
            f.writelines(self.__linesGenerator(forceNewDepthOf, inclMRO))

    def __linesGenerator(self, forceNewDepthOf, inclMRO):
        for callChain in self.log:
            if isinstance(forceNewDepthOf, int):
                callChain = callChain[:forceNewDepthOf]

            yield ' <- '.join(self.__lineGenerator(callChain, forceNewDepthOf, inclMRO))

    @staticmethod
    def __lineGenerator(callChain, forceNewDepthOf, inclMRO):
        for mroClsNs, methName, fileName, lineNum in callChain[: forceNewDepthOf]:
            if mroClsNs is None:
                yield fileName.replace('.py', str(lineNum)) + '.' + methName
            elif inclMRO:
                mroClsNs[-1] = mroClsNs[-1] + '.' + methName + ')' * (len(mroClsNs) - 1)
                yield '('.join(mroClsNs)
            else:
                yield mroClsNs[-1] + '.' + methName

    """=============================================================================================================="""


stak = STAK()







while True:
    variables = globals().copy()
    variables.update(locals())
    shell = code.InteractiveConsole(variables)
    shell.interact()


















































# end
