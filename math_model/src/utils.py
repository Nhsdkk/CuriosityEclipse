from typing import Union


class InfiniteSolutionsError(Exception):
    pass


class NoSolutionsError(Exception):
    pass


def solve_quadratic(
    a: Union[float, int], b: Union[float, int], c: Union[float, int]
) -> tuple[float, float]:
    if not any([a, b, c]):
        raise InfiniteSolutionsError
    elif all([not a, not b, c]) or b ** 2 - 4 * a * c < 0:
        raise NoSolutionsError
    elif not (b**2 - 4 * a * c):
        return -b / (2 * a), -b / (2 * a)
    elif not a:
        return -c / b, -c / b
    else:
        roots = sorted(
            [
                (-b - (b**2 - 4 * a * c) ** 0.5) / (2 * a),
                (-b + (b**2 - 4 * a * c) ** 0.5) / (2 * a),
            ]
        )
        return roots[0], roots[1]
