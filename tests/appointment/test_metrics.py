# SPDX-License-Identifier: BSD-3-Clause
"""
Appointment metric tests.
"""

from poli_sci_kit.appointment.metrics import (
    alloc_to_share_ratio,
    dispr_index,
    div_index,
    effective_number_of_groups,
    ideal_share,
    rep_weight,
    sqr_alloc_to_share_error,
    sqr_rep_weight_error,
    total_alloc_to_share_error,
    total_rep_weight_error,
)


def test_ideal_share(share, total_shares, seats):
    assert (
        round(
            ideal_share(share=share, total_shares=total_shares, total_alloc=seats),
            4,
        )
        == 6.9222
    )


def test_alloc_to_share_ratio(share, total_shares, allocation, seats):
    assert (
        round(
            alloc_to_share_ratio(
                share=share,
                total_shares=total_shares,
                allocation=allocation,
                total_alloc=seats,
            ),
            4,
        )
        == 1.0112
    )


def test_square_alloc_to_share_ratio(share, total_shares, allocation, seats):
    assert (
        round(
            sqr_alloc_to_share_error(
                share=share,
                total_shares=total_shares,
                allocation=allocation,
                total_alloc=seats,
            ),
            6,
        )
        == 0.000126
    )


def test_total_alloc_to_share_error(tie_votes_list, allocations):
    assert (
        round(
            total_alloc_to_share_error(
                shares=tie_votes_list, allocations=allocations, proportional=True
            ),
            6,
        )
        == 0.006835
    )


def test_rep_weight(share, allocation):
    assert round(rep_weight(share=share, allocation=allocation), 4) == 274082.5714


def test_sqr_rep_weight_error(share, total_shares, allocation, seats):
    assert (
        round(
            sqr_rep_weight_error(
                share=share,
                total_shares=total_shares,
                allocation=allocation,
                total_alloc=seats,
            ),
            4,
        )
        == 9480416.9437
    )


def test_total_rep_weight_error(tie_votes_list, allocations):
    assert (
        round(
            total_rep_weight_error(
                shares=tie_votes_list, allocations=allocations, proportional=True
            ),
            4,
        )
        == 594037282.4765
    )


def test_div_not_0(short_votes_list, q, div_index_metrics):
    assert div_index(shares=short_votes_list, q=q, metric_type=div_index_metrics) != 0


def test_dispr_not_0(short_votes_list, allocations, dispr_index_metrics):
    assert (
        dispr_index(
            shares=short_votes_list,
            allocations=allocations,
            metric_type=dispr_index_metrics,
        )
        != 0
    )


def test_effective_number_of_groups_not_0(short_votes_list, effective_group_metrics):
    assert (
        effective_number_of_groups(
            shares=short_votes_list, metric_type=effective_group_metrics
        )
        != 0
    )
