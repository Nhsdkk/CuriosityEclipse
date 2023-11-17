from pandas import read_csv
from numpy import zeros

from logger.src.logger_interface import LoggerInterface


class CsvLogger(LoggerInterface):
    """
    Class for logger, which outputs to CSV file
    """

    _column_name_last_index_mapping: dict[str, int] = {}
    _filename: str = None

    def __init__(self, filename: str = "log.csv"):
        """
        :param filename: name of the file to write (by default "log.csv")
        """
        self._filename = filename

    def _write_fs(self, column_name: str, value: float, column_exists: bool = True):
        """
        Write data to csv file

        :param column_name: name of the column
        :param value: value of the variable
        :param column_exists: flag to check for column existence
        """
        with open(self._filename, "r") as file:
            df = read_csv(file)

        if not column_exists:
            if len(df.columns) == 0:
                df.insert(0, column_name, value, allow_duplicates=True)
                self._column_name_last_index_mapping[column_name] = 1
            else:
                rows_length = df.shape[0]
                df.insert(
                    len(df.columns),
                    column_name,
                    zeros(rows_length, float),
                    allow_duplicates=True,
                )
                self._column_name_last_index_mapping[column_name] = rows_length + 1
        else:
            index = self._column_name_last_index_mapping[column_name]
            rows_length = df.shape[0]
            if index <= rows_length:
                df.set_value(index, column_name, value)
            else:
                df.loc[index] = zeros(len(df.columns))
                df.set_value(index, column_name, value)

        df.to_csv(self._filename, index=False, mode="a")

    def log(self, variable_type: str, value: float) -> None:
        """
        Log the value of the variable

        :param variable_type: the variable group name to which this value will be assigned
        :param value: value of the variable
        """
        self._write_fs(
            variable_type, value, variable_type in self._column_name_last_index_mapping
        )
