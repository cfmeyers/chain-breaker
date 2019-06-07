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

    @freeze_time("2019-04-29")
    def test_it_returns_yesterday_if_yesterday_is_only_link_in_chain(self):
        links = [date(2019, 4, 28)]
        assert [date(2019, 4, 28)] == links_to_today(links)

    @freeze_time("2019-04-29")
    def test_it_returns_both_today_and_yesterday_if_they_are_only_links_in_chain(self):
        links = [date(2019, 4, 29), date(2019, 4, 28)]
        assert [date(2019, 4, 29), date(2019, 4, 28)] == links_to_today(links)

    @freeze_time("2019-04-29")
    def test_it_returns_both_yesterday_and_day_prior(self):
        links = [date(2019, 4, 28), date(2019, 4, 27)]
        assert [date(2019, 4, 28), date(2019, 4, 27)] == links_to_today(links)

    @freeze_time("2019-04-29")
    def test_it_empty_list_for_no_dates(self):
        links = []
        assert [] == links_to_today(links)

    @freeze_time("2019-04-29")
    def test_it_does_not_return_any_days_if_there_is_a_gap(self):
        links = [date(2019, 4, 27)]
        assert [] == links_to_today(links)

    @freeze_time("2019-04-29")
    def test_it_returns_both_yesterday_but_no_gaps(self):
        links = [date(2019, 4, 28), date(2019, 4, 26), date(2019, 4, 25)]
        assert [date(2019, 4, 28)] == links_to_today(links)
