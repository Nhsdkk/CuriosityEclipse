import matplotlib.pyplot as plt
from typing import Any
from numpy import ndarray, dtype


class GraphGenerator:
    """Graph generator class"""

    def __init__(self):
        pass

    @staticmethod
    def create_height_graph(
        t_arr: ndarray[Any, dtype], height_arr: ndarray[Any, dtype]
    ) -> None:
        """
        Create h(t) graph.

        :param t_arr: Time values array
        :param height_arr: Height values array
        :return: None
        """
        plt.title("Height (time) m / sec")
        plt.xlabel("Time (sec)")
        plt.ylabel("Height (m)")
        plt.grid()
        plt.plot(t_arr, height_arr)
        plt.show()

    @staticmethod
    def create_graph(
        plot_name: str,
        x_name: str, y_name: str,
        x_arr: ndarray[Any, dtype], y_arr: ndarray[Any, dtype],
    ) -> None:
        plt.title(plot_name)
        plt.xlabel(x_name)
        plt.ylabel(y_name)
        plt.grid()
        plt.plot(x_arr, y_arr)
        plt.show()