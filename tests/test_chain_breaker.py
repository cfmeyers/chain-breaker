#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `chain_breaker` package."""

import pytest
from datetime import date, datetime, timedelta
from freezegun import freeze_time

from chain_breaker.chain_breaker import (
    links_to_today,
    make_dates_with_colors,
    DateWithColor,
    get_this_week,
)


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
        assert [date(2019, 4, 28), date(2019, 4, 29)] == links_to_today(links)

    @freeze_time("2019-04-29")
    def test_it_returns_both_yesterday_and_day_prior(self):
        links = [date(2019, 4, 28), date(2019, 4, 27)]
        assert [date(2019, 4, 27), date(2019, 4, 28)] == links_to_today(links)

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


class TestGetThisWeek:
    # TODO refactor as absolute dates, not relative with timedelta
    @freeze_time("2019-04-29")  # Monday
    def test_it_returns_this_week_when_today_is_monday(self):
        monday = datetime.today().date()
        tuesday = monday + timedelta(days=1)
        wednesday = monday + timedelta(days=2)
        thursday = monday + timedelta(days=3)
        friday = monday + timedelta(days=4)
        saturday = monday + timedelta(days=5)
        sunday = monday + timedelta(days=6)
        # assert monday == get_this_week()[0]
        assert [
            monday,
            tuesday,
            wednesday,
            thursday,
            friday,
            saturday,
            sunday,
        ] == get_this_week()

    @freeze_time("2019-05-05")  # sunday
    def test_it_returns_this_week_when_today_is_sunday(self):
        monday = datetime.today().date() - timedelta(days=6)
        tuesday = monday + timedelta(days=1)
        wednesday = monday + timedelta(days=2)
        thursday = monday + timedelta(days=3)
        friday = monday + timedelta(days=4)
        saturday = monday + timedelta(days=5)
        sunday = datetime.today().date()

        assert [
            monday,
            tuesday,
            wednesday,
            thursday,
            friday,
            saturday,
            sunday,
        ] == get_this_week()


class TestMakeDatesWithColors:
    @freeze_time("2019-04-29")
    def test_it_returns_a_week_of_all_grey_dates_with_no_unbroken_links(self):
        monday = datetime.today().date()
        tuesday = monday + timedelta(days=1)
        wednesday = monday + timedelta(days=2)
        thursday = monday + timedelta(days=3)
        friday = monday + timedelta(days=4)
        saturday = monday + timedelta(days=5)
        sunday = monday + timedelta(days=6)
        assert monday.strftime('%A') == 'Monday'
        assert sunday.strftime('%A') == 'Sunday'

        expected = [
            DateWithColor(date=monday, color='grey'),
            DateWithColor(date=tuesday, color='grey'),
            DateWithColor(date=wednesday, color='grey'),
            DateWithColor(date=thursday, color='grey'),
            DateWithColor(date=friday, color='grey'),
            DateWithColor(date=saturday, color='grey'),
            DateWithColor(date=sunday, color='grey'),
        ]

        assert expected == make_dates_with_colors([])
