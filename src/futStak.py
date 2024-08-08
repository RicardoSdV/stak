"""
This is a research project to see if future stacking is viable

Conclusions:
    - Of course its possible, this is how debuggers work duh

    - Seems like once you set a trace and all the callables are called
    the trace returns to the original callable

"""
# from sys import settrace
#
# def E(param): print 'Leaf E'
# def D(): E('param')
# def C(): print 'Leaf C'
# def B(): C(); D()
# def A(): B()
#
#
# def trace(frame, event, arg):
#     print 'event: {}, name: {}, arg: {}'.format(event, frame.f_code.co_name, arg)
#     return trace
#
# settrace(trace)
#
# A()
#
# settrace(None)

class Class(object):
    def someOtherExample(self, **kwargs):
        print kwargs
c = Class()

class Class2(object):
    def example(self, someArg=None, someOtherArg='SomethingElse', **kwargs):
        print locals()

c2 = Class2()

c2.example()
