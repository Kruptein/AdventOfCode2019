from itertools import product
from typing import List, Optional, Tuple

from .utils import load_rows, split_row


Point = Tuple[int, int]
Segment = Tuple[Point, Point]


def advance_line(point: Point, op: str) -> Point:
    direction, distance = op[0], int(op[1:])
    if direction == "R":
        return point[0] + distance, point[1]
    if direction == "L":
        return point[0] - distance, point[1]
    if direction == "U":
        return point[0], point[1] + distance
    return point[0], point[1] - distance


def order_segment(a: Point, b: Point) -> Segment:
    if a[0] == b[0]:
        if a[1] < b[1]:
            return a, b
        return b, a
    if a[0] < b[0]:
        return a, b
    return b, a


def calc_segments(line: List[str]) -> List[Segment]:
    last_point = (0, 0)
    segments = []
    for op in line:
        new_point = advance_line(last_point, op)
        segments.append(order_segment(last_point, new_point))
        last_point = new_point
    return segments


def get_intersection(a: Segment, b: Segment) -> Optional[Point]:
    if a[0][0] == a[1][0] and b[0][0] <= a[0][0] <= b[1][0] and a[0][1] <= b[0][1] <= a[1][1]:
        return a[0][0], b[0][1]
    elif a[0][1] == a[1][1] and b[0][1] <= a[0][1] <= b[1][1] and a[0][0] <= b[0][0] <= a[1][0]:
        return b[0][0], a[0][1]


def find_intersections(a, b):
    for c, d in product(a, b):
        intersection = get_intersection(c, d)
        if intersection is not None and intersection != (0, 0):
            yield intersection


def manhattan(p: Point) -> int:
    return abs(p[0]) + abs(p[1])


def find_closest_intersection(rows: List[List[str]]) -> Point:
    closest_intersection = None, None
    for intersection in find_intersections(*(calc_segments(row) for row in rows)):
        m = manhattan(intersection)
        if closest_intersection[0] is None or closest_intersection[1] > m:
            closest_intersection = intersection, m
    return closest_intersection[0][0] + closest_intersection[0][1]


def point_on_segment(point: Point, segment: Segment) -> bool:
    if segment[0][0] == segment[1][0]:
        return point[0] == segment[0][0] and segment[0][1] <= point[1] <= segment[1][1]
    return point[1] == segment[0][1] and segment[0][0] <= point[0] <= segment[1][0]


def calc_signal_delay(lines: List[List[str]], intersection: Point) -> int:
    total = 0
    for line in lines:
        x, y = 0, 0
        for op in line:
            i = 0
            direction, distance = op[0], int(op[1:])
            while (x, y) != intersection and i < distance:
                if direction == "R":
                    x += 1
                elif direction == "L":
                    x -= 1
                elif direction == "U":
                    y += 1
                else:
                    y -= 1
                i += 1
                total += 1
    return total


def find_shortest_intersection(rows: List[str]) -> Point:
    shortest_intersection = None
    segments = [calc_segments(row) for row in rows]
    for intersection in find_intersections(*segments):
        sd = calc_signal_delay(rows, intersection)
        if shortest_intersection is None or shortest_intersection > sd:
            shortest_intersection = sd
    return shortest_intersection


if __name__ == '__main__':
    data = load_rows("day3.in", split_row())

    assert find_closest_intersection([["R8","U5","L5","D3"], ["U7","R6","D4","L4"]]) == 6
    assert find_closest_intersection([split_row()("R75,D30,R83,U83,L12,D49,R71,U7,L72"), split_row()("U62,R66,U55,R34,D71,R55,D58,R83")]) == 159
    assert find_closest_intersection([split_row()("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"), split_row()("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7")]) == 135

    print(find_closest_intersection(data))

    assert find_shortest_intersection([["R8","U5","L5","D3"], ["U7","R6","D4","L4"]]) == 30
    assert find_shortest_intersection([split_row()("R75,D30,R83,U83,L12,D49,R71,U7,L72"), split_row()("U62,R66,U55,R34,D71,R55,D58,R83")]) == 610
    assert find_shortest_intersection([split_row()("R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51"), split_row()("U98,R91,D20,R16,D67,R40,U7,R15,U6,R7")]) == 410

    print(find_shortest_intersection(data))