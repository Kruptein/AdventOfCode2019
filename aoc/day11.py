from collections import defaultdict
from dataclasses import dataclass
from functools import partial
from sys import stdout
from typing import Dict, List, Set, Tuple

from .day9 import RelativeIntcode
from .utils import load_rows, split_row


DIR = [
    (0, -1),
    (-1, 0),
    (0, 1),
    (1, 0),
]


@dataclass
class State:
    position: Tuple[int]
    direction: int
    panels_counted: Set[Tuple[int]]
    brain: RelativeIntcode
    board: Dict[Tuple[int], str]

    @property
    def colour(self) -> int:
        return 1 if self.board[self.position] == '#' else 0
    
    @colour.setter
    def colour(self, new_value: int) -> None:
        self.board[self.position] = '#' if new_value == 1 else '.'
        self.panels_counted.add(self.position)
    
    def rotate(self, direction: int) -> None:
        self.direction = (self.direction + (1 if direction == 1 else -1)) % len(DIR)
    
    def step(self) -> None:
        self.position = self.position[0] + DIR[self.direction][0], self.position[1] + DIR[self.direction][1]


def move(data: List[int], state: State) -> int:
    while next(state.brain) != -1:
        state.colour = state.brain.send(state.colour)
        state.rotate(next(state.brain))
        state.step()
    return len(state.panels_counted)


if __name__ == "__main__":
    data = load_rows("day11.in", partial(split_row, int))[0]

    init_state = State(
        position=(0, 0),
        direction=0,
        panels_counted=set(),
        brain=RelativeIntcode(data[:], []).yield_process(),
        board=defaultdict(lambda : '.')
    )

    init_state = State(
        position=(0, 0),
        direction=0,
        panels_counted=set(),
        brain=RelativeIntcode(data, []).yield_process(),
        board=defaultdict(lambda : '.')
    )
    init_state.board[(0, 0)] = '#'
    move(data, init_state)
    
    for j in range(min(y for _, y in init_state.panels_counted), max(y for _, y in init_state.panels_counted) + 1):
        for i in reversed(range(min(x for x, _ in init_state.panels_counted), max(x for x, _ in init_state.panels_counted) + 1)):
            if (i, j) in init_state.board:
                stdout.write(init_state.board[(i, j)])
            else:
                stdout.write(" ")
        stdout.write("\n")