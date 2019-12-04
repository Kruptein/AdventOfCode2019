import os
from pathlib import Path
from typing import Callable, List, TypeVar

T = TypeVar("T")

DATA_DIR = Path(os.path.dirname(__file__)) / ".." / "data"


def load_rows(file_name: str, transformation: Callable[[str], T]) -> List[T]:
    with open(DATA_DIR / file_name) as f:
        return list(map(transformation, f))


def split_row(
    transformation: Callable[[str], T], row: str, *, sep: str = ","
) -> List[T]:
    return [transformation(el) for el in row.split(sep)]
