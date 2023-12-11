"""
Command line interface for advent of code 2021.
"""

import importlib
import time

import click

from .utils import get_input_filename_for_day

from .new_day import new_day as new_day_fn


@click.command()
@click.argument("day_num", type=click.IntRange(min=1, max=25))
def day(day_num: int) -> None:
    """Run the first() and second() methods for a given day."""

    click.echo(f"🎄 Running Advent of Code for day {day_num} 🎄\n")

    day_module = importlib.import_module(f"advent.days.day{day_num:02}")

    input_filename = get_input_filename_for_day(day_num)

    start_t = time.perf_counter()
    with open(input_filename) as reader:
        first_result = day_module.first(reader)
    first_t = time.perf_counter()
    click.echo(f"First: {first_result} ({first_t - start_t:.2f}s)")

    with open(input_filename) as reader:
        second_result = day_module.second(reader)
    second_t = time.perf_counter()
    click.echo(f"Second: {second_result} ({second_t - first_t:.2f}s)")

    click.echo(f"\n✨ Done ({second_t - start_t:.2f}s) ✨")


@click.command()
@click.argument("day_num", type=click.IntRange(min=1, max=25))
def new_day(day_num: int) -> None:
    """Create a new day's files."""

    click.echo(f"🎄 Creating new files for day {day_num} 🎄\n")
    new_day_fn(day_num)

    click.echo(f"\n✨ Done ✨")
