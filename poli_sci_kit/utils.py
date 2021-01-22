"""
Utility functions for general operations and plotting

Contents
--------
  0. No Class
      normalize

      gen_list_of_lists
      gen_faction_groups

      gen_parl_points
      swap_parl_allocations
"""

import numpy as np
import pandas as pd


def normalize(vals):
    """Returns respective normalized values"""
    total_vals = sum(vals)
    proportions = [1.0 * v / total_vals for v in vals]

    return proportions


def gen_list_of_lists(original_list, new_structure):
    """Generates a list of lists with a given structure from a given list"""
    assert len(original_list) == sum(
        new_structure
    ), "The number of elements in the original list and desired structure don't match"

    list_of_lists = [
        [original_list[i + sum(new_structure[:j])] for i in range(new_structure[j])]
        for j in range(len(new_structure))
    ]

    return list_of_lists


def gen_faction_groups(original_list, factions_indexes):
    """
    Reorders a list into a list of lists where sublists are faction amounts

    Parameters
    ----------
        original_list : list
            The data to be reorganizaed

        factions_indexes : list of lists (contains ints)
           The structure of original_list indexes to output

    Returns
    -------
        factioned_list : list of lists
            The values of original_list ordered as the indexes of factions_indexes
    """
    factions_structure = [len(sublist) for sublist in factions_indexes]
    flat_indexes = [item for sublist in factions_indexes for item in sublist]
    ordered_original_list = [original_list[i] for i in flat_indexes]
    factioned_list = gen_list_of_lists(ordered_original_list, factions_structure)

    return factioned_list


def gen_parl_points(
    allocations, names=None, style="semicircle", num_rows=2, speaker=False
):
    """
    Produces a df with coordinates for a parliament plot

    Parameters
    ----------
        allocations : list
            The share of seats given to the regions or parties

        names : list : optional (default=None)
            The names of the groups

        style : str (default=semicircle)
            Whether to plot the parliament as a semicircle or a rectangle

        num_rows : int (default=2)
            The number of rows in the plot

        speaker : bool : optional (default=False)
            Whether to include a point for the speaker of the house colored by their group
            Note: 'True' colors the point based on the largest group, but passing a name from 'names' is also possible

    Returns
    -------
        df_seat_lctns : pd.DataFrame
            A dataframe with points to be converted to a parliament plot via seaborn's scatterplot
    """
    total_seats = sum(allocations)

    if not names:
        # For dataframe assignment
        names = [f"group_{i}" for i in range(len(allocations))]

    if speaker:
        assert (speaker == True) or (
            speaker in names
        ), "Either the 'speaker' argument must be true, or must match an element from the provided 'names' argument"
        total_seats -= 1
        allocations = list(allocations)

        if speaker == True:
            assert (
                len([c for c in allocations if c == max(allocations)]) == 1
            ), "Two parties got the highest number of seats in the allocation. Please assign the speaker via passing one of their names."

            largest_group_index = allocations.index(max(allocations))
            allocations[largest_group_index] -= 1

            # Reassign 'speaker' to the largest group's name so it can be assigned later
            speaker = names[largest_group_index]

        elif speaker in names:
            largest_group_index = names.index(speaker)
            allocations[largest_group_index] -= 1

    # Make an empty dataframe and fill it with coordinates for the structure
    # Then assign group values for allocation based on the rows
    df_seat_lctns = pd.DataFrame(
        columns=["group", "row", "row_position", "x_loc", "y_loc"]
    )

    if style == "semicircle":

        def arc_coordinates(r, seats):
            """
            Generates an arc of the parliament plot given a radius and the number of seats
            """
            angles = np.linspace(start=np.pi, stop=0, num=seats)
            x_coordinates, y_coordinates = [], []

            # Broadcast angles to their corresponding coordinates
            x_coordinates = list(r * np.cos(angles))
            y_coordinates = list(r * np.sin(angles))

            return x_coordinates, y_coordinates

        xs, ys = [], []
        radii = range(2, 2 + num_rows)

        row_seats = [int(total_seats / num_rows)] * num_rows
        extra_seat = total_seats - sum(
            row_seats
        )  # 0 or 1 based on whether the seats divide evenly into the rows
        row_seats[-1] += extra_seat

        # Shift the seats per row such that it's always increasing
        if num_rows % 2 != 0:
            seats_shift = list(range(-int(num_rows / 2), int(num_rows / 2) + 1, 1))
        else:
            positive_shift = list(range(1, int(num_rows / 2) + 1, 1))
            negative_shift = [-1 * i for i in positive_shift[::-1]]
            seats_shift = negative_shift + positive_shift

        seats_shift = [
            i * int(num_rows / 2) for i in seats_shift
        ]  # greater shift for higher rows for more equal spacing
        seats_per_row = [row_seats[i] + seats_shift[i] for i in range(len(row_seats))]

        row_indexes = []
        row_position_indexes = []
        for i in range(len(seats_per_row)):
            arc_xs, arc_ys = arc_coordinates(radii[i], seats_per_row[i])
            xs += arc_xs
            ys += arc_ys
            row_indexes += [i] * seats_per_row[i]
            # List of lists for position indexes such that they can be accessed by row and position
            row_position_indexes += [list(range(seats_per_row[i]))]

        for i in range(total_seats):
            df_seat_lctns.loc[i, "x_loc"] = xs[i]
            df_seat_lctns.loc[i, "y_loc"] = ys[i]

        df_seat_lctns["row"] = row_indexes
        df_seat_lctns["row_position"] = [
            item for sublist in row_position_indexes for item in sublist
        ]

        # Index the group and depleat a copy of allocations at its location
        group_index = 0
        seats_to_allocate = allocations.copy()
        row_index = 0

        while total_seats > 0:
            # Assign based on row and the current index within that row
            if row_position_indexes[row_index] != []:
                index_to_assign = [
                    i
                    for i in df_seat_lctns.index
                    if df_seat_lctns.loc[i, "row"] == row_index
                    and df_seat_lctns.loc[i, "row_position"]
                    == row_position_indexes[row_index][0]
                ][0]

                df_seat_lctns.loc[index_to_assign, "group"] = names[group_index]

                total_seats -= 1

                seats_to_allocate[group_index] -= 1
                if seats_to_allocate[group_index] == 0:
                    group_index += 1

                row_position_indexes[row_index].pop(0)

                row_index += 1
                if row_index == num_rows:
                    row_index = 0

                # Make sure that radii are filled before rows are completed
                for i in range(num_rows):
                    if len(row_position_indexes[i]) < i + 2:
                        if i != 0:
                            row_index -= 1
                        else:
                            row_index = num_rows - 1

            else:
                while row_position_indexes[row_index] == []:
                    row_index += 1

    elif style == "rectangle":
        x_coordinate = 0

        # y_coordinates are split by baseline of 2 units, with double that for the middle aisle
        equa_distant_indexes = list(range(0, num_rows * 2, 2))
        y_coordinates = [
            i
            if (
                equa_distant_indexes.index(i) < int(len(equa_distant_indexes) / 2)
                and len(equa_distant_indexes) % 2 == 0
            )
            or (
                equa_distant_indexes.index(i) < int(len(equa_distant_indexes) / 2) + 1
                and len(equa_distant_indexes) % 2 != 0
            )
            else i + 2
            for i in equa_distant_indexes
        ]

        if num_rows == 1:
            for i in range(total_seats):
                df_seat_lctns.loc[i, "x_loc"] = x_coordinate
                df_seat_lctns.loc[i, "y_loc"] = 0

                x_coordinate += 2

            df_seat_lctns["row"] = [0] * len(df_seat_lctns)
            list_of_name_lists = [
                [names[i]] * allocations[i] for i in range(len(allocations))
            ]
            df_seat_lctns["group"] = [
                item for sublist in list_of_name_lists for item in sublist
            ]

        else:
            row_index = 0
            position_index = 0
            row_seats_no_remainder = int(total_seats / num_rows) * num_rows

            for i in range(row_seats_no_remainder):
                y_coordinate = y_coordinates[row_index]
                df_seat_lctns.loc[i, "row"] = row_index
                df_seat_lctns.loc[i, "row_position"] = position_index
                df_seat_lctns.loc[i, "x_loc"] = x_coordinate
                df_seat_lctns.loc[i, "y_loc"] = y_coordinate

                x_coordinate += 2
                position_index += 1

                # Reset to the start of the next row
                if (i + 1) % int(total_seats / num_rows) == 0:
                    row_index += 1
                    x_coordinate = 0
                    position_index = 0

            # Add last seats that were rounded off
            max_x = max(df_seat_lctns["x_loc"])
            max_pos = max(df_seat_lctns["x_loc"])
            row_index = 0  # reset to first row
            for i in list(range(total_seats))[row_seats_no_remainder:]:
                y_coordinate = y_coordinates[row_index]
                df_seat_lctns.loc[i, "row"] = row_index
                df_seat_lctns.loc[i, "row_position"] = max_pos + 1
                df_seat_lctns.loc[i, "x_loc"] = max_x + 2
                df_seat_lctns.loc[i, "y_loc"] = y_coordinate
                row_index += 1

            # Sort df for index based assignment
            df_seat_lctns.sort_values(
                ["row", "x_loc", "y_loc"], ascending=[True, True, True], inplace=True
            )
            df_seat_lctns.reset_index(inplace=True, drop=True)

            # Define the top and bottom rows so they can be filled in order
            top_rows = y_coordinates[int((len(y_coordinates) + 1) / 2) :]
            bottom_rows = y_coordinates[: int((len(y_coordinates) + 1) / 2)]

            # Find the total seats in each section to be depleated
            total_top_seats = 0
            for row in top_rows:
                total_top_seats += len(df_seat_lctns[df_seat_lctns["y_loc"] == row])

            total_bottom_seats = 0
            for row in bottom_rows:
                total_bottom_seats += len(df_seat_lctns[df_seat_lctns["y_loc"] == row])

            # Index the group and depleat a copy of allocations at its location
            group_index = 0
            seats_to_allocate = allocations.copy()

            # Top assignment from low to high and left to right
            top_x = 0
            top_y = top_rows[0]

            while total_top_seats > 0:
                index_to_assign = [
                    i
                    for i in df_seat_lctns.index
                    if df_seat_lctns.loc[i, "x_loc"] == top_x
                    and df_seat_lctns.loc[i, "y_loc"] == top_y
                ][0]

                df_seat_lctns.loc[index_to_assign, "group"] = names[group_index]

                seats_to_allocate[group_index] -= 1
                if seats_to_allocate[group_index] == 0:
                    group_index += 1

                if top_y == top_rows[-1]:
                    # Move right and reset vertical
                    top_x += 2
                    top_y = top_rows[0]

                else:
                    # Move up
                    top_y += 2

                total_top_seats -= 1

            # Bottom assignment from high to low and right to left
            bottom_x = max(df_seat_lctns["x_loc"])
            bottom_y = bottom_rows[-1]
            # Fix initial position in case of unequal seats per row
            while (
                len(
                    [
                        i
                        for i in df_seat_lctns.index
                        if df_seat_lctns.loc[i, "x_loc"] == bottom_x
                        and df_seat_lctns.loc[i, "y_loc"] == bottom_y
                    ]
                )
                == 0
            ):
                # Move down
                bottom_y -= 2

            while total_bottom_seats > 0:
                index_to_assign = [
                    i
                    for i in df_seat_lctns.index
                    if df_seat_lctns.loc[i, "x_loc"] == bottom_x
                    and df_seat_lctns.loc[i, "y_loc"] == bottom_y
                ][0]

                df_seat_lctns.loc[index_to_assign, "group"] = names[group_index]

                seats_to_allocate[group_index] -= 1
                if seats_to_allocate[group_index] == 0:
                    group_index += 1

                if bottom_y == bottom_rows[0]:
                    # Move left and reset vertical
                    bottom_x -= 2
                    bottom_y = bottom_rows[-1]

                else:
                    # Move down
                    bottom_y -= 2

                total_bottom_seats -= 1

    else:
        ValueError("The 'style' argument must be either 'semicircle' or 'rectangle'")

    if speaker:
        index_to_assign = len(df_seat_lctns)

        if style == "semicircle":
            df_seat_lctns.loc[index_to_assign, "x_loc"] = 0
            df_seat_lctns.loc[index_to_assign, "y_loc"] = 0
            df_seat_lctns.loc[index_to_assign, "group"] = speaker

        elif style == "rectangle":
            if len(y_coordinates) % 2 == 0:
                middle_index_1 = len(y_coordinates) / 2 - 1
                middle_index_2 = len(y_coordinates) / 2

                y_coordinate = (
                    y_coordinates[int(middle_index_1)]
                    + y_coordinates[int(middle_index_2)]
                ) / 2

            else:
                middle_index = int(len(y_coordinates) / 2)
                y_coordinate = float(y_coordinates[middle_index] + 2)

            df_seat_lctns.loc[index_to_assign, "x_loc"] = 0
            df_seat_lctns.loc[index_to_assign, "y_loc"] = y_coordinate
            df_seat_lctns.loc[index_to_assign, "group"] = speaker

    return df_seat_lctns


def swap_parl_allocations(df, row_1, pos_1, row_2, pos_2):
    """
    Replaces two allocations of the parliament plot df to clean up coloration

    Parameters
    ----------
        row_1 : int
            The row of one seat to swap

        pos_1 : int
            The position in the row of one seat to swap

        row_2 : int
            The row of the other seat to swap

        pos_2 : int
            The position in the row of the other seat to swap

    Returns
    -------
        df_seat_lctns : pd.DataFrame
            A parliament plot allocations data frame with two allocations swapped
    """
    allocation_1 = df[(df["row"] == row_1) & (df["row_position"] == pos_1)][
        "group"
    ].values[0]
    index_1 = df[(df["row"] == row_1) & (df["row_position"] == pos_1)].index

    allocation_2 = df[(df["row"] == row_2) & (df["row_position"] == pos_2)][
        "group"
    ].values[0]
    index_2 = df[(df["row"] == row_2) & (df["row_position"] == pos_2)].index

    df.loc[index_1, "group"] = allocation_2
    df.loc[index_2, "group"] = allocation_1
