# SPDX-License-Identifier: BSD-3-Clause
"""
The plotting function to create parliament plots.
"""

import pandas as pd
import seaborn as sns
from matplotlib.axes import Axes

from poli_sci_kit.utils import (
    gen_parliament_plot_points,
    hex_to_rgb,
    rgb_to_hex,
    scale_saturation,
)

default_sat = 0.95


def parliament_plot(
    allocations: list,
    labels: list[str] | None = None,
    colors: list | None = None,
    style: str = "semicircle",
    num_rows: int = 2,
    marker_size: int | float = 200,
    speaker: bool = False,
    df_seat_lctns: pd.DataFrame | None = None,
    dsat: float = default_sat,
    axis: str | None = None,
    legend: bool = False,
    **kwargs,
) -> Axes:
    """
    Produce a parliament plot given seat allocations.

    Parameters
    ----------
    allocations : list
        The share of seats given to the regions or parties.

    labels : list[str] : optional (default=None)
        The names of the groups.

    colors : list : optional (default=None)
        The colors of the groups as hex keys.

    style : str (default=semicircle)
        Whether to plot the parliament as a semicircle or a rectangle.

    num_rows : int (default=2)
        The number of rows in the plot.

    marker_size : int or float (default=200)
        The size of the scatter plot markers that make up the plot.

    speaker : bool : optional (default=False)
        Whether to include a point for the speaker of the house colored by their group.

        Note: 'True' colors the point based on the largest group, but passing a name from 'labels' is also possible.

    df_seat_lctns : pd.DataFrame : optional (default=None)
        A df of coordinates to plot.

    dsat : float : optional (default=default_sat)
        The degree of desaturation to be applied to the colors.

    axis : str : optional (default=None)
        Adds an axis to plots so they can be combined.

    legend : bool : optional (default=False)
        Whether to display a legend.

    **kwargs : dict
        Optional keyword arguments to be passed to sns.scatter plot.

    Returns
    -------
    Axes
        Parliament seat distribution as either an arc or a rectangle, each having the option to be converted to seats.
    """
    assert num_rows <= sum(allocations), (
        "The number of rows cannot exceed the number of seats to be allocated."
    )

    if colors:
        assert len(colors) == len(allocations), (
            "The number of colors provided doesn't match the number of counts to be displayed."
        )

    elif colors is None:
        sns.set_palette("deep")  # default sns palette
        colors = [
            rgb_to_hex(c) for c in sns.color_palette(n_colors=len(allocations), desat=1)
        ]

    colors = [scale_saturation(rgb_triple=hex_to_rgb(c), sat=dsat) for c in colors]
    sns.set_palette(colors)

    if df_seat_lctns is None:
        df_seat_lctns = gen_parliament_plot_points(
            allocations=allocations,
            labels=labels,
            style=style,
            num_rows=num_rows,
            speaker=speaker,
        )

    if style == "rectangle":
        if labels is None:
            labels = list(df_seat_lctns["group"].unique())

        marker = "s"
        # Loop through groups and plot their allocations.
        for g, lbl in enumerate(labels):
            df_subsetted = df_seat_lctns[df_seat_lctns["group"] == lbl]

            ax = sns.scatterplot(
                data=df_subsetted,
                x="x_loc",
                y="y_loc",
                color=colors[g],
                marker=marker,
                s=marker_size,
                edgecolor="#D2D2D3",  # edge color same as legend outline
                ax=axis,
                legend=legend,
                **kwargs,
            )

    elif style == "semicircle":
        marker = "o"

        ax = sns.scatterplot(
            data=df_seat_lctns,
            x="x_loc",
            y="y_loc",
            hue="group",
            marker=marker,
            s=marker_size,
            edgecolor="#D2D2D3",  # edge color same as legend outline
            ax=axis,
            legend=legend,
            **kwargs,
        )

    # Make plot a proportional and remove background axes.
    ax.axis("equal")
    ax.axis("off")

    return ax
