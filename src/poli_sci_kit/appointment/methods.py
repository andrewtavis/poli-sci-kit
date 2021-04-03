"""
Appointment Methods
-------------------

Methods used to derive allocations based on received shares.

Contents:
    largest_remainder (aka Hamilton, Vinton, Hare–Niemeyer)

        Options: Hare, Droop, Hagenbach–Bischoff

    highest_averages

        Options: Jefferson, Webster, Huntington-Hill
"""

from math import ceil, modf, sqrt
from operator import itemgetter
from random import shuffle


def largest_remainder(
    quota_style="Hare",
    shares=None,
    total_alloc=None,
    alloc_threshold=None,
    min_alloc=None,
    tie_break="majority",
    majority_bonus=False,
):
    """
    Apportion seats using the Largest Remainder (Hamilton, Vinton, Hare–Niemeyer) methods.

    Parameters
    ----------
        quota_style : str (default=Hare)
            The style of quota vote-seat quota to use

            Options:
                Each defines a divisor from which remainders are defined

                - Hare :

                    .. math::
                        quota_hare = \frac{total shares}{total allocations}

                    Note: the simplest form of largest remainder quota

                - Droop :

                    .. math::
                        quota_droop = int(\frac{total shares}{total allocations + 1}) + 1

                    Note: favors larger groups more than the Hare quota

                - Hagenbach–Bischoff :

                    .. math::
                        quota_hb = \frac{total shares}{total allocations + 1}

                    Note: favors larger groups more than the Hare quota

        shares : list (default=None)
            A list of populations or votes for regions or parties

        total_alloc : int (default=None)
            The number to be allocated

        alloc_threshold : float (default=None)
            A minimum percentage of the population or votes that must be met to receive an allocation

        min_alloc : int (default=None)
            A minimum number of allocations that each group must receive

        tie_break : str (default=majority)
            How a tie break is done (by majority or random, with a majority tie defaulting to random)

        majority_bonus : bool (default=False)
            Whether the largest group is automatically given 50% of the vote

    Returns
    -------
        allocations : list
            A list of allocations in the order of the provided shares
    """
    assert (
        alloc_threshold == None or min_alloc == None
    ), """Appointment methods cannot be used with both an entry threshold and a minimum seat allocation.
        Set one of alloc_threshold or min_alloc to None"""

    def get_quota(quota_style, shares, total_alloc):
        if quota_style == "Hare":
            seat_quota = 1.0 * sum(shares) / total_alloc
        elif quota_style == "Droop":
            seat_quota = int(sum(shares) / (total_alloc + 1)) + 1
        elif quota_style == "Hagenbach–Bischoff":
            seat_quota = 1.0 * sum(shares) / (total_alloc + 1)
        else:
            ValueError(
                "Invalid quota provided. Choose from Hare, Droop, or Hagenbach–Bischoff."
            )

        return seat_quota

    if alloc_threshold:
        passed_threshold = [
            True if 1.0 * s / sum(shares) > alloc_threshold else False for s in shares
        ]
        shares = [s if passed_threshold[i] == True else 0 for i, s in enumerate(shares)]

    original_remainders = None
    if min_alloc != None and min_alloc > 0:
        assert (
            min_alloc * len(shares) <= total_alloc
        ), "The sum of the minimum seats to be allocated cannot be more than the seats to be allocated."
        baseline_allocations = [min_alloc] * len(shares)

        # Save the original remainders and allocations to avoid penalization from new divisions after minimum seat allocation
        seat_quota = get_quota(
            quota_style=quota_style, shares=shares, total_alloc=total_alloc
        )
        original_remainders, original_allocations = zip(
            *[modf(1.0 * s / seat_quota) for s in shares]
        )

        # If possible, append the original allocations with the baseline such that the seats for remainders are used for the minimum allocation
        original_with_baseline = [
            a if a >= baseline_allocations[i] else baseline_allocations[i]
            for i, a in enumerate(original_allocations)
        ]
        if sum(original_with_baseline) <= total_alloc:
            original_with_baseline = [int(a) for a in original_with_baseline]

        elif sum(original_with_baseline) > total_alloc:
            # We need to just use the baseline and assign over it
            original_with_baseline = baseline_allocations

        total_alloc -= sum(original_with_baseline)

        if total_alloc == 0:
            return original_with_baseline

    seat_quota = get_quota(
        quota_style=quota_style, shares=shares, total_alloc=total_alloc
    )
    remainders, allocations = zip(*[modf(1.0 * s / seat_quota) for s in shares])

    if min_alloc != None and min_alloc > 0:
        remainders = original_remainders
        if (
            original_with_baseline != baseline_allocations
        ):  # we have extra allocations already
            allocations = [0] * len(
                shares
            )  # don't allocate any more seats based on the quota

    allocations = [int(a) for a in allocations]
    unallocated = int(total_alloc - sum(allocations))

    remainders_sorted_ids = [
        i[0] for i in sorted(enumerate(remainders), key=itemgetter(1))
    ][::-1]
    last_assigned_remainder = remainders_sorted_ids[unallocated - 1]
    allocatable = [
        i
        for i in remainders_sorted_ids
        if remainders[i] >= remainders[last_assigned_remainder]
    ]
    equal_to_last_assigned = [
        i for i in allocatable if remainders[i] == remainders[last_assigned_remainder]
    ]

    # Assign for all that are greater than the last remainder to be assigned
    for k in [i for i in allocatable if i not in equal_to_last_assigned][:unallocated]:
        allocations[k] += 1
        unallocated -= 1

    # Assign the last assignable remainder if there is no tie
    if len(equal_to_last_assigned) == 1 and unallocated == 1:
        allocations[equal_to_last_assigned[0]] += 1
        unallocated -= 1

    # Tie break conditions
    else:
        if tie_break == "majority":
            sorted_by_results = [
                i[0]
                for i in sorted(enumerate(shares), key=itemgetter(1))
                if i[0] in equal_to_last_assigned
            ][::-1]
            equal_to_highest = [
                i
                for i in sorted_by_results
                if shares[i] == shares[sorted_by_results[0]]
            ]

            if len(equal_to_highest) == 1:
                for k in range(unallocated):
                    allocations[sorted_by_results[k]] += 1

            else:
                # Defaults to random for those with equal allocation and remainder
                tie_break = "random"

        if tie_break == "random":
            shuffle(equal_to_last_assigned)
            for k in range(unallocated):
                allocations[equal_to_last_assigned[k]] += 1

        else:
            ValueError(
                f"A tie break is required for the last seat(s), and an invalid argument '{tie_break}' has been passed. Please choose from 'majority' or 'random'."
            )

    if min_alloc:
        allocations = [a + original_with_baseline[i] for i, a in enumerate(allocations)]

    if majority_bonus:
        # If a single majority group does not receive at least 50%, then they are given it, and assignment is redone for the rest
        if (
            not allocations[shares.index(max(shares))] >= int(ceil(total_alloc / 2))
            and len([s for s in shares if s == max(shares)]) == 1
        ):
            non_majority_shares = [s for s in shares if s != max(shares)]
            reduced_seats = total_alloc - int(ceil(total_alloc / 2))
            non_majority_allocations = largest_remainder(
                quota_style=quota_style,
                shares=non_majority_shares,
                total_alloc=reduced_seats,
                alloc_threshold=alloc_threshold,
                min_alloc=min_alloc,
                tie_break=tie_break,
                majority_bonus=False,
            )

            # Insert majority allocation
            non_majority_allocations[
                shares.index(max(shares)) : shares.index(max(shares))
            ] = [int(ceil(total_alloc / 2))]
            allocations = non_majority_allocations

    return allocations


def highest_averages(
    averaging_style="Jefferson",
    shares=None,
    total_alloc=None,
    alloc_threshold=None,
    min_alloc=None,
    tie_break="majority",
    majority_bonus=False,
    modifier=None,
):
    """
    Apportion seats using the Highest Averages (Jefferson, Webster, Huntington-Hill) methods.

    Parameters
    ----------
        averaging_style : str (default=Jefferson)
            The style that highest averages are computed

            Options:
                Each defines a divisor for each region or party to determines the next seat based on all previous assignments

                - Jefferson : divisor_i = share_i / (num_already_allocated_i + 1)

                    Note: an absolute majority always lead to an absolute majority in seats (favors large groups)

                - Webster : divisor_i = share_i / ((2 * num_already_allocated_i) + 1)

                    Note: generally the smallest deviation from ideal shares (favors medium groups)

                - Huntington-Hill : divisor_i = share_i / sqrt(num_already_allocated_i * (num_already_allocated_i + 1))

                    Note: assures that all regions or parties receive at least one vote (favors small groups)

        shares : list (default=None)
            A list of populations or votes for regions or parties

        total_alloc : int (default=None)
            The number to be allocated

        alloc_threshold : float (default=None)
            A minimum percentage of the population or votes that must be met to receive an allocation

        min_alloc : int (default=None)
            A minimum number of allocations that each group must receive

        tie_break : str (default=majority)
            How a tie break is done (by majority or random, with a majority tie defaulting to random)

        modifier : float (default=None)
            What to replace the divisor of the first quotient by to change the advantage of groups yet to receive an assignment
            Note: modifiers > 1 disadvantage smaller parties, and modifiers < 1 advantage them

    Returns
    -------
        allocations : list
            A list of allocations in the order of the provided shares
    """
    assert (
        alloc_threshold == None or min_alloc == None
    ), """Appointment methods cannot be used with both an entry threshold and a minimum seat allocation. Set one of 'alloc_threshold' or 'min_alloc' to None"""

    assert (
        alloc_threshold == None or averaging_style != "Huntington-Hill"
    ), """The Huntington-Hill method requires all groups to receive a seat, and thus cannot be used with a threshold. Set 'alloc_threshold' to None."""

    if averaging_style == "Huntington-Hill" and (min_alloc == None or min_alloc == 0):
        print(
            "A minimum allocation is required in the denominator of Huntington-Hill calculations."
        )
        print("A minimum allocation of 1 will be applied.")
        assert (
            len(shares) <= total_alloc
        ), "There must be at least one seat per group when using the Huntington-Hill method."
        min_alloc = 1

    if alloc_threshold:
        passed_threshold = [
            True if 1.0 * i / sum(shares) > alloc_threshold else False for i in shares
        ]
        shares = [s if passed_threshold[i] == True else 0 for i, s in enumerate(shares)]

    if min_alloc != None and min_alloc > 0:
        assert (
            min_alloc * len(shares) <= total_alloc
        ), "The sum of the minimum seats to be allocated cannot be more than the seats to be allocated."
        allocations = [min_alloc] * len(shares)
        total_alloc -= sum(allocations)

        if total_alloc == 0:
            return allocations
    else:
        allocations = [0] * len(shares)

    remaining_alloc = total_alloc
    while remaining_alloc > 0:

        if averaging_style == "Jefferson":
            if modifier:
                quotients = [
                    1.0 * s / (allocations[i] + 1)
                    if allocations[i] > 1
                    else 1.0 * s / modifier
                    for i, s in enumerate(shares)
                ]

            else:
                quotients = [
                    1.0 * s / (allocations[i] + 1) for i, s in enumerate(shares)
                ]

        elif averaging_style == "Webster":
            if modifier:
                quotients = [
                    1.0 * s / ((2 * allocations[i]) + 1)
                    if allocations[i] > 1
                    else 1.0 * s / modifier
                    for i, s in enumerate(shares)
                ]

            else:
                quotients = [
                    1.0 * s / ((2 * allocations[i]) + 1) for i, s in enumerate(shares)
                ]

        elif averaging_style == "Huntington-Hill":
            if modifier:
                quotients = [
                    1.0 * s / sqrt(allocations[i] * (allocations[i] + 1))
                    if allocations[i] > 1
                    else 1.0 * s / modifier
                    for i, s in enumerate(shares)
                ]

            else:
                quotients = [
                    1.0 * s / sqrt(allocations[i] * (allocations[i] + 1))
                    for i, s in enumerate(shares)
                ]

        else:
            print(
                f"'{averaging_style}' is not a supported highest averages method. Please choose from 'Jefferson', 'Webster', or 'Huntington-Hill'"
            )
            print(
                "Naming conventions for methods differ across regions, with United States naming conventions used in social-sci-kit."
            )
            print(
                """US assignment method name conversions:
            Jeffersion         : D'Hondt, Hagenbach-Bischoff (includes entry quota)
            Webster            : Sainte-Laguë, Major Fraction
            Huntington-Hill    : Equal Proportions"""
            )

            return

        # Find those indexes that have a maximum quotient to check if a tie break is needed
        max_quotient_indexes = [
            q[0] for q in enumerate(quotients) if q[1] == max(quotients)
        ]

        # Normal assignment to all that have the max quotient
        if len(max_quotient_indexes) <= remaining_alloc:
            for i in max_quotient_indexes:
                allocations[i] += 1

            remaining_alloc -= len(max_quotient_indexes)

        # Tie break conditions
        elif len(max_quotient_indexes) > remaining_alloc:
            if tie_break == "majority":
                sorted_by_results = [
                    i[0]
                    for i in sorted(enumerate(shares), key=itemgetter(1))
                    if i[0] in max_quotient_indexes
                ][::-1]
                equal_to_highest = [
                    i
                    for i in sorted_by_results
                    if shares[i] == shares[sorted_by_results[0]]
                ]

                if len(equal_to_highest) == 1:
                    allocations[sorted_by_results[0]] += 1
                    remaining_alloc -= 1

                else:
                    # Defaults to random for those with equal allocation and remainder
                    tie_break = "random"

            if tie_break == "random":
                shuffle(max_quotient_indexes)
                allocations[max_quotient_indexes[0]] += 1
                remaining_alloc -= 1

            else:
                ValueError(
                    f"A tie break is required for the last seat(s), and an invalid argument '{tie_break}' has been passed. Please choose from 'majority' or 'random'."
                )

    if majority_bonus:
        # If a single majority group does not receive at least 50%, then they are given it, and assignment is redone for the rest
        if (
            not allocations[shares.index(max(shares))] >= int(ceil(total_alloc / 2))
            and len([s for s in shares if s == max(shares)]) == 1
        ):
            non_majority_shares = [s for s in shares if s != max(shares)]
            reduced_seats = total_alloc - int(ceil(total_alloc / 2))
            non_majority_allocations = highest_averages(
                averaging_style=averaging_style,
                shares=non_majority_shares,
                total_alloc=reduced_seats,
                alloc_threshold=alloc_threshold,
                min_alloc=min_alloc,
                tie_break=tie_break,
                majority_bonus=False,
                modifier=modifier,
            )

            # Insert majority allocation
            non_majority_allocations[
                shares.index(max(shares)) : shares.index(max(shares))
            ] = [int(ceil(total_alloc / 2))]
            allocations = non_majority_allocations

    return allocations
