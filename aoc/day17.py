"""
Forgive my insanity.

This solution solves everything programatically.
"""
from functools import partial
from itertools import product
from typing import List, Set, Tuple

from .day11 import DIR
from .day13 import InfoIntCode, IntCodeState
from .utils import load_rows, split_row


def p2(data: List[str]):
    out = set()
    i = 0
    j = 0
    line_width = 0
    start_pos = (0, 0)
    for el in data:
        if el in ["#", "<", ">", "v", "^"]:
            print(el, end="")
            out.add((i, j))
            if el != "#":
                start_pos = (i, j)
        elif el == chr(10):
            print()
            if line_width == 0:
                line_width = i
            i = -1
            j += 1
        elif el == ".":
            print(".", end="")
        else:
            print("WARNING")
        i += 1
    print()
    line_height = j
    k = []
    for i, j in out:
        if i > 0 and i < line_width - 1 and j > 0 and j < line_height - 1:
            if (i - 1, j) not in out or (i + 1, j) not in out:
                continue
            if (i, j - 1) not in out or (i, j + 1) not in out:
                continue
        else:
            continue
        k.append((i, j))
    return { 'board': out, 'intersections': k, 'start_pos': start_pos, 'alignment_sum': sum(i * j for i, j in k)}


def calc_path(board, start):
    old = start
    path = [(start, (0, 0))]
    while True:
        arms = []
        for i, j in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            coords = (start[0] + i, start[1] + j)
            if coords not in board or coords == old:
                continue
            arms.append((coords, (i, j)))
        if len(arms) == 1:
            path.append(arms[0])
        elif len(arms) > 1:
            for arm in arms:
                if arm[0][0] == start[0] == old[0] or arm[0][1] == start[1] == old[1]:
                    path.append(arm)
                    break
        else:
            break
        old = start
        start = path[-1][0]
    actual_path = []
    cur_dir = path[1][1]
    cur_count = 0
    next_rotato = "L"
    for coord, direction in path[1:]:
        if direction == cur_dir:
            cur_count += 1
        else:
            actual_path.append(next_rotato)
            actual_path.append(str(cur_count))
            if DIR[(DIR.index(cur_dir) + 3) % 4] == direction:
                next_rotato = "R"
            else:
                next_rotato = "L"
            cur_count = 1
            cur_dir = direction
    actual_path.append(next_rotato)
    actual_path.append(str(cur_count))

    s = ",".join(actual_path)
    for a in range(len(s)):
        a_s = s[:a]
        if len(a_s) > 20: continue
        T = s.replace(a_s, "")
        for b in range(len(T)):
            b_s = T[:b]
            if len(b_s) > 20: continue
            K = T.replace(b_s, "")
            for c in range(len(K)):
                c_s = K[:c]
                if len(c_s) > 20:
                    continue
                if len(K.replace(c_s, "")) == 0:
                    a_s = a_s.strip(",")
                    b_s = b_s.strip(",")
                    c_s = c_s.strip(",")
                    return { "A": a_s, "B": b_s, "C": c_s, "commands": s.replace(a_s, "A").replace(b_s, "B").replace(c_s, "C")}



def process(data: List[int]) -> List[str]:
    processor = InfoIntCode(data[:], []).yield_process()
    out = []
    while val := next(processor):
        if val.state == IntCodeState.ENDED:
            break
        if val.state == IntCodeState.OUTPUT:
            out.append(chr(val.value))
    out = p2(out)
    path = calc_path(out["board"], out["start_pos"])
    cmds = ["commands", "A", "B", "C"]
    path_cmd = 0
    data[0] = 2
    processor = InfoIntCode(data, []).yield_process()
    read_output = False
    while val := next(processor):
        if val.state == IntCodeState.ENDED:
            break
        if val.state == IntCodeState.OUTPUT:
            if read_output:
                try:
                    chr(val.value)
                except:
                    return out["alignment_sum"], val.value
        elif val.state == IntCodeState.INPUT:
            read_output = True
            if path_cmd < 4:
                for cmd in path[cmds[path_cmd]]:
                    processor.send(ord(cmd))
                    next(processor)    
            else:
                processor.send(ord("n"))
                next(processor)
            path_cmd += 1
            processor.send(10)


if __name__ == "__main__":
    data = load_rows("day17.in", partial(split_row, int))[0]
    
    print(process(data))