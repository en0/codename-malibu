def counter(limit=-1):
    def _next_generator():
        i = 0
        while i != limit:
            i += 1
            yield i
    _ng = _next_generator()
    return lambda: next(_ng)
