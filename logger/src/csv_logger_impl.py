import pandas
from typing import Self


from logger.src.logger_interface import LoggerInterface
from shared.debugger import debug
from shared.singleton import singleton


@singleton
class CsvLogger(LoggerInterface):
    """Class for logger, which outputs to CSV file"""

    _columns: dict[str, list[float]] = {}
    _filename: str = None
    _instance: Self = None

    def __init__(self, filename: str = "out.csv"):
        """
        Public constructor

        :param filename: name of the file to write
        """
        self._filename = filename

    def _clean_data(self) -> None:
        """
        Ensure that all column arrays have the same size by appending zeroes at the end

        :return: None
        """
        max_length = max([len(self._columns[key]) for key in self._columns.keys()])

        for key in self._columns.keys():
            self._columns[key] += [0] * (max_length - len(self._columns[key]))

        return

    def dump(self):
        """
        Write data to csv file

        :return: None
        """
        self._clean_data()
        df = pandas.DataFrame.from_dict(self._columns)
        df.to_csv(self._filename, index=False, mode="a")

    @debug
    def log(self, variable_type: str, value: float) -> None:
        """
        Save value of the variable

        :param variable_type: Type, that allows us to assign variable to the group
        :param value: Value, that need to be saved
        :return: None
        """
        if variable_type not in self._columns:
            self._columns[variable_type] = [value]
        else:
            self._columns[variable_type].append(value)
