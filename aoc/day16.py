from itertools import repeat
from typing import List

from .utils import load_rows


def process(phase: List[int], pattern: List[int]) -> List[int]:
    out = []
    for j in range(len(phase)):
        k = 0
        for i, l in enumerate(phase):
            k += phase[i] * pattern[((i + 1) // (j + 1)) % len(pattern)]
        out.append(int(str(k)[-1]))
    return out


def process2(phase: List[int], pattern: List[int], target: int) -> List[int]:
    for i in range(len(phase) - 2, target - 1, -1):
        phase[i] = (phase[i] + phase[i + 1]) % 10
    return phase


def load_sequence(str_seq: str) -> List[int]:
    return [int(x) for x in list(str_seq.strip())]


if __name__ == "__main__":
    data = load_rows("day16.in", load_sequence)[0] * 10_000

    pattern = [0, 1, 0, -1]

    for _ in range(100):
        data = process2(data, pattern, 5976809)
    print(data[5976809 : 5976809 + 8])
