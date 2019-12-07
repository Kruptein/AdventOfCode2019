from functools import partial
from itertools import permutations
from typing import Generator, List

from .day5 import IntCodePlus
from .utils import load_rows, split_row


class GeneratorIntCode(IntCodePlus):
    def yield_process(self) -> Generator[int, int, None]:
        while (op_info := self.cursor) != 99:
            op_split = list(str(op_info))
            op_code = int("".join(op_split[-2:]))
            if op_code == 3 and not self.inp:
                new_inp = yield
                self.inp.append(new_inp)
            self.operations[op_code](op_split[-3::-1])
            if op_code == 4:
                yield self.outp[-1]
        yield -1

def test_phase(phases: List[int], data: List[int]) -> int:
    amplifiers = [ GeneratorIntCode(data[:], [p]).yield_process() for p in phases]
    next_input = 0
    while True:
        for i, ampl in enumerate(amplifiers):
            if next(ampl) == -1:
                return next_input;
            next_input = ampl.send(next_input)


def find_max(data: List[int], phase_range: List[int]) -> int:
    max_val = 0
    for perm in permutations(phase_range):
        signal = test_phase(perm, data[:])
        if max_val < signal: max_val = signal
    return max_val


if __name__ == "__main__":
    data = load_rows("day7.in", partial(split_row, int))[0]

    assert test_phase([4,3,2,1,0], split_row(int, "3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0")) == 43210
    assert test_phase([0,1,2,3,4], split_row(int, "3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0")) == 54321

    print(find_max(data[:], range(5)))

    assert test_phase([9,8,7,6,5], split_row(int, "3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5")) == 139629729
    assert test_phase([9,7,8,5,6], split_row(int, "3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10")) == 18216

    print(find_max(data[:], range(5, 10)))