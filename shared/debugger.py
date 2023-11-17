from types import FunctionType


def debug(func: FunctionType) -> any:
    """
    Debugger decorator, that prints function args, kwargs and result

    :param func: any function
    :return: same function
    """

    def wrapper(*args, **kwargs) -> any:
        print(
            f"Function with name {func.__name__} was called with:\n\t1)args - {args}\n\t2)kwargs - {kwargs}"
        )
        try:
            result = func(*args, **kwargs)
            print(
                f"Function with name {func.__name__} returned result:\n\tresult - {result}"
            )
            return result
        except Exception as err:
            print(
                f"Function with name {func.__name__} finished with error:\n\terror - {err}"
            )
            raise err

    return wrapper
