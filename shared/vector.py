from dataclasses import dataclass
from math import sqrt

from point import Point


@dataclass
class Vector:
    """Vector class for calculations"""

    start: Point
    end: Point
    modulo: float

    def __init__(self, start: Point, end: Point):
        """
        Public constructor

        :param start: start point of the vector
        :param end: end point of the vector
        """
        self.start = start
        self.end = end
        self.modulo = self._calculate_modulo()

    def _calculate_modulo(self) -> float:
        """
        Calculate vector modulo.

        :return: vector modulo
        """
        return sqrt(
            (self.start.x - self.end.x) ** 2
            + (self.start.y - self.end.y) ** 2
            + (self.start.z - self.end.z) ** 2
        )
