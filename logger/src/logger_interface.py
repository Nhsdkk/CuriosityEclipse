class LoggerInterface:
    """Interface for logger"""

    def log(self, variable_type: str, value: float) -> None:
        """
        Save value of the variable

        :param variable_type: Type, that allows us to assign variable to the group
        :param value: Value, that need to be saved
        :return: None
        """
        pass

    def dump(self) -> None:
        """
        Dump log content

        :return: None
        """
        pass
