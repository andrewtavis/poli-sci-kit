# SPDX-License-Identifier: BSD-3-Clause
"""
Largest Remainder method tests.
"""

from poli_sci_kit.appointment.methods import largest_remainder


def test_lr_sum(largest_remainder_styles, votes, seats):
    assert (
        sum(
            largest_remainder(
                quota_style=largest_remainder_styles, shares=votes, total_alloc=seats
            )
        )
        == seats
    )


def test_lr_min_alloc(largest_remainder_styles, votes, seats):
    assert all(
        alloc >= 3
        for alloc in largest_remainder(
            quota_style=largest_remainder_styles,
            shares=votes,
            total_alloc=seats,
            min_alloc=3,
        )
    )


def test_lr_greater_than_zero(largest_remainder_styles, votes, seats):
    assert all(
        alloc >= 0
        for alloc in largest_remainder(
            quota_style=largest_remainder_styles, shares=votes, total_alloc=seats,
        )
    )


def test_lr_hare(long_votes_list, seats_large):
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
        largest_remainder(
            quota_style="Hare", shares=long_votes_list, total_alloc=seats_large,
        )
        == results
    )


def test_lr_droop(long_votes_list, seats_large):
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
        largest_remainder(
            quota_style="Droop", shares=long_votes_list, total_alloc=seats_large,
        )
        == results
    )


def test_lr_hb(long_votes_list, seats_large):
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
        largest_remainder(
            quota_style="Hagenbach–Bischoff",
            shares=long_votes_list,
            total_alloc=seats_large,
        )
        == results
    )


def test_lr_threshold(short_votes_list, seats_large):
    results = [117, 83, 0, 0, 0]

    assert (
        largest_remainder(
            quota_style="Hare",
            shares=short_votes_list,
            total_alloc=seats_large,
            alloc_threshold=0.2,
            min_alloc=None,
            tie_break="majority",
            majority_bonus=False,
        )
        == results
    )


def test_lr_modifier(short_votes_list):
    seats = 5
    results = [3, 1, 1, 0, 0]

    assert (
        largest_remainder(
            quota_style="Hare",
            shares=short_votes_list,
            total_alloc=seats,
            alloc_threshold=None,
            min_alloc=None,
            tie_break="majority",
            majority_bonus=0.5,
        )
        == results
    )


def test_lr_tie_break(tie_votes_list):
    seats = 8
    results_1 = [3, 2, 1, 1, 1]
    results_2 = [3, 1, 2, 1, 1]

    assert largest_remainder(
        quota_style="Hare",
        shares=tie_votes_list,
        total_alloc=seats,
        alloc_threshold=None,
        min_alloc=None,
        tie_break="majority",
        majority_bonus=False,
    ) in [results_1, results_2]


def test_lr_majority(tie_votes_list):
    seats = 8
    results = [4, 1, 1, 1, 1]

    assert (
        largest_remainder(
            quota_style="Hare",
            shares=tie_votes_list,
            total_alloc=seats,
            alloc_threshold=None,
            min_alloc=None,
            tie_break="majority",
            majority_bonus=True,
        )
        == results
    )
