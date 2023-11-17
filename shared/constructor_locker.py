class ConstructorLocker(type):
    """
    Metaclass to make private constructor
    """

    def __call__(cls, *args, **kwargs) -> None:
        """
        Raise error when trying to call class constructor

        :param args: args
        :param kwargs: kwargs
        :return: None
        """
        raise TypeError(
            f"{cls.__module__}.{cls.__qualname__} has no public constructor"
        )
