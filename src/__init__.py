d = {'a': 1, 'b': 2}

def func(a=1, b=2):
    d2 = {
        'a': a,
        'b': b,
        's': 3,
        'd': 4,
    }
    print d2

def func2(**kwargs): pass

func(a=0, b=0)
func2(a=0, b=0)
