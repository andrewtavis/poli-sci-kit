# SPDX-License-Identifier: BSD-3-Clause
"""
Appointment metric tests.
"""

from poli_sci_kit.appointment.metrics import (
    alloc_to_share_ratio,
    disproportionality_index,
    diversity_index,
    effective_number_of_groups,
    ideal_share,
    representative_weight,
    sqr_alloc_to_share_error,
    sqr_representative_weight_error,
    total_allocation_to_share_error,
    total_representative_weight_error,
)


def test_ideal_share(share, total_shares, seats):
    assert (
        round(
            ideal_share(share=share, total_shares=total_shares, total_allocation=seats),
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
                total_allocation=seats,
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
                total_allocation=seats,
            ),
            6,
        )
        == 0.000126
    )


def test_total_allocation_to_share_error(tie_votes_list, allocations):
    assert (
        round(
            total_allocation_to_share_error(
                shares=tie_votes_list, allocations=allocations, proportional=True
            ),
            6,
        )
        == 0.006835
    )


def test_representative_weight(share, allocation):
    assert (
        round(representative_weight(share=share, allocation=allocation), 4)
        == 274082.5714
    )


def test_sqr_representative_weight_error(share, total_shares, allocation, seats):
    assert (
        round(
            sqr_representative_weight_error(
                share=share,
                total_shares=total_shares,
                allocation=allocation,
                total_allocation=seats,
            ),
            4,
        )
        == 9480416.9437
    )


def test_total_representative_weight_error(tie_votes_list, allocations):
    assert (
        round(
            total_representative_weight_error(
                shares=tie_votes_list, allocations=allocations, proportional=True
            ),
            4,
        )
        == 594037282.4765
    )


def test_div_not_0(short_votes_list, q, diversity_index_metrics):
    assert (
        diversity_index(
            shares=short_votes_list, q=q, metric_type=diversity_index_metrics
        )
        != 0
    )


def test_dispr_not_0(short_votes_list, allocations, disproportionality_index_metrics):
    assert (
        disproportionality_index(
            shares=short_votes_list,
            allocations=allocations,
            metric_type=disproportionality_index_metrics,
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
