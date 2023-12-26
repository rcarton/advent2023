import io

from advent.days.day21 import (
    ENTRIES,
    Garden,
    TOTAL_STEPS,
    count_reachable,
    first,
    how_many_steps_to_visit_all_from_entry,
    how_many_visitable,
    second,
)
from advent.utils import get_data_for_day

data = """...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
..........."""


def test_garden_get_index():
    g = Garden.from_string(data)
    # assert g[1, 0] == "."
    # assert g[1, -1] == "."
    assert g[1, -2] == g[1, -13] == "#"

    assert "".join(g[-2, i] for i in range(g.width)) == ".##..##.##."
    assert "".join(g[-2 - g.height, i] for i in range(g.width)) == ".##..##.##."


def test_how_many_steps_to_visit():
    g = Garden.from_string(get_data_for_day(21).read().strip())
    nw = (0, 0)
    n = (0, g.width // 2)
    ne = (0, g.width - 1)
    sw = (g.height - 1, 0)
    s = (g.height - 1, g.width // 2)
    se = (g.height - 1, g.width - 1)
    for entry in [nw, n, ne, sw, s, se]:
        print(how_many_steps_to_visit_all_from_entry(g, entry))
    assert how_many_steps_to_visit_all_from_entry(g, (0, 0)) == 0


def test_how_many_visitable():
    g = Garden.from_string(get_data_for_day(21).read().strip())
    print(how_many_visitable(g))

    print("Odd")
    for e, ec in ENTRIES.items():
        print(e, count_reachable(g, 261, ec))
    print("Even")
    for e, ec in ENTRIES.items():
        print(e, count_reachable(g, 260, ec))


def test_first():
    assert first(io.StringIO(data), 6) == 16


def brute_force(g: Garden, steps: int) -> int:
    return count_reachable(g, steps)


def test_second():
    # steps = TOTAL_STEPS
    g = Garden.from_string(get_data_for_day(21).read().strip())
    steps = (6 * g.width) + g.width // 2
    print(f"steps={steps}")
    g.unlimited = True
    bf_count = brute_force(g, steps)

    print(bf_count)
    # bf_count = 456232
    #
    assert second(get_data_for_day(21), steps) == bf_count


def test_brute_force():
    g = Garden.from_string(data)
    g.unlimited = True

    assert brute_force(g, 5000) == 16733044
