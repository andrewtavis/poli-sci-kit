# SPDX-License-Identifier: BSD-3-Clause
"""
Utilities for tests.
"""

from poli_sci_kit.utils import (
    gen_faction_groups,
    gen_list_of_lists,
    gen_parliament_plot_points,
    hex_to_rgb,
    normalize,
    rgb_to_hex,
    scale_saturation,
    swap_parliament_allocations,
)


def test_normalize():
    assert sum(normalize([1, 2, 3, 4, 5])) == 1.0


def test_gen_list_of_lists():
    test_list = [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert gen_list_of_lists(original_list=test_list, new_structure=[3, 3, 3]) == [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
    ]


def test_gen_faction_groups():
    test_list = ["a", "b", "c", "d", "e", "f"]
    assert gen_faction_groups(
        original_list=test_list, factions_indexes=[[0, 1, 5], [2, 3, 4]]
    ) == [
        ["a", "b", "f"],
        [
            "c",
            "d",
            "e",
        ],
    ]


def test_semicircle_parliament_plot(allocations):
    test_df = gen_parliament_plot_points(
        allocations=allocations,
        style="semicircle",
        num_rows=2,
        speaker=False,
    )

    assert list(test_df["row"]) == [
        0,
        1,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
    ]
    assert list(test_df["row_position"]) == [
        0,
        0,
        1,
        1,
        2,
        2,
        3,
        3,
        4,
        4,
        5,
        6,
        5,
        7,
        6,
        8,
        7,
        9,
        8,
        10,
    ]

    test_df = gen_parliament_plot_points(
        allocations=allocations,
        style="semicircle",
        num_rows=2,
        speaker=True,
    )

    assert test_df["x_loc"][len(test_df) - 1] == 0
    assert test_df["y_loc"][len(test_df) - 1] == 0


def test_rectangle_parliament_plot(allocations):
    assert list(
        gen_parliament_plot_points(
            allocations=allocations,
            style="rectangle",
            num_rows=4,
            speaker=False,
        )["row"]
    ) == [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3]

    assert list(
        gen_parliament_plot_points(
            allocations=allocations,
            style="rectangle",
            num_rows=4,
            speaker=False,
        )["row_position"]
    ) == [0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4, 0, 1, 2, 3, 4]

    test_df = gen_parliament_plot_points(
        allocations=allocations,
        style="rectangle",
        num_rows=4,
        speaker=True,
    )

    assert test_df["x_loc"][len(test_df) - 1] == 0
    assert test_df["y_loc"][len(test_df) - 1] == 4


def test_swap_parliament_allocations(allocations):
    test_df = gen_parliament_plot_points(
        allocations=allocations,
        style="rectangle",
        num_rows=4,
        speaker=False,
    )

    test_swap_df = test_df.copy()
    swap_parliament_allocations(df=test_swap_df, row_0=0, pos_0=0, row_1=0, pos_1=1)

    assert test_df["group"][0] == test_swap_df["group"][1]


def test_hex_to_rgb():
    assert hex_to_rgb("#ffffff").get_value_tuple() == (1.0, 1.0, 1.0)


def test_rgb_to_hex():
    assert rgb_to_hex((1.0, 1.0, 1.0)) == "#ffffff"


def test_scale_saturation():
    assert scale_saturation((1, 1, 1), 0.95) == (0.95, 0.95, 0.95)
