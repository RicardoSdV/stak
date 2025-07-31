# This was written by chatGPT, works like shit, need to rewrite properly at some point.

def prettyLog(obj, indent=0, _visited=None, LOG=lambda *_, **__: None):

    if _visited is None:
        _visited = set()

    spacing = '    ' * indent
    if id(obj) in _visited:
        return
    _visited.add(id(obj))

    if isinstance(obj, dict):
        LOG(spacing + '{')
        for key, value in obj.iteritems():
            LOG(spacing + '    %s: ' % repr(key)),
            prettyLog(value, indent + 1, _visited)
        LOG(spacing + '}')
    elif isinstance(obj, (list, tuple, set)):
        open_char = '[' if isinstance(obj, list) else '(' if isinstance(obj, tuple) else '{'
        close_char = ']' if isinstance(obj, list) else ')' if isinstance(obj, tuple) else '}'
        LOG(spacing + open_char)
        for item in obj:
            prettyLog(item, indent + 1, _visited)
        LOG(spacing + close_char)
    elif hasattr(obj, '__dict__'):
        LOG(spacing + '%s {' % obj.__class__.__name__)
        prettyLog(obj.__dict__, indent + 1, _visited)
        LOG(spacing + '}')
    else:
        LOG(spacing + repr(obj))