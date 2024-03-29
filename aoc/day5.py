from functools import partial
from operator import eq, gt, lt, ne
from typing import Callable, List

from .day2 import Intcode
from .utils import load_rows, split_row


class IntCodePlus(Intcode):
    def __init__(self, program: List[int], inp: List[int]):
        super().__init__(program)
        self.inp = inp
        self.outp: List[int] = []
        self.operations[3] = self.input_op
        self.operations[4] = self.output_op
        self.operations[5] = partial(self.jump_zero, ne)
        self.operations[6] = partial(self.jump_zero, eq)
        self.operations[7] = partial(self.jump_param, lt)
        self.operations[8] = partial(self.jump_param, eq)

    def process(self) -> List[int]:
        super().process()
        return self.outp

    def get_mode(
        self, offset: int, modes: List[str], *, index_mode: bool = False
    ) -> int:
        if len(modes) + 1 <= offset or modes[offset - 1] == "0":
            if index_mode:
                return self.get(offset)
            return self.program[self.get(offset)]
        return self.get(offset, index_mode=index_mode)

    def simple_op(self, method: Callable[[int, int], int], modes: List[str]) -> None:
        self.program[self.get_mode(3, modes, index_mode=True)] = method(
            self.get_mode(1, modes), self.get_mode(2, modes)
        )
        self.index += 4

    def input_op(self, modes: List[str]) -> None:
        self.program[self.get_mode(1, modes, index_mode=True)] = self.inp.pop(0)
        self.index += 2

    def output_op(self, modes: List[str]) -> None:
        self.outp.append(self.get_mode(1, modes))
        self.index += 2

    def jump_zero(self, op: Callable[[int, int], int], modes: List[str]) -> None:
        if op(self.get_mode(1, modes), 0):
            self.index = self.get_mode(2, modes)
        else:
            self.index += 3

    def jump_param(self, op: Callable[[int, int], int], modes: List[str]) -> None:
        self.program[self.get_mode(3, modes, index_mode=True)] = int(
            op(self.get_mode(1, modes), self.get_mode(2, modes))
        )
        self.index += 4


if __name__ == "__main__":
    data = load_rows("day5.in", partial(split_row, int))[0]

    print(IntCodePlus(data[:], [1]).process())
    assert IntCodePlus(
        [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [0]
    ).process() == [0]
    assert IntCodePlus(
        [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [1]
    ).process() == [1]
    large_inp = load_rows("ex5.in", int)
    assert IntCodePlus(large_inp, [5]).process() == [999]
    assert IntCodePlus(large_inp, [8]).process() == [1000]
    assert IntCodePlus(large_inp, [10]).process() == [1001]
    print(IntCodePlus(data[:], [5]).process())

