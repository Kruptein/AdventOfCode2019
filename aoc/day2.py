from functools import partial
from itertools import product
from operator import add, mul
from typing import List

from .utils import load_rows, split_row


def process(integers: List[int]) -> int:
    def _(i: int) -> int:
        return integers[integers[i]]

    index = 0
    while (op_code := integers[index]) != 99:
        op = add if op_code == 1 else mul
        integers[integers[index + 3]] = op(_(index + 1), _(index + 2))
        index += 4
    return integers[0]


def find_pair(integers: List[int]) -> int:
    for noun, verb in product(range(1, 100), repeat=2):
        data = integers[:]
        data[1:3] = noun, verb
        if process(data) == 19690720:
            return 100 * noun + verb


if __name__ == '__main__':
    og_data = load_rows("day2.in", partial(split_row, int))[0]
    data = og_data[:]
    # Restore the gravity assist program to the 1202 program alarm
    data[1:3] = 12, 2

    assert process([1,0,0,0,99]) == 2
    assert process([2,3,0,3,99]) == 2
    assert process([2,4,4,5,99,0]) == 2
    assert process([1,1,1,4,99,5,6,0,99]) == 30
    print(process(data))

    print(find_pair(og_data))
