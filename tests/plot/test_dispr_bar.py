# SPDX-License-Identifier: BSD-3-Clause
"""
Disproportionality bar plot tests.
"""

import matplotlib.pyplot as plt

from poli_sci_kit.plot import disproportionality_bar_plot


def test_disproportionality_bar_plot(monkeypatch, short_votes_list, allocations):
    monkeypatch.setattr(plt, "show", lambda: None)
    disproportionality_bar_plot(
        shares=short_votes_list,
        allocations=allocations,
        percent=False,
    )


def test_disproportionality_bar_plot_percent(
    monkeypatch, short_votes_list, allocations
):
    monkeypatch.setattr(plt, "show", lambda: None)
    disproportionality_bar_plot(
        shares=short_votes_list,
        allocations=allocations,
        percent=True,
    )


def test_disproportionality_bar_plot_subset(
    monkeypatch, short_votes_list, allocations, total_shares, seats
):
    monkeypatch.setattr(plt, "show", lambda: None)
    disproportionality_bar_plot(
        shares=short_votes_list[:3],
        allocations=allocations[:3],
        total_shares=total_shares,
        total_alloc=seats,
        percent=True,
    )
