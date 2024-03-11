""" Paste this inside a method to pretty print its callstack & more """


print 'START CALLSTACK -------------------------------------------'
import inspect as ins
localsExcl = ('localsExcl', 'frame', 'stack_info', '__builtins__', '__file__', 'Trak', '__package__')
stackList = []
for frame in ins.stack():
    frameObj, filePath, lineNum, methName, codeList = frame[0], frame[1], frame[2], frame[3], frame[4]
    localVars = str(
        {k: str(v).split(' at 0x')[0] for k, v in frameObj.f_locals.items() if k not in localsExcl and v})
    codeStr = ' '.join(line.lstrip().rstrip('\n') for line in codeList) if codeList else ''
    stackList.append(
        '[STAK] {}{}{}{}{}\n'.format(filePath, ', ln ' + str(lineNum), ', ' + methName, ', ' + codeStr, ', ' + localVars
                              ).lstrip(', '))
print ''.join(stackList)
print 'END CALLSTACK ---------------------------------------------'



""" Simple """
import traceback
traceback.print_stack()