# SPDX-License-Identifier: BSD-3-Clause
"""
Parliament plot tests.
"""

import matplotlib.pyplot as plt
import pytest

from poli_sci_kit.plot import parliament_plot


def test_semicircle_parliament_plot(monkeypatch, allocations):
    monkeypatch.setattr(plt, "show", lambda: None)
    parliament_plot(allocations=allocations, style="semicircle")


def test_rectangle_parliament_plot(monkeypatch, allocations):
    monkeypatch.setattr(plt, "show", lambda: None)
    parliament_plot(allocations=allocations, style="rectangle")


def test_parliament_plot_row_exception():
    with pytest.raises(
        ValueError,
        match="Cannot allocate 12 seats into 4 rows. Try a smaller number of rows.",
    ):
        parliament_plot(allocations=[2, 2, 8], num_rows=4)
