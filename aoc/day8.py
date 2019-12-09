from sys import stdout
from typing import List

from .utils import load_rows


def part1(w: int, h: int, data: List[int]) -> int:
    layer_size = w * h
    rows = (data[i : i + layer_size] for i in range(0, len(data), layer_size))
    min_row = min(rows, key=lambda x: x.count(0))
    return min_row.count(1) * min_row.count(2)


def get_final_image(w: int, h: int, data: List[int]) -> List[int]:
    layer_size = w * h
    rows = [data[i : i + layer_size] for i in range(0, len(data), layer_size)]
    final_image = []

    for i in range(layer_size):
        final_image.append(next(row[i] for row in rows if row[i] != 2))
    return final_image


if __name__ == "__main__":
    data = load_rows("day8.in", lambda x: [int(y) for y in list(x)])[0]

    example = [int(x) for x in list("123456789012")]
    assert part1(3, 2, example) == 1

    print(part1(25, 6, data))

    assert get_final_image(2, 2, [int(x) for x in list("0222112222120000")]) == [
        0,
        1,
        1,
        0,
    ]

    image = get_final_image(25, 6, data)

    for j in range(6):
        for i in range(25):
            if image[j * 25 + i] == 1:
                stdout.write("1")
            else:
                stdout.write(" ")
        stdout.write("\n")
