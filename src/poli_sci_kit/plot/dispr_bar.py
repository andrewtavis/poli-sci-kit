"""
Disproportionality Bar Plot
---------------------------

The plotting function to create disproportionality bar plots.

Contents:
    dispr_bar
"""

import pandas as pd
import seaborn as sns
from poli_sci_kit import utils

default_sat = 0.95


def dispr_bar(
    shares,
    allocations,
    labels=None,
    colors=None,
    total_shares=None,
    total_alloc=None,
    percent=False,
    dsat=default_sat,
    axis=None,
):
    """
    Plots the difference in allocated seats to received shares.

    Parameters
    ----------
        shares : list
            The shares amounts or those that allocations should be compared to

        allocations : list
            The allocated amounts

        labels : list (default=None)
            A list of group names as labels for the x-axis

        colors : list or list of lists : optional (default=None)
            The colors of the groups as hex keys

        total_shares : int (default=None)
            The total share amounts
            Note: allows for subsets of the total groups

        total_alloc : int (default=None)
            The total number of allocations amounts
            Note: allows for subsets of the total groups

        percent : bool (default=False)
            Whether the y-axis should depict relative changes or not

        dsat : float : optional (default=default_sat)
            The degree of desaturation to be applied to the colors

        axis : str : optional (default=None)
            Adds an axis to plots so they can be combined

    Returns
    -------
        ax : matplotlib.pyplot.subplot
            A bar plot with aggregate or relative seat-share differences and bar widths representing share proportions
    """
    assert len(shares) == len(
        allocations
    ), "The number of different shares must equal the number of different seat allocations."

    if total_shares and total_alloc:
        share_percents = [i / total_shares for i in shares]
        seat_percents = [i / total_alloc for i in allocations]
    else:
        share_percents = [i / sum(shares) for i in shares]
        seat_percents = [i / sum(allocations) for i in allocations]

    disproportionality = [
        round(seat_percents[i] - p, 4) for i, p in enumerate(share_percents)
    ]

    if percent == True:
        disproportionality = [
            round(disproportionality[i] / p * 100, 4)
            for i, p in enumerate(share_percents)
        ]

    if not labels:
        labels = list(range(len(disproportionality) + 1)[1:])

    df = pd.DataFrame(disproportionality, index=labels, columns=["disproportionality"])

    if colors:
        assert len(colors) == len(
            shares
        ), "The number of colors provided doesn't match the number of counts to be displayed"
        colors = [
            utils.scale_saturation(rgb_trip=utils.hex_to_rgb(c), sat=dsat)
            for c in colors
        ]
        sns.set_palette(colors)

    elif colors == None:
        sns.set_palette("deep")  # default sns palette
        colors = [
            utils.rgb_to_hex(c)
            for c in sns.color_palette(n_colors=len(shares), desat=1)
        ]

    ax = sns.barplot(
        data=df, x=df.index, y="disproportionality", saturation=dsat, ax=axis
    )
    # Change widths by looping over the bars and adjusting the width/position
    bar_widths = []
    bar_positions = []
    prev_bar_position = 0
    for bar, new_width in zip(ax.patches, share_percents):
        bar.set_x(prev_bar_position)
        bar.set_width(new_width * len(df))

        prev_bar_position += new_width * len(df)
        bar_widths.append(new_width * len(df))
        bar_positions.append(prev_bar_position)

    # Add heights to the top and bottom of bars
    for p in ax.patches:
        height = p.get_height()
        if height < 0:  # compensates for text height for negative bar labels
            ax.text(
                x=p.get_x() + p.get_width() / 2.0,
                y=height
                + 1.5 * min([abs(i) for i in disproportionality]) * -1,  # put below
                s=str(height),
                ha="center",
            )
        else:
            ax.text(
                x=p.get_x() + p.get_width() / 2.0,
                y=height + 0.75 * min([abs(i) for i in disproportionality]),
                s=str(height),
                ha="center",
            )

    ax.set_xlim([0, prev_bar_position * 1.05])
    ax.axhline(0, ls="-", color="black")  # so the x-axis is distinct
    ax.set_xticks(
        ticks=[p - (bar_widths[i] / 2.0) for i, p in enumerate(bar_positions)]
    )
    ax.set_xticklabels(labels=[labels[i] for i in range(len(bar_widths))])

    ax.set_ylim([min(disproportionality) * 1.5, max(disproportionality) * 1.5])
    ax.set_xlim([0, len(shares)])

    return ax
