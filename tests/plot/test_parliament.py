"""
Parliament Plot Tests
---------------------
"""

import matplotlib.pyplot as plt
from poli_sci_kit import plot


def test_semicircle_parl_plot(monkeypatch, allocations):
    monkeypatch.setattr(plt, "show", lambda: None)
    plot.parliament(allocations=allocations, style="semicircle")


def test_rectangle_parl_plot(monkeypatch, allocations):
    monkeypatch.setattr(plt, "show", lambda: None)
    plot.parliament(allocations=allocations, style="rectangle")
