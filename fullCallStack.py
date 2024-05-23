""" Call STACK() from meth to fugly print, technically STACKs' callstack minus the first frame"""
from inspect import stack

def STACK():
    frames = stack()[1:]; OGMN = frames[0][3]
    OGCN = next((c.__name__ for c in frames[0][0].f_locals['self'].__class__.__mro__ if OGMN in c.__dict__), None)
    p = ['START_CALLSTACK: {}.{} -----------------------------------------------------------'.format(OGCN, OGMN)]
    excl = ('excl', 'f', '__builtins__', '__file__', '__package__', '__doc__')
    for f in frames:
        lV = str({k: str(v).split(' at 0x')[0] for k, v in f[0].f_locals.items() if k not in excl and v})
        code = ' '.join(line.lstrip().rstrip('\n') for line in f[4]) if f[4] else ''
        p.append('[STAK] {}{}{}{}{}{}{}{}{}'.format(f[1], ', ln ', str(f[2]), ', ', f[3], ', ', code, ', ', lV))
    p.append('END_CALLSTACK: {}.{} ---------------------------------------------------------'.format(OGCN, OGMN))
    print '\n'.join(p)


class TestGanny(object): pass
class TestDaddy(TestGanny):
    def test(self): STACK()
    def testCaller(self): self.test()
class Test(TestDaddy):
    def testCallerOfCaller(self): self.testCaller()
class TestBro(TestDaddy): pass
class TestDawg(Test): pass


TestDawg().testCallerOfCaller()


