from traceback import print_stack

def dep2(imports):
    def decorator(func):
        return
    return decorator


def dep(**import_map):
    print 'dep'
    def decorator(func):
        print 'decorator'
        def wrapper(*args, **kwargs):
            print 'wrapper'
            deps = {}
            for name, path in import_map.items():
                module_path, _, attr = path.partition(':')
                mod = __import__(module_path, fromlist=[attr] if attr else [])
                deps[name] = getattr(mod, attr) if attr else mod

            old_defaults = func.func_defaults or ()
            arg_names = func.func_code.co_varnames
            num_defaults = len(old_defaults)
            num_args = func.func_code.co_argcount

            new_defaults = list(old_defaults)
            default_offset = num_args - num_defaults

            for name, value in deps.items():
                try:
                    idx = arg_names.index(name)
                    pos = idx - default_offset
                    if pos < 0:
                        new_defaults = [None] * (-pos) + new_defaults
                        pos = 0
                    new_defaults[pos] = value
                except ValueError:
                    pass

            func.func_defaults = tuple(new_defaults)

            func.func_code = func.func_code

            return func(*args, **kwargs)
        return wrapper
    return decorator


@dep(json='json', os='os', join='os.path:join', test2='src.function_dependency.test2:test2')
def do_something(data, json=None, os=None, join=None, test2=None):
    print_stack()
    print('CWD:', os.getcwd())
    print('Serialized:', json.dumps(data))
    print('Joined:', join('a', 'b'))


do_something((1,2,4))
