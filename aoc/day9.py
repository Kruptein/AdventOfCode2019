from functools import partial
from itertools import permutations
from typing import Generator, List

from .day7 import GeneratorIntCode
from .utils import load_rows, split_row


class InfiniteList(List[int]):
    def __getitem__(self, key):
        if key >= len(self):
            return 0
        return super().__getitem__(key)

    def __setitem__(self, key, value):
        if key >= len(self):
            self.extend([0 for _ in range(key - len(self) + 1)])
        return super().__setitem__(key, value)


class RelativeIntcode(GeneratorIntCode):
    def __init__(self, program: List[int], inp: List[int]):
        super().__init__(InfiniteList(program), inp)
        self.relative_base = 0
        self.operations[9] = self.adjust_relative_base

    def adjust_relative_base(self, modes: List[str]) -> None:
        self.relative_base += self.get_mode(1, modes)
        self.index += 2

    def get_mode(
        self, offset: int, modes: List[str], *, index_mode: bool = False
    ) -> int:
        if len(modes) + 1 > offset and modes[offset - 1] == "2":
            if index_mode:
                return self.get(offset) + self.relative_base
            return self.program[self.get(offset) + self.relative_base]
        return super().get_mode(offset, modes, index_mode=index_mode)


if __name__ == "__main__":
    data = load_rows("day9.in", partial(split_row, int))[0]

    test1 = RelativeIntcode(
        split_row(int, "1102,34915192,34915192,7,4,7,99,0"), []
    ).process()[0]
    assert len(str(test1)) == 16

    test2 = RelativeIntcode(split_row(int, "104,1125899906842624,99"), []).process()[0]
    assert test2 == 1125899906842624

    print(RelativeIntcode(data, [1]).process())
    print(RelativeIntcode(data, [2]).process())
