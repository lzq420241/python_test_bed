from functools import wraps as original_wraps

def wraps(func):
    def inner(f):
        f = original_wraps(func)(f)
        f.__wrapped__ = func
        return f
    return inner

class _patch(object):

    attribute_name = None
    _active_patches = set()

    def __init__(
            self, getter, attribute
        ):
        self.getter = getter
        self.attribute = attribute
        self.new = new

    def __call__(self, func):
        if isinstance(func, ClassTypes):
            return self.decorate_class(func)
        return self.decorate_callable(func)

    def decorate_callable(self, func):

        @wraps(func)
        def patched(*args, **keywargs):
            # don't use a with here (backwards compatability with Python 2.4)
            extra_args = []
            entered_patchers = []

            # can't use try...except...finally because of Python 2.4
            # compatibility
            exc_info = tuple()
            try:
                try:
                    for patching in patched.patchings:
                        arg = patching.__enter__()
                        entered_patchers.append(patching)
                        if patching.attribute_name is not None:
                            keywargs.update(arg)
                        elif patching.new is DEFAULT:
                            extra_args.append(arg)

                    args += tuple(extra_args)
                    return func(*args, **keywargs)
                except:
                    if (patching not in entered_patchers and
                        _is_started(patching)):
                        # the patcher may have been started, but an exception
                        # raised whilst entering one of its additional_patchers
                        entered_patchers.append(patching)
                    # Pass the exception to __exit__
                    exc_info = sys.exc_info()
                    # re-raise the exception
                    raise
            finally:
                for patching in reversed(entered_patchers):
                    patching.__exit__(*exc_info)

        patched.patchings = [self]
        if hasattr(func, 'func_code'):
            # not in Python 3
            patched.compat_co_firstlineno = getattr(
                func, "compat_co_firstlineno",
                func.func_code.co_firstlineno
            )
        return patched