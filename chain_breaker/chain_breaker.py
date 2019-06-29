# -*- coding: utf-8 -*-
from datetime import date, timedelta
from collections import namedtuple
import csv

from prompt_toolkit import prompt, HTML
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import clear

import dateparser

"""Main module."""

DateWithColor = namedtuple('DateWithColor', 'date color')


style = Style.from_dict({'title': 'bg:grey fg:purple'})


def read_in_all_links(path_to_chain):
    links = set()
    with open(path_to_chain) as f:
        for line in f:
            link_date = dateparser.parse(line).date()
            links.add(link_date)
    return sorted(links, reverse=True)


def links_to_today(links):
    today = date.today()
    yesterday = today - timedelta(days=1)
    if links == [] or links[0] not in (today, yesterday):
        return []
    chain = [links[0]]  # either today or yesterday

    for link in links[1:]:
        if link != chain[-1] - timedelta(days=1):
            break
        else:
            chain.append(link)
    return list(reversed(chain))


# TODO so ugly
def get_this_week():
    today = date.today()
    day_index = today.weekday()
    days_before_today = list(
        reversed([today + timedelta(days=-(n + 1)) for n in range(day_index)])
    )
    days_after_today = [today + timedelta(days=n + 1) for n in range(6 - day_index)]
    return days_before_today + [today] + days_after_today


def make_dates_with_colors(unbroken_links):
    this_week = get_this_week()
    if unbroken_links == []:
        return [DateWithColor(date=l, color='grey') for l in this_week]
    remaining_days = []
    for day in this_week:
        if day > unbroken_links[-1]:
            remaining_days.append(day)

    return [DateWithColor(date=l, color='red') for l in unbroken_links] + [
        DateWithColor(date=l, color='grey') for l in remaining_days
    ]


def render_chain(path_to_chain, title):
    clear()
    all_links = read_in_all_links(path_to_chain)
    unbroken_links = links_to_today(all_links)
    dates_with_colors = make_dates_with_colors(unbroken_links)
    output = make_blocks(dates_with_colors)
    streak_count = len([d for d in dates_with_colors if d.color == 'red'])
    print(
        HTML(
            f'<bold><title> ▶ {title.upper()} ◀ </title><title>({streak_count})</title></bold>'
        ),
        style=style,
    )
    print(HTML(output))


def make_block(d: DateWithColor):
    if d.date.strftime('%A') == 'Thursday':
        letter = 'Þ'
    else:
        letter = d.date.strftime('%A')[0].lower()
    decorated = f"<bold><white>{letter}</white></bold>"
    return f"""\
<{d.color}>▆▆▆</{d.color}>
<{d.color}>▆{decorated}▆</{d.color}>
<{d.color}>▆▆▆</{d.color}>\
"""


def make_blocks(links):
    blocks = [make_block(link) for link in links]
    top = ''
    middle = ''
    bottom = ''
    for block in blocks:
        t, m, b = block.split('\n')
        top += f'{t} '
        middle += f'{m} '
        bottom += f'{b} '
    return f"""\
{top}
{middle}
{bottom}"""
