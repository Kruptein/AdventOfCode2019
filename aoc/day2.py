from functools import partial, partialmethod
from itertools import product
from operator import add, mul
from typing import Callable, Dict, List, Optional

from .utils import load_rows, split_row


class Intcode:
    def __init__(self, program: List[int]):
        self.program = program
        self.index = 0
        self.operations: Dict[int, Callable[[List[str]], None]] = {
            1: partial(self.simple_op, add),
            2: partial(self.simple_op, mul),
        }

    @property
    def cursor(self) -> int:
        return self.get(0)

    def get(self, offset: int) -> int:
        return self.program[self.index + offset]

    def process(self) -> int:
        while (op_info := self.cursor) != 99:
            op_split = list(str(op_info))
            self.operations[int("".join(op_split[-2:]))](op_split[-3::-1])
        return self.program[0]

    def simple_op(self, method: Callable[[int, int], int], modes: List[str]) -> None:
        self.program[self.get(3)] = method(
            self.program[self.get(1)], self.program[self.get(2)]
        )
        self.index += 4


def find_pair(integers: List[int]) -> Optional[int]:
    for noun, verb in product(range(1, 100), repeat=2):
        data = integers[:]
        data[1:3] = noun, verb
        if Intcode(data).process() == 19690720:
            return 100 * noun + verb
    return None


if __name__ == "__main__":
    og_data = load_rows("day2.in", partial(split_row, int))[0]
    data = og_data[:]
    # Restore the gravity assist program to the 1202 program alarm
    data[1:3] = 12, 2

    assert Intcode([1, 0, 0, 0, 99]).process() == 2
    assert Intcode([2, 3, 0, 3, 99]).process() == 2
    assert Intcode([2, 4, 4, 5, 99, 0]).process() == 2
    assert Intcode([1, 1, 1, 4, 99, 5, 6, 0, 99]).process() == 30
    # print(process(data))
    print(Intcode(data).process())

    print(find_pair(og_data))
