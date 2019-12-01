from typing import List

from .utils import load_rows

def calculate_mass(module: int) -> int:
    return (module // 3) - 2

def calculate_total_mass(modules: List[int]) -> int:
    return sum(calculate_mass(module) for module in modules)

if __name__ == '__main__':
    assert calculate_total_mass([12, 14, 1969, 100756]) == 2 + 2 + 654 + 33583
    print(calculate_total_mass(load_rows("day1.in", int)))
