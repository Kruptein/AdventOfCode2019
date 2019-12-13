from enum import IntEnum
from functools import partial
from math import copysign
from typing import Generator, List, NamedTuple, Optional, Tuple

from .day9 import RelativeIntcode
from .utils import load_rows, split_row


class IntCodeState(IntEnum):
    OUTPUT = 0
    INPUT = 1
    ENDED = 2


class IntCodePause(NamedTuple):
    state: IntCodeState
    value: Optional[int]


class InfoIntCode(RelativeIntcode):
    def yield_process(self) -> Generator[IntCodePause, int, None]:
        while (op_info := self.cursor) != 99:
            op_split = list(str(op_info))
            op_code = int("".join(op_split[-2:]))
            if op_code == 3 and not self.inp:
                new_inp = yield IntCodePause(IntCodeState.INPUT, None)
                self.inp.append(new_inp)
                yield
            self.operations[op_code](op_split[-3::-1])
            if op_code == 4:
                yield IntCodePause(IntCodeState.OUTPUT, self.outp[-1])
        yield IntCodePause(IntCodeState.ENDED, None)


class Tile(IntEnum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


def process(data: List[int]) -> Tuple[int, int]:
    board = {}
    paddle_pos = (0, 0)
    ball_pos = (0, 0)
    score = 0
    processor = InfoIntCode(data, []).yield_process()
    while val := next(processor):
        if val.state == IntCodeState.ENDED:
            break
        if val.state == IntCodeState.OUTPUT:
            coords = (val.value, next(processor).value)
            if coords == (-1, 0):
                score = next(processor).value
            else:
                tile = next(processor).value
                board[coords] = tile
                if tile == Tile.BALL:
                    ball_pos = coords
                elif tile == Tile.PADDLE:
                    paddle_pos = coords
        else:
            x_diff = ball_pos[0] - paddle_pos[0]
            if x_diff == 0:
                processor.send(0)
            else:
                processor.send(int(copysign(1, x_diff)))
    return sum(1 for x in board.values() if x == Tile.BLOCK), score


if __name__ == "__main__":
    data = load_rows("day13.in", partial(split_row, int))[0]

    assert process([104, 1, 104, 2, 104, 3, 104, 6, 104, 5, 104, 4, 99])[0] == 0

    print(process(data[:]))

    data[0] = 2
    print(process(data))
