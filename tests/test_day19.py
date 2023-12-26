import io

from advent.days.day19 import (
    Rule,
    apply_rule_to_unknowns,
    first,
    parse_rule,
    second,
    total,
)

data = """px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}"""


def test_first():
    assert first(io.StringIO(data)) == 19114


def test_second_custom():
    d1 = """px{a<2006:qkq,m>2090:A,rfg}
in{s<1351:R,A}

{x=787,m=2655,a=1222,s=2876}
"""
    assert second(io.StringIO(d1)) == total(
        dict(x=(0, 4000), m=(0, 4000), a=(0, 4000), s=(1351, 4000))
    )

    d1 = """px{a<2006:qkq,m>2090:A,rfg}
in{s>1351:R,A}

{x=787,m=2655,a=1222,s=2876}
"""
    assert second(io.StringIO(d1)) == total(
        dict(x=(0, 4000), m=(0, 4000), a=(0, 4000), s=(0, 1351))
    )


def test_apply_rule_to_unknowns():
    fuk = parse_rule("a<2000:A,A}")
    assert apply_rule_to_unknowns(
        fuk, dict(x=(0, 4000), m=(0, 2090), a=(2006, 4000), s=(0, 1350))
    ) == (None, {"x": (0, 4000), "m": (0, 2090), "a": (2006, 4000), "s": (0, 1350)})

    fuk = parse_rule("a>2000:A,A}")
    assert apply_rule_to_unknowns(
        fuk, dict(x=(0, 4000), m=(0, 2090), a=(2006, 4000), s=(0, 1350))
    ) == ({"a": (2006, 4000), "m": (0, 2090), "s": (0, 1350), "x": (0, 4000)}, None)


def test_second_rec():
    d1 = """px{a<2006:A,m>2090:boo,fuk}
in{s<1351:px,A}
boo{m<3000:A,a>2000:A,R}
fuk{a>2000:A,A}

{x=787,m=2655,a=1222,s=2876}
"""
    """
    in r1 > px r1: x=(0,4000),m=(0,4000),a=(0,2005),s=(0,1350)    ### {'x': (0, 4000), 'm': (0, 4000), 'a': (0, 2005), 's': (0, 1350)} ### 43383379558106
    in r1 > px r2 > boo r1: x=(0,4000),m=(2091,2999),a=(2006,4000),s=(0,1350)  ### {'x': (0, 4000), 'm': (2091, 2999), 'a': (2006, 4000), 's': (0, 1350)} ### 97053077205
    in r1 > px r2 > boo r2: x=(0,4000),m=(3000,4000),a=(2006, 4000),s=(0,1350) ### {'x': (0, 4000), 'm': (3000, 4000), 'a': (2006, 4000), 's': (0, 1350)} ### 10794458920245
    in r1 > px df: x=(0,4000),m=(0,2090),a=(2006,4000),s=(0,1350) ### {'x': (0, 4000), 'm': (0, 2090), 'a': (2006, 4000), 's': (0, 1350)} ### 22548664937295
    in df: x=(0,4000),m=(0,4000),a=(0,4000),s=(1351,4000) ###  {'x': (0, 4000), 'm': (0, 4000), 'a': (0, 4000), 's': (1351, 4000)} ### 169727231802650
    
    
    boo: 97053077205 + 10794458920245 = 10891511997450
    px: r2(boo):10891511997450 + r1:43383379558106 + df:22548664937295 = 76823556492851
    in: r1(px):76823556492851 + 169727231802650 = 246550788295501
    """

    # boo rule 1 total(dict(x=(0, 4000), m=(2091, 2099), a=(2006, 4000), s=(0, 1350)))
    # boo rule 2 total(dict(x=(0, 4000), m=(3000, 4000), a=(2006, 4000), s=(0, 1350)))
    # boo default -> should be None
    # px rule 1 total(dict(x=(0, 4000), m=(0, 4000), a=(0, 2005), s=(0, 1350)))
    # px rule 2 see boo
    # px default total(dict(x=(0, 4000), m=(0, 2090), a=(2006, 4000), s=(0, 1350)))
    # in rule1 see px
    # in default total(dict(x=(0, 4000), m=(0, 4000), a=(0, 4000), s=(1351, 4000)))
    tootoo = (
        total(dict(x=(0, 4000), m=(0, 4000), a=(0, 2005), s=(0, 1350)))
        + total(dict(x=(0, 4000), m=(2091, 2999), a=(2006, 4000), s=(0, 1350)))
        + total(dict(x=(0, 4000), m=(3000, 4000), a=(2006, 4000), s=(0, 1350)))
        + total(dict(x=(0, 4000), m=(0, 2090), a=(2006, 4000), s=(0, 1350)))
        + total(dict(x=(0, 4000), m=(0, 4000), a=(0, 4000), s=(1351, 4000)))
    )
    print()
    assert second(io.StringIO(d1)) == tootoo


# TODO not tested default is another workflow


def test_second():
    print()
    print(data.split("\n\n")[0])
    print()
    assert second(io.StringIO(data)) == 167409079868000
