"""
Utility functions for general operations and coloration

Contents
--------
  0. No Class
      head_shape
      wrap_print_list

      normalize

      gen_list_of_lists
      gen_faction_groups
"""

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
