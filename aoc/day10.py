import math
import sys
from collections import Counter, defaultdict
from itertools import combinations
from typing import List, Tuple

from .utils import load_rows


def on_segment(a: Tuple[int], b: Tuple[int], c: Tuple[int]) -> bool:
    x = (c[1] - a[1]) * (b[0] - a[0]) - (c[0] - a[0]) * (b[1] - a[1])
    
    if abs(x) > sys.float_info.epsilon:
        return False
    
    return min(a[0], b[0]) <= c[0] <= max(a[0], b[0]) and min(a[1], b[1]) <= c[1] <= max(a[1], b[1])


def can_see(a: Tuple[int], b: Tuple[int], board: List[Tuple[int]]) -> bool:
    for asteroid in board:
        if asteroid == a or asteroid == b: continue
        if on_segment(a, b, asteroid):
            return False
    return True


def find_max(board: List[List[str]]) -> int:
    asteroid_vision = Counter()
    for asteroid, other in combinations(board, 2):
        if can_see(asteroid, other, board):
            asteroid_vision[asteroid] += 1
            asteroid_vision[other] += 1
    return asteroid_vision.most_common()[0]


def build_board(data: List[str]) -> List[Tuple[int]]:
    return [ (i, j) for j, x in enumerate(data) for i, y in enumerate(x) if y == '#' ]


def vaporize(board: List[Tuple[int]], origin: Tuple[int]):
    destroyed = []
    angled_board = defaultdict(list)
    for el in board:
        a = math.atan2(origin[1] - el[1], el[0] - origin[0])
        if a < 0: a += math.pi * 2
        angled_board[a].append(el)
    AK = sorted(angled_board.keys())
    index = next(i for i, k in enumerate(AK) if k >= math.pi / 2)
    while len(destroyed) < 200:
        destroyed.append(min(angled_board[AK[index]], key=lambda a: (abs(a[0] - origin[0]), abs(a[1] - origin[1]))))
        index -= 1
        if index < 0: index = len(AK) - 1
    return destroyed[199][0] * 100 + destroyed[199][1]


if __name__ == "__main__":
    data = load_rows("day10.in", str)

    test = """.#..##.###...#######
##.############..##.
.#.######.########.#
.###.#######.####.#.
#####.##.#.##.###.##
..#####..#.#########
####################
#.####....###.#.#.##
##.#################
#####.##.###..####..
..######..##.#######
####.##.####...##..#
.#####..#.######.###
##...#.##########...
#.##########.#######
.####.#.###.###.#.##
....##.##.###..#####
.#.#.###########.###
#.#.#.#####.####.###
###.##.####.##.#..##"""
    board = build_board(test.splitlines())
    asteroid, count = find_max(board)
    assert count == 210
    assert vaporize(board, asteroid) == 802

    board = build_board(data)
    asteroid, count = find_max(board)
    print(count)
    print(vaporize(board, asteroid))
