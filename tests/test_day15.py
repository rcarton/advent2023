import io
from dataclasses import dataclass
from typing import Generic, Optional, TypeVar

from advent.days.day15 import first, second

data = """rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7"""


def test_first():
    assert first(io.StringIO(data)) == 1320


def test_second():
    assert second(io.StringIO(data)) == 145
