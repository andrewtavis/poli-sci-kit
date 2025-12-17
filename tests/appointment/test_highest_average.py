# SPDX-License-Identifier: BSD-3-Clause
"""
Highest Averages method tests.
"""

from poli_sci_kit.appointment.methods import highest_averages


def test_ha_sum(highest_averages_styles, votes, seats):
    assert (
        sum(
            highest_averages(
                averaging_style=highest_averages_styles,
                shares=votes,
                total_alloc=seats,
            )
        )
        == seats
    )


def test_ha_min_alloc(highest_averages_styles, votes, seats):
    assert all(
        alloc >= 3
        for alloc in highest_averages(
            averaging_style=highest_averages_styles,
            shares=votes,
            total_alloc=seats,
            min_alloc=3,
        )
    )


def test_ha_greater_than_zero(highest_averages_styles, votes, seats):
    assert all(
        alloc >= 0
        for alloc in highest_averages(
            averaging_style=highest_averages_styles, shares=votes, total_alloc=seats,
        )
    )


def test_ha_jefferson(long_votes_list, seats_large):
    results = [
        33,
        23,
        18,
        16,
        11,
        11,
        11,
        10,
        8,
        7,
        7,
        7,
        6,
        5,
        5,
        4,
        4,
        4,
        3,
        2,
        2,
        1,
        1,
        1,
    ]

    assert (
        highest_averages(
            averaging_style="Jefferson",
            shares=long_votes_list,
            total_alloc=seats_large,
        )
        == results
    )


def test_ha_webster(long_votes_list, seats_large):
    results = [
        32,
        23,
        17,
        16,
        11,
        10,
        10,
        10,
        8,
        7,
        7,
        7,
        6,
        5,
        5,
        5,
        4,
        4,
        3,
        3,
        2,
        2,
        2,
        1,
    ]

    assert (
        highest_averages(
            averaging_style="Webster", shares=long_votes_list, total_alloc=seats_large,
        )
        == results
    )


def test_ha_huntington_hill(long_votes_list, seats_large):
    results = [
        32,
        22,
        17,
        16,
        11,
        10,
        10,
        10,
        8,
        7,
        7,
        7,
        6,
        5,
        5,
        5,
        5,
        4,
        3,
        3,
        2,
        2,
        2,
        1,
    ]

    assert (
        highest_averages(
            averaging_style="Huntington-Hill",
            shares=long_votes_list,
            total_alloc=seats_large,
        )
        == results
    )


def test_ha_threshold(short_votes_list):
    seats = 200
    results = [118, 82, 0, 0, 0]

    assert (
        highest_averages(
            averaging_style="Jefferson",
            shares=short_votes_list,
            total_alloc=seats,
            alloc_threshold=0.2,
            min_alloc=None,
            tie_break="majority",
            majority_bonus=False,
            modifier=None,
        )
        == results
    )


def test_ha_modifier(short_votes_list):
    seats = 5
    results = [2, 2, 1, 0, 0]

    assert (
        highest_averages(
            averaging_style="Jefferson",
            shares=short_votes_list,
            total_alloc=seats,
            alloc_threshold=None,
            min_alloc=None,
            tie_break="majority",
            majority_bonus=False,
            modifier=0.5,
        )
        == results
    )


def test_ha_tie_break(tie_votes_list):
    seats = 8
    results_1 = [3, 2, 1, 1, 1]
    results_2 = [3, 1, 2, 1, 1]

    assert highest_averages(
        averaging_style="Jefferson",
        shares=tie_votes_list,
        total_alloc=seats,
        alloc_threshold=None,
        min_alloc=None,
        tie_break="random",
        majority_bonus=False,
        modifier=None,
    ) in [results_1, results_2]


def test_ha_majority(tie_votes_list):
    seats = 8
    results = [4, 1, 1, 1, 1]

    assert (
        highest_averages(
            averaging_style="Jefferson",
            shares=tie_votes_list,
            total_alloc=seats,
            alloc_threshold=None,
            min_alloc=None,
            tie_break="majority",
            majority_bonus=True,
            modifier=None,
        )
        == results
    )
