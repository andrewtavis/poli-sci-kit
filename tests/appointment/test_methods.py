"""
Appointment Method Tests
------------------------
"""

from poli_sci_kit.appointment.methods import largest_remainder, highest_average


def test_lr_sum(largest_remainder_styles, votes, seats):
    assert (
        sum(
            largest_remainder(
                quota_style=largest_remainder_styles, shares=votes, total_alloc=seats
            )
        )
        == seats
    )


def test_ha_sum(highest_average_styles, votes, seats):
    assert (
        sum(
            highest_average(
                averaging_style=highest_average_styles, shares=votes, total_alloc=seats,
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


def test_ha_min_alloc(highest_average_styles, votes, seats):
    assert all(
        alloc >= 3
        for alloc in highest_average(
            averaging_style=highest_average_styles,
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


def test_ha_greater_than_zero(highest_average_styles, votes, seats):
    assert all(
        alloc >= 0
        for alloc in highest_average(
            averaging_style=highest_average_styles, shares=votes, total_alloc=seats,
        )
    )


def test_lr_hare():
    votes = [
        1918578,
        1348072,
        1023503,
        937901,
        639747,
        625263,
        621832,
        610408,
        455025,
        429811,
        405843,
        399454,
        343031,
        319922,
        297665,
        280657,
        269326,
        262508,
        171904,
        157147,
        130419,
        110358,
        97194,
        75432,
    ]

    seats = 200

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
        largest_remainder(quota_style="Hare", shares=votes, total_alloc=seats,)
        == results
    )


def test_ha_jefferson():
    votes = [
        1918578,
        1348072,
        1023503,
        937901,
        639747,
        625263,
        621832,
        610408,
        455025,
        429811,
        405843,
        399454,
        343031,
        319922,
        297665,
        280657,
        269326,
        262508,
        171904,
        157147,
        130419,
        110358,
        97194,
        75432,
    ]

    seats = 200

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
        highest_average(averaging_style="Jefferson", shares=votes, total_alloc=seats,)
        == results
    )
