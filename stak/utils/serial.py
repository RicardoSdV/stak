from ..const import exclFromLocals


def argsToStr(serializedArgs, commaJoin=', '.join):
    return commaJoin(
        k + '=' + v
        if k != 'noKeyFound'
        else v
        for k, v in serializedArgs
    )

def serializeArgs(frame, args, kwargs):
    args = iter(args)
    while args:
        k = next(args, 'noKeyFound')
        v = next(args, 'noValFound')

        if k == 'noKeyFound' and v == 'noValFound':
            break

        if k != 'noKeyFound' and v != 'noValFound':
            yield str(k), str(v)
            continue

        yield 'noKeyFound', str(k)

    # TODO: Theres a bug here where self gets to kwargs for some reason.
    for k, v in kwargs.iteritems():
        yield k, str(v)

    if not frame:
        return

    for k, v in frame.f_locals.iteritems():
        if k in exclFromLocals:
            continue

        if k in kwargs:
            continue

        yield k, str(v)
