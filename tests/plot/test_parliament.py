# SPDX-License-Identifier: BSD-3-Clause
"""
Parliament plot tests.
"""

import matplotlib.pyplot as plt
from poli_sci_kit import plot
import pytest


def test_semicircle_parl_plot(monkeypatch, allocations):
    monkeypatch.setattr(plt, "show", lambda: None)
    plot.parliament(allocations=allocations, style="semicircle")


def test_rectangle_parl_plot(monkeypatch, allocations):
    monkeypatch.setattr(plt, "show", lambda: None)
    plot.parliament(allocations=allocations, style="rectangle")


def test_parl_plot_row_exception():
    with pytest.raises(
        ValueError,
        match="Cannot allocate 12 seats into 4 rows. Try a smaller number of rows.",
    ):
        plot.parliament(allocations=[2, 2, 8], num_rows=4)
