from shared.constructor_locker import ConstructorLocker


class LoggerInterface (metaclass=ConstructorLocker):
    """Interface for logger"""

    def log(self, variable_type: str, value: float) -> None:
        """
        Log the value of the variable

        :param variable_type: Type, that allows us to assign variable to the group
        :param value: Value, that need to be logged
        """
        pass
