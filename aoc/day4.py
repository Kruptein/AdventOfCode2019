from collections import Counter
from typing import Optional


def find_passwords(start: int, end: int, *, group_limit: Optional[int] = None) -> int:
    matching = 0
    for i in range(start, end + 1):
        si = str(i)
        if group_limit:
            if 2 not in Counter(si).values():
                continue
        elif len(set(si)) == 6:
            continue
        if "".join(sorted(si)) != si:
            continue
        matching += 1
    return matching


if __name__ == "__main__":
    start = 123257
    end = 647015

    print(find_passwords(start, end))
    print(find_passwords(start, end, group_limit=2))
