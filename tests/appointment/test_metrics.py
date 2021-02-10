"""Appointment metric tests"""

from poli_sci_kit.appointment import metrics


def test_ideal_share(share, total_shares, seats):
    assert (
        round(
            metrics.ideal_share(
                share=share, total_shares=total_shares, total_alloc=seats
            ),
            4,
        )
        == 6.9222
    )


def test_alloc_to_share_ratio(share, total_shares, allocation, seats):
    assert (
        round(
            metrics.alloc_to_share_ratio(
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
            metrics.sqr_alloc_to_share_error(
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
            metrics.total_alloc_to_share_error(
                shares=tie_votes_list, allocations=allocations, proportional=True
            ),
            6,
        )
        == 0.006835
    )


def test_rep_weight(share, allocation):
    assert (
        round(metrics.rep_weight(share=share, allocation=allocation), 4) == 274082.5714
    )


def test_sqr_rep_weight_error(share, total_shares, allocation, seats):
    assert (
        round(
            metrics.sqr_rep_weight_error(
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
            metrics.total_rep_weight_error(
                shares=tie_votes_list, allocations=allocations, proportional=True
            ),
            4,
        )
        == 594037282.4765
    )


def test_div_not_0(short_votes_list, q, div_index_metrics):
    assert (
        metrics.div_index(shares=short_votes_list, q=q, metric_type=div_index_metrics)
        != 0
    )


def test_dispr_not_0(short_votes_list, allocations, dispr_index_metrics):
    assert (
        metrics.dispr_index(
            shares=short_votes_list,
            allocations=allocations,
            metric_type=dispr_index_metrics,
        )
        != 0
    )


def test_effective_number_of_groups_not_0(short_votes_list, effective_group_metrics):
    assert (
        metrics.effective_number_of_groups(
            shares=short_votes_list, metric_type=effective_group_metrics
        )
        != 0
    )
