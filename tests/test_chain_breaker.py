#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `chain_breaker` package."""

import pytest
from datetime import date
from freezegun import freeze_time

from chain_breaker.chain_breaker import links_to_today


class TestLinksToToday:
    @freeze_time("2019-04-29")
    def test_it_returns_today_if_today_is_only_link_in_chain(self):
        links = [date(2019, 4, 29)]
        assert [date(2019, 4, 29)] == links_to_today(links)
