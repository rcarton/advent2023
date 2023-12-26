import io

from advent.days.day20 import Modules, first, parse_input, second
from advent.utils import get_data_for_day

data11 = """broadcaster -> a, b, c
%a -> b
%b -> c
%c -> inv
&inv -> a"""

data12 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output"""

data2 = """broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> rx"""


def test_first():
    assert first(io.StringIO(data11)) == 32000000
    assert first(io.StringIO(data12)) == 11687500


def test_second():
    assert second(io.StringIO(data12)) == 0


def test_second_data():
    assert second(get_data_for_day(20)) == 0


def print_tree(modules: Modules, m_name: str, past: list[str] = None):
    past = past if past is not None else []
    if len(past) > 2:
        return
    pad = "  " * len(past)
    rec = m_name in past
    mm = modules.get(m_name, None)
    print(
        pad
        + f" {mm.mtype if mm else ''}{m_name if m_name != 'broadcaster' else ''}{'*' if rec else ''}"
    )

    if rec:
        return

    sources = []
    for m in modules.values():
        if m_name in m.dests:
            sources.append(m.name)
    new_past = past + [m_name]
    for s_name in sources:
        print_tree(modules, s_name, new_past)


def test_view_tree():
    data = get_data_for_day(20)
    modules = parse_input(data)
    print()
    print_tree(modules, "rx")
