from collections.abc import Iterator
import csv
import datetime
from flask import render_template
from itertools import count

def even_or_odd(x: int) -> str:
    return "odd" if x % 2 else "even"

def tail(it: Iterator) -> Iterator:
    next(it)
    return it

def current_week() -> int:
    return datetime.datetime.now().isocalendar().week

def read_and_sort_csv() -> list[tuple[int, list[str]]]:
    with open('static/students.csv') as file:
        csv_reader = csv.DictReader(file, delimiter=",") # done so the list is not consumed
        rows = list(csv_reader)
        groups = []

        for week in count(start=current_week()):
            if str(week) not in csv_reader.fieldnames: # pyright: ignore
                break

            students = list(map(
                lambda student: student["name"],
                filter(
                    lambda student: student[str(week)] == 'x',
                    rows
                )
            ))

            if not students: # filter out breaks and such
                continue

            groups.append((week, students))

        return groups

def students():
    return render_template("students.jinja")


if __name__ == "__main__":
    read_and_sort_csv()
