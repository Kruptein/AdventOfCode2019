from __future__ import annotations
from functools import partial
from typing import Dict, List, Optional, Tuple

from .utils import load_rows, split_row

ORBIT_MAP: Dict[str, O] = {}


class O:
    def __init__(self, name: str, direct_orbits: List[O]) -> None:
        self.name = name
        self.direct_orbits = direct_orbits
        self.orbittors: List[O] = []

    def __repr__(self) -> str:
        return self.name

    def orbit(self, o: O) -> None:
        self.direct_orbits.append(o)
        o.orbittors.append(self)

    @property
    def indirect_orbits(self) -> List[O]:
        return [
            orbits
            for neighbour in self.direct_orbits
            for orbits in neighbour.all_orbits
        ]

    @property
    def indirect_orbittors(self) -> List[O]:
        return [
            orbits for neighbour in self.orbittors for orbits in neighbour.all_orbittors
        ]

    @property
    def all_orbits(self) -> List[O]:
        return [*self.direct_orbits, *self.indirect_orbits]

    @property
    def all_orbittors(self) -> List[O]:
        return [*self.orbittors, *self.indirect_orbittors]


def process(input_list: List[str]) -> None:
    for inp in input_list:
        a, b = inp.strip("\n").split(")")
        if a not in ORBIT_MAP:
            ORBIT_MAP[a] = O(a, [])
        if b not in ORBIT_MAP:
            ORBIT_MAP[b] = O(b, [])
        ORBIT_MAP[b].orbit(ORBIT_MAP[a])


def find_path(a: O, b: O, visitors: Optional[List[O]] = None) -> Tuple[int, bool]:
    if visitors is None:
        visitors = []
    visitors.append(a)
    if b in a.direct_orbits or b in a.orbittors:
        return 0, True
    for neighbour in [*a.direct_orbits, *a.orbittors]:
        if neighbour in visitors:
            continue
        path = find_path(neighbour, b, visitors)
        if path[1]:
            return path[0] + 1, True
    return 0, False


if __name__ == "__main__":
    ex_data = load_rows("ex6.in", str)
    data = load_rows("day6.in", str)

    process(ex_data)
    assert len(ORBIT_MAP["D"].all_orbits) == 3
    assert len(ORBIT_MAP["L"].all_orbits) == 7
    assert len(ORBIT_MAP["COM"].all_orbits) == 0
    assert find_path(ORBIT_MAP["COM"], ORBIT_MAP["H"]) == (2, True)

    ORBIT_MAP = {}
    process(data)
    print(sum(len(orbit.all_orbits) for orbit in ORBIT_MAP.values()))
    print(find_path(ORBIT_MAP["SAN"], ORBIT_MAP["YOU"])[0] - 1)
