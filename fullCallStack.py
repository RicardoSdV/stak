""" Paste in meth to fugly print the callstack """
from inspect import stack

def STACK():
    frames, stackList = stack()[1:], []; OGMN = frames[0][3]
    OGCN = next((c.__name__ for c in frames[0][0].f_locals['self'].__class__.__mro__ if OGMN in c.__dict__), None)
    localsExcl = ('localsExcl', 'frame', 'stack_info', '__builtins__', '__file__', 'Trak', '__package__')
    for frame in frames:
        frameObj, filePath, lineNum, methName, codeList = frame[0], frame[1], frame[2], frame[3], frame[4]
        localVars = str(
            {k: str(v).split(' at 0x')[0] for k, v in frameObj.f_locals.items() if k not in localsExcl and v})
        codeStr = ' '.join(line.lstrip().rstrip('\n') for line in codeList) if codeList else ''
        stackList.append(
            '[STAK] {}{}{}{}{}'.format(filePath, ', ln ' + str(lineNum), ', ' + methName, ', ' + codeStr,
                                       ', ' + localVars
                                       ).lstrip(', '))
    print 'START_CALLSTACK: {}.{} -----------------------------------------------------'.format(OGCN, OGMN)
    print '\n'.join(stackList)
    print 'END_CALLSTACK: {}.{} -------------------------------------------------------'.format(OGCN, OGMN)


class TestGanny(object): pass
class TestDaddy(TestGanny):
    def test(self): STACK()
    def testCaller(self): self.test()
class Test(TestDaddy):
    def testCallerOfCaller(self): self.testCaller()
class TestBro(TestDaddy): pass
class TestDawg(Test): pass


TestDawg().testCallerOfCaller()


