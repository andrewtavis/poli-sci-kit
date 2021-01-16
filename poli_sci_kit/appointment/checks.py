"""
Functions to conditionally check appointment methods

Contents
--------
  0. No Class
      quota_condition
      consistency_condition
"""

import pandas as pd
from math import ceil, floor

from poli_sci_kit.appointment.metrics import ideal_share


def quota_condition(all_shares, all_seats):
    """
    Checks whether assignment method results fall within the range of the ideal share rounded down and up

    Parameters
    ----------
        all_shares : list
            The preportion of the population or votes for the regions or parties

        all_seats : list
            The share of seats given to the regions or parties

    Returns
    -------
        check_pass or fail_report: bool or list (contains tuples)
            A value of True, or a list of corresponding arguments where the check has failed and their indexes
    """
    assert len(all_shares) == len(
        all_seats
    ), "The total different shares of a population or vote must equal that of the allocated seats."

    check_list = [
        ceil(ideal_share(all_shares[i], sum(all_shares), sum(all_seats)))
        >= all_seats[i]
        and floor(ideal_share(all_shares[i], sum(all_shares), sum(all_seats)))
        <= all_seats[i]
        for i in range(len(all_shares))
    ]

    fail_report = {}
    for i in range(len(check_list)):
        if check_list[i] == False:
            fail_report[i] = (all_shares[i], all_seats[i])

    check_pass = False not in check_list
    print("Quota condition passed:", check_pass)

    if not check_pass:
        print("Returning list of argument elements that failed the condition.")
        return fail_report

    else:
        return check_pass


def consistency_condition(
    all_var_shares=None, all_var_seats=None, check_type="seat_monotony"
):
    """
    Checks the consistency of assignment method results given dataframes of shares and allocations
    Rows and columns of the df(s) will be marked and dropped if consistent, with a failed condition being if the resulting df has size > 0 (some where inconsistent)

    Parameters
    ----------
        all_var_shares : pd.DataFrame (num_region_party, num_variation; contains ints, default=None)
            Preportions of the population or votes for the regions or parties given variance

        all_var_seats : pd.DataFrame (num_region_party, num_variation; contains ints, default=None)
            Shares of seats given to the regions or parties given variance

        check_type : str
            Whether the consistency of a change in seats or a change in shares is checked

            Options:
                The style of monotony to derive the consistency with

                - seat_monotony : An incease in total seats does not decrease alloted seats
                    Note: use sums of cols of all_var_seats, checking col element monotony given a differences in sums

                - share_monotony : An incease in share does not decrease alloted seats
                    Note: use rows of all_var_shares and check coinciding elements of all_var_seats for monotony

    Returns
    -------
        check_pass or df_fail_report: bool or pd.DataFrame (contains ints)
            A value of True, or False with a df of corresponding arguments where the check has failed
    """
    if all_var_shares is not None and all_var_seats is not None:
        assert (
            all_var_shares.shape == all_var_seats.shape
        ), "The number of share variations must be equal to the number of seat allocation variations."

    if check_type == "seat_monotony":
        df_fail_report = all_var_seats.copy()

        seat_sums = [all_var_seats[col].sum() for col in all_var_seats.columns]
        seat_sums_sorted_indexes = [
            tup[0] for tup in sorted(enumerate(seat_sums), key=lambda i: i[1])
        ]

        # Order seat allocation columns by increasing total
        all_var_seats = all_var_seats[
            [all_var_seats.columns[i] for i in seat_sums_sorted_indexes]
        ]

        # Check that elements of each column are less than corresponding ones in later columns
        check_cols = [
            [
                all_var_seats.loc[:, all_var_seats.columns[j]]
                <= all_var_seats.loc[:, all_var_seats.columns[i]]
                for i in range(len(all_var_seats.columns))[j:]
            ]
            for j in range(len(all_var_seats.columns))
        ]

        # Return True if the column elements are always less than following ones, or the str of the later columns that break the condition
        # str() is used to assure that 1 != True in the later sets
        check_cols = [
            [True if i[j].all() == True else str(j) for j in range(len(i))]
            for i in check_cols
        ]

        # Return True if the column's total allotment passes the condition, or the index of columns with which the column fails
        check_cols = [
            True
            if list(set(check_cols[i]))[0] == True and len(set(check_cols[i])) == 1
            else [i + int(item) for item in list(set(check_cols[i])) if item != True]
            for i in range(len(check_cols))
        ]

        col_range = list(range(len(df_fail_report.columns)))  # list to use .pop()

        cols_droppped = 0
        for i in col_range:
            if check_cols[i] == True:
                # Drop the column, and add to an indexer to maintain lengths
                df_fail_report.drop(
                    df_fail_report.columns[i - cols_droppped], axis=1, inplace=True
                )
                cols_droppped += 1
            else:
                # Keep the column, and remove the indexes of any columns that break the condition to keep them as well
                for later_col in check_cols[i]:
                    col_range.pop(later_col)

        # Find elements in a row that are greater than following elements
        check_rows = [
            [
                [
                    df_fail_report.loc[row, df_fail_report.columns[col]]
                    <= df_fail_report.loc[row, df_fail_report.columns[col_after]]
                    for col_after in range(len(df_fail_report.columns))[col:]
                ]
                for col in range(len(df_fail_report.columns))
            ]
            for row in df_fail_report.index
        ]

        check_rows = [
            [
                True
                if list(set(comparison))[0] == True and len(set(comparison)) == 1
                else False
                for comparison in i
            ]
            for i in check_rows
        ]
        check_rows = [
            True if list(set(i))[0] == True and len(set(i)) == 1 else False
            for i in check_rows
        ]

        rows_droppped = 0
        for i in range(len(df_fail_report.index)):
            if check_rows[i] == True:
                # Drop the row if no elements are greater than following ones, and add to an indexer to maintain lengths
                df_fail_report.drop(
                    df_fail_report.index[i - rows_droppped], axis=0, inplace=True
                )
                rows_droppped += 1

    elif check_type == "share_monotony":
        # The fail report df has share and seat columns alternated
        df_fail_report = pd.DataFrame()
        for i in range(len(all_var_shares.columns)):
            df_fail_report.loc[:, all_var_shares.columns[i]] = pd.Series(
                all_var_shares[all_var_shares.columns[i]], index=all_var_shares.index
            )
            df_fail_report.loc[:, all_var_seats.columns[i]] = pd.Series(
                all_var_seats[all_var_seats.columns[i]], index=all_var_seats.index
            )

        # Check which share and seat columns are less than one another
        check_share_rows = [
            [
                [
                    all_var_shares.loc[row, all_var_shares.columns[col]]
                    <= all_var_shares.loc[row, all_var_shares.columns[other_col]]
                    for other_col in range(len(all_var_shares.columns))
                ]
                for col in range(len(all_var_shares.columns))
            ]
            for row in all_var_shares.index
        ]

        check_seat_rows = [
            [
                [
                    all_var_seats.loc[row, all_var_seats.columns[col]]
                    <= all_var_seats.loc[row, all_var_seats.columns[other_col]]
                    for other_col in range(len(all_var_seats.columns))
                ]
                for col in range(len(all_var_seats.columns))
            ]
            for row in all_var_seats.index
        ]

        # Combine the above for indexes where the condition is met and not
        check_shares_seats = [
            [
                [
                    False
                    if check_share_rows[i][j][k] == True
                    and check_seat_rows[i][j][k] != True
                    else True
                    for k in range(len(check_share_rows[0][0]))
                ]
                for j in range(len(check_share_rows[0]))
            ]
            for i in range(len(check_share_rows))
        ]

        rows_kept = []
        for row in range(len(df_fail_report.index)):
            row_element_checker = 0
            for element_check in check_shares_seats[row]:
                if list(set(element_check))[0] == True and len(set(element_check)) == 1:
                    row_element_checker += 1

            if row_element_checker == len(check_shares_seats[row]):
                df_fail_report.drop(df_fail_report.index[row], axis=0, inplace=True)
            else:
                rows_kept.append(row)

        # Column indexes, indexing over pairs as share and seat columns are dropped together
        col_pair_range = list(range(int(len(df_fail_report.columns) / 2)))

        # Indexing which columns to keep
        col_pairs_to_keep = []
        for row in rows_kept:
            for col in col_pair_range:
                if (
                    list(set(check_shares_seats[row][col]))[0] != True
                    or len(set(check_shares_seats[row][col])) != 1
                ):
                    col_pairs_to_keep.append(col)

                    for later_col in range(len(check_shares_seats[row][col])):
                        if check_shares_seats[row][col][later_col] == False:
                            col_pairs_to_keep.append(later_col)

        col_pairs_to_keep = list(set(col_pairs_to_keep))

        # Return those columns to be dropped
        cols_to_keep = [[2 * i, 2 * i + 1] for i in col_pairs_to_keep]
        cols_to_keep = [item for sublist in cols_to_keep for item in sublist]

        cols_droppped = 0
        for col in range(len(df_fail_report.columns)):
            if col not in cols_to_keep:
                df_fail_report.drop(
                    df_fail_report.columns[col - cols_droppped], axis=1, inplace=True
                )
                cols_droppped += 1

    else:
        ValueError(
            "The 'check_type' argument myst be either seat_monotony or share_monotony"
        )

    check_pass = len(df_fail_report) == 0
    print(
        f"Consistency condition based on {check_type.split('_')[0]} monotony passed:",
        check_pass,
    )

    if not check_pass:
        print("Returning df of argument elements that failed the condition.")
        return df_fail_report

    else:
        return check_pass
