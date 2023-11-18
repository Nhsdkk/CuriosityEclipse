from dataclasses import dataclass, field


@dataclass
class Point:
    """Point class for calculations"""

    x: float = field(default=0)
    y: float = field(default=0)
    z: float = field(default=0)
