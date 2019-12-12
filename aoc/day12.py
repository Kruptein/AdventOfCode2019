from collections import namedtuple
from copy import deepcopy
from functools import partial
from itertools import combinations
from math import gcd
from typing import List, Optional

from .utils import load_rows, split_row


def update_gravity(
    positions: List[List[int]], velocities: List[List[int]]
) -> List[List[int]]:
    for i, j in combinations(range(len(positions)), 2):
        for p in range(3):
            if positions[i][p] < positions[j][p]:
                velocities[i][p] += 1
                velocities[j][p] -= 1
            elif positions[i][p] > positions[j][p]:
                velocities[i][p] -= 1
                velocities[j][p] += 1
    return velocities


def update_velocity(
    positions: List[List[int]], velocities: List[List[int]]
) -> List[List[int]]:
    for moon in range(4):
        positions[moon] = [positions[moon][i] + velocities[moon][i] for i in range(3)]
    return positions


def update_energies(
    energies: List[List[int]], positions: List[List[int]], velocities: List[List[int]]
) -> List[int]:
    return [
        sum(abs(el) for el in positions[moon]) * sum(abs(el) for el in velocities[moon])
        for moon in range(4)
    ]


def _lcm(a: int, b: int) -> int:
    return abs(a * b) // gcd(a, b)


def lcm(numbers: List[int]) -> int:
    while len(numbers) > 1:
        numbers[:2] = [_lcm(numbers[0], numbers[1])]
    return numbers[0]


def simulate(positions: List[List[int]], step_count: Optional[int]) -> int:
    velocities = [[0, 0, 0] for _ in range(4)]
    og_pos = deepcopy(positions)
    energies: List[List[int]] = []
    cycles = [0, 0, 0]
    timestep = 0
    while True:
        velocities = update_gravity(positions, velocities)
        positions = update_velocity(positions, velocities)
        timestep += 1
        if step_count is None:
            for i in range(3):
                if all(positions[moon][i] == og_pos[moon][i] for moon in range(4)):
                    if cycles[i] == 0:
                        cycles[i] = timestep + 1
                    if all(j != 0 for j in cycles):
                        return lcm(cycles)
        else:
            energies.append(update_energies(energies, positions, velocities))
            if step_count == timestep:
                return sum(energies[-1])


if __name__ == "__main__":
    test = [[-1, 0, 2], [2, -10, -7], [4, -8, 8], [3, 5, -1]]
    data = [[6, 10, 10], [-9, 3, 17], [9, -4, 14], [4, 14, 4]]

    assert simulate(deepcopy(test), 10) == 179
    assert simulate(deepcopy(test), None) == 2772

    print(simulate(deepcopy(data), 1000))
    print(simulate(deepcopy(data), None))
