"""
This is a research project to see if future stacking is viable

Conclusions:
    - Of course its possible, this is how debuggers work duh

"""
from sys import settrace

def D(): print 'arrived at leaf D'
def C(): print 'arrived at leaf C'
def B(): C(); D()
def A(): B()


def trace(frame, event, arg):
    if event == 'call':
        print 'Function call: {}'.format(frame.f_code.co_name)
        print'  Line number: {}'.format(frame.f_lineno)
        print'  File name: {}'.format(frame.f_code.co_filename)
    elif event == 'return':
        print 'Function return: {}'.format(frame.f_code.co_name)
        print '  Line number: {}'.format(frame.f_lineno)
    elif event == 'line':
        print 'Line execution: {}'.format(frame.f_code.co_name)
        print '  Line number: {}'.format(frame.f_lineno)
    else:
        print 'Unknown event: {}'.format(event)
    print 'arg', arg, '\n'

    return trace

settrace(trace)

A()

settrace(None)