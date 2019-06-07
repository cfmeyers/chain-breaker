# -*- coding: utf-8 -*-
from datetime import date, timedelta
import csv
from prompt_toolkit import prompt, HTML
from prompt_toolkit import print_formatted_text as print
from prompt_toolkit.shortcuts import clear

import dateparser

"""Main module."""


def read_chain_links(path_to_chain):
    links = set()
    with open(path_to_chain) as f:
        for line in f:
            link_date = dateparser.parse(line).date()
            links.add(link_date)
    return sorted(links, reverse=True)


def links_to_today(links):
    today = date.today()
    yesterday = today - timedelta(days=1)
    if links == []:
        return []
    first_link = links[0]
    chain = []
    if first_link not in (today, yesterday):
        return []
    elif first_link == today:
        chain.append(today)
        cur_link = today
    else:
        chain.append(yesterday)
        cur_link = yesterday

    for link in links[1:]:
        if link != cur_link - timedelta(days=1):
            return chain
        else:
            chain.append(link)
            cur_link = link
    return chain


def render_chain(path_to_chain, title):
    clear()
    links = read_chain_links(path_to_chain)
    links_to_today(links)
    print(HTML(f'<bold><purple>{title.upper()}</purple></bold>'))

    output = make_blocks(reversed(links))
    print(HTML(f'<red>{output}</red>'))


def make_block(d):
    letter = d.strftime('%A')[0].lower()
    decorated = f"<bold><white bg='grey'>{letter}</white></bold>"
    return f"""\
▆▆▆
▆{decorated}▆
▆▆▆"""


def make_blocks(links):
    blocks = [make_block(link) for link in links]
    top = ''
    middle = ''
    bottom = ''
    for block in blocks:
        t, m, b = block.split('\n')
        top += f'{t} '
        middle += f'{m}>'
        bottom += f'{b} '
    return f"""\
{top}
{middle}
{bottom}"""
