# SPDX-License-Identifier: BSD-3-Clause
"""
Appointment check tests.
"""

import pandas as pd
from poli_sci_kit.appointment.checks import consistency_condition, quota_condition


def test_quota_condition_pass():
    shares = [
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

    seats = [
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
    assert quota_condition(shares=shares, seats=seats) == True


def test_quota_condition_fail():
    shares = [
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

    seats = [
        29,  # too low
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
        4,  # too high
    ]
    assert quota_condition(shares=shares, seats=seats) != True


def test_consistency_condition_seat_pass():
    df_shares = pd.DataFrame(data=[[100] * 3, [75] * 3, [50] * 3])

    df_seats = pd.DataFrame(data=[[1, 2, 2], [1, 1, 2], [1, 1, 1]])

    assert (
        consistency_condition(
            df_shares=df_shares, df_seats=df_seats, check_type="seat_monotony"
        )
        == True
    )


def test_consistency_condition_seat_fail():
    df_shares = pd.DataFrame(data=[[100] * 3, [75] * 3, [50] * 3])

    df_seats = pd.DataFrame(
        data=[[1, 2, 1], [1, 1, 1], [1, 1, 3]]
    )  # first group loses a seat in the third iteration

    assert (
        consistency_condition(
            df_shares=df_shares, df_seats=df_seats, check_type="seat_monotony"
        )
        is not True
    )


def test_consistency_condition_share_pass():
    df_shares = pd.DataFrame(data=[[100, 110, 120], [75, 65, 65], [50, 50, 40]])

    df_seats = pd.DataFrame(data=[[3, 3, 3], [2, 2, 2], [1, 1, 1]])
    assert (
        consistency_condition(
            df_shares=df_shares, df_seats=df_seats, check_type="share_monotony"
        )
        == True
    )


def test_consistency_condition_share_fail():
    df_shares = pd.DataFrame(data=[[100, 110, 120], [75, 65, 65], [50, 50, 40]])

    df_seats = pd.DataFrame(
        data=[[3, 3, 2], [2, 2, 3], [1, 1, 1]]
    )  # increase in third leads to decrease
    assert (
        consistency_condition(
            df_shares=df_shares, df_seats=df_seats, check_type="share_monotony"
        )
        is not True
    )
