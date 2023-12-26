from dataclasses import dataclass
from typing import Callable, Literal, Optional, TextIO, Union
import re

from advent.intervals import Interval
from advent.utils import prod

WorkflowName = str
Category = Literal["x", "m", "a", "s"]
Outcome = Literal["A", "R"]
Result = Union[Outcome | WorkflowName]


@dataclass(frozen=True)
class Part:
    x: int
    m: int
    a: int
    s: int

    def get_cat(self, category: Category) -> int:
        assert category in "xmas"
        return self.__getattribute__(category)

    def rating(self):
        return self.x + self.m + self.a + self.s


def lt(a: int, b: int) -> bool:
    return a < b


def gt(a: int, b: int) -> bool:
    return a > b


@dataclass
class Rule:
    category: Category
    cmp_op: Literal["<", ">"]
    cmp_value: int
    result: Result

    def process(self, part: Part) -> Optional[Result]:
        val = part.get_cat(self.category)
        cmp_fn = lt if self.cmp_op == "<" else gt
        return self.result if cmp_fn(val, self.cmp_value) else None

    def __repr__(self):
        return f"{self.category}{self.cmp_op}{self.cmp_value}:{self.result}"


@dataclass
class Workflow:
    name: str
    rules: list[Rule]
    default: WorkflowName

    def process(self, part: Part) -> Result:
        for rule in self.rules:
            result = rule.process(part)
            if result is not None:
                return result
        return self.default

    def __repr__(self):
        return f"{self.name}{{{','.join(str(r) for r in self.rules)},{self.default}}}"


Workflows = dict[str, Workflow]


def parse_rule(s: str) -> Rule:
    # a<2006:qkq
    cat, s_op, s_val, result = re.match(r"([xmas])([<>])(\d+):(\w+)", s).groups()
    return Rule(cat, s_op, int(s_val), result)


def parse_workflow(s: str) -> Workflow:
    # px{a<2006:qkq,m>2090:A,rfg}
    name, s_rules, default = re.match(r"(\w+)\{(.+),(\w+)}", s).groups()
    rules = [parse_rule(r) for r in s_rules.split(",")]
    return Workflow(
        name,
        rules,
        default,
    )


def parse_part(s: str) -> Part:
    # {x=787,m=2655,a=1222,s=2876}
    x, m, a, s = re.match(r"^{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}$", s).groups()
    return Part(int(x), int(m), int(a), int(s))


def parse_input(input: TextIO) -> tuple[Workflows, list[Part]]:
    s_wf, s_parts = input.read().strip().split("\n\n")
    workflow_list = [parse_workflow(wf) for wf in s_wf.splitlines()]
    parts = [parse_part(p) for p in s_parts.splitlines()]
    return {wf.name: wf for wf in workflow_list}, parts


def process(part: Part, wfs: Workflows) -> Outcome:
    result = "in"
    while result not in ("A", "R"):
        result = wfs[result].process(part)

    return result


Unknowns = dict[Category, Interval]


def apply_rule_to_unknowns(
    rule: Rule, unknowns: Unknowns
) -> tuple[Optional[Unknowns], Optional[Unknowns]]:
    # Return value is pass, no_pass
    interval = unknowns[rule.category]
    passed = dict(unknowns)
    failed = dict(unknowns)

    # s<537:gd
    start, end = interval
    if rule.cmp_op == "<":
        # Passed
        new_end = min(end, rule.cmp_value - 1)
        if new_end < start:
            passed = None
        else:
            passed[rule.category] = (start, new_end)

        # Failed
        new_start = max(rule.cmp_value, start)
        if new_start > end:
            failed = None
        else:
            failed[rule.category] = (new_start, end)
    else:
        # Passed
        new_start = max(start, rule.cmp_value + 1)
        if new_start > end:
            passed = None
        else:
            passed[rule.category] = (new_start, end)

        # Failed
        new_end = min(end, rule.cmp_value)
        if new_end < start:
            failed = None
        else:
            failed[rule.category] = (start, new_end)

    return passed, failed


def total(unknowns: Unknowns):
    return prod(end - start + 1 for start, end in unknowns.values())


def comb_accepted_by_wf(
    wf_name: str, wfs: Workflows, unknowns: Optional[Unknowns] = None, stack: int = 0
) -> int:
    # This is the product of number of accepted values for x,m,a,s for this workflow (=> result in "A")
    if not unknowns:
        unknowns = {
            "x": (1, 4000),
            "m": (1, 4000),
            "a": (1, 4000),
            "s": (1, 4000),
        }

    print(
        stack * "\t"
        + f"{wf_name} x={unknowns['x']},m={unknowns['m']},a={unknowns['a']},s={unknowns['s']}  total={total(unknowns)}"
    )

    wf = wfs[wf_name]
    accepted = 0

    # While there are unknowns, keep following
    # print()
    # print(f"wf={str(wf)} unknowns={unknowns}")
    for r in wf.rules:
        passed, failed = apply_rule_to_unknowns(r, unknowns)
        # print(f"{wf} {r} passed={passed} failed={failed}")
        if passed:
            if r.result == "A":
                # print(f"{wf} {r} A:{passed}")
                print(
                    (stack + 1) * "\t"
                    + f"{wf_name} {r} x={passed['x']},m={passed['m']},a={passed['a']},s={passed['s']}"
                )
                accepted += total(passed)
            elif r.result == "R":
                # We're not counting rejections
                pass
            else:
                # Follow with the other workflows
                accepted += comb_accepted_by_wf(r.result, wfs, passed, stack + 1)

        # Account for not passed
        unknowns = failed

    # Rest of the unknowns go to the workflow default
    if unknowns:
        # print(f"{wf} default {wf.default}={unknowns}")
        if wf.default == "A":
            # print(f"{wf} default A:{unknowns}")
            print(
                (stack + 1) * "\t"
                + f"{wf_name} def A x={unknowns['x']},m={unknowns['m']},a={unknowns['a']},s={unknowns['s']}"
            )
            accepted += total(unknowns)
        elif wf.default == "R":
            # We're not counting rejections
            pass
        else:
            # Follow with the other workflows
            accepted += comb_accepted_by_wf(wf.default, wfs, unknowns, stack + 1)

    print(stack * "\t" + f"{wf.name} -> {accepted}")
    return accepted


def first(input: TextIO) -> int:
    wfs, parts = parse_input(input)
    return sum(p.rating() for p in parts if process(p, wfs) == "A")


def second(input: TextIO) -> int:
    wfs, _ = parse_input(input)
    return comb_accepted_by_wf("in", wfs)
