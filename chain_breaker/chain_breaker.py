# -*- coding: utf-8 -*-
from datetime import date, timedelta
import csv

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


def render_chain(path_to_chain):
    links = read_chain_links(path_to_chain)
    links_to_today(links)
