def fusion_list_process(f):
    """
    Map a Fusion list to a traditional list.

    Arguments:
        f : Callable - function to wrap

    Returns:
        Callable - wrapped function that maps output to a list

    This is used since FusionScript represents lists as
    dictionaries with 1-indexed integer keys.
    """

    def wrapper(*args, **kwargs):
        return [item[1] for item in sorted(f(*args, **kwargs).items())]

    return wrapper
