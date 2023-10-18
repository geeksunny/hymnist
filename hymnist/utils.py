class PostInitCaller(type):
    """Metaclass to add a call to __post_init__() after the constructor finishes."""

    def __call__(cls, *args, **kwargs):
        obj = type.__call__(cls, *args, **kwargs)
        obj.__post_init__()
        return obj
