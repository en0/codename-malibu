from .typing import IEventBus

def auto_wireup_events(ebus: IEventBus, obj: object):
    events = []
    for method in dir(obj):
        if method.startswith("on_"):
            meth = getattr(obj, method)
            events.append(meth)
            ebus.attach(method[3:].upper(), meth)
    return events

def counter(limit=-1):
    def _next_generator():
        i = 0
        while i != limit:
            i += 1
            yield i
    _ng = _next_generator()
    return lambda: next(_ng)
