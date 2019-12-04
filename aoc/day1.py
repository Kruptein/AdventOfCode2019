from functools import lru_cache
from typing import List

from .utils import load_rows


def calculate_mass(module: int) -> int:
    return (module // 3) - 2


def calculate_total_mass(modules: List[int]) -> int:
    return sum(calculate_mass(module) for module in modules)


@lru_cache(maxsize=None)
def recursive_calculate_mass(module: int) -> int:
    mass = calculate_mass(module)
    return 0 if mass <= 0 else mass + recursive_calculate_mass(mass)


def calculate_total_mass2(modules: List[int]) -> int:
    return sum(recursive_calculate_mass(module) for module in modules)


if __name__ == "__main__":
    data = load_rows("day1.in", int)

    assert calculate_total_mass([12, 14, 1969, 100756]) == 2 + 2 + 654 + 33583
    print(calculate_total_mass(data))

    assert calculate_total_mass2([14, 1969, 100756]) == 2 + 966 + 50346
    print(calculate_total_mass2(data))
