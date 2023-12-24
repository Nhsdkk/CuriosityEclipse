import math
from dataclasses import dataclass
from math import sqrt, acos
from typing import Self

from shared.point import Point


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

    def calculate_angle(self, other: Self) -> float:
        """
        Calculate angle between two vectors.

        :param other: second vector
        :return: angle between two vectors
        """
        x, other_x = self.end.x - self.start.x, other.end.x - other.start.x
        y, other_y = self.end.y - self.start.y, other.end.y - other.start.y
        z, other_z = self.end.z - self.start.z, other.end.z - other.start.z
        cos = abs(x * other_x + y * other_y + z * other_z) / (self.modulo * other.modulo)
        return math.degrees(acos(cos))
