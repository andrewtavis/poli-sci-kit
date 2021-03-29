"""
Appointment Metrics
-------------------

Functions to analyze the results of appointments, allocations and other social science scenarios.

Based on
    Kohler, U., and Zeh, J. (2012). “Apportionment methods”.
    The Stata Journal, Vol. 12, No. 3, pp. 375–392.
    URL: https://journals.sagepub.com/doi/pdf/10.1177/1536867X1201200303

    Karpov, A. (2008). "Measurement of disproportionality in proportional representation systems".
    Mathematical and Computer Modelling, Vol. 48, 1421-1438.
    URL: https://www.sciencedirect.com/science/article/pii/S0895717708001933

    Taagepera, R., Grofman, B. (2003). "Mapping the Indices of Seats-Votes Disproportionality and Inter-Election Volatility". Party Politics, Vol. 9, No. 6, pp. 659–677.
    URL: https://escholarship.org/content/qt0m9912ff/qt0m9912ff.pdf.

Contents:
    ideal_share,
    alloc_to_share_ratio,
    sqr_alloc_to_share_error,
    total_alloc_to_share_error,
    rep_weight,
    sqr_rep_weight_error,
    total_rep_weight_error,
    div_index,
    effective_number_of_groups
    dispr_index
"""

from math import exp, log, sqrt

from poli_sci_kit.utils import normalize
from scipy.stats import linregress


def ideal_share(share, total_shares, total_alloc):
    """
    Calculate the ideal share of proportions and totals.

    Parameters
    ----------
        share : int
            The proportion to be checked

        total_shares : int
            The total amount of shares

        total_alloc : int
            The number of allocations to provide

    Returns
    -------
        ideal : float
            The ideal share that would be allocated
    """
    return 1.0 * share / total_shares * total_alloc


def alloc_to_share_ratio(share, total_shares, allocation, total_alloc):
    """
    Calculate the allocation to share (advantage) ratio given to a region or group.

    Parameters
    ----------
        share : int
            The proportion to be checked

        total_shares : int
            The total amount of shares

        allocation : int
            The share of allocations given to the region or group

        total_alloc : int
            The number of allocations to provide

    Returns
    -------
        asr : float
            The ratio of the allocations the region or group received to their proportion of the original shares
    """
    return 1.0 * (allocation / total_alloc) / (share / total_shares)


def sqr_alloc_to_share_error(share, total_shares, allocation, total_alloc):
    """
    Calculate the squared error of an assignment's allocation to share ratio for a population or group.

    Parameters
    ----------
        share : int
            The proportion to be checked

        total_shares : int
            The total amount of shares

        allocation : int
            The share of allocations given to the region or group

        total_alloc : int
            The number of allocations to provide

    Returns
    -------
        sqr_asr_err : float
            The squared of the error of the allocation to share ratio
    """
    asr = alloc_to_share_ratio(
        share=share,
        total_shares=total_shares,
        allocation=allocation,
        total_alloc=total_alloc,
    )

    return (asr - 1) ** 2


def total_alloc_to_share_error(shares, allocations, proportional=True):
    """
    Calculate the total squared error of an assignment's allocation to share ratio.

    Parameters
    ----------
        shares : list
            The proportion of the original shares for the regions or groups

        allocations : list
            The share of allocations given to the regions or groups

        proportional : bool (default=False)
            Whether the assignment's error is calculated as proportional to the region or group shares

    Returns
    -------
        total_asr_err : float
            The summation of the allocation to share ratio error for all populations or groups
    """
    assert len(shares) == len(
        allocations
    ), "The total different shares of a population or vote must equal that of the allocations."

    sum_share = sum(shares)
    sum_allocations = sum(allocations)

    sqr_asr_errors = [
        sqr_alloc_to_share_error(
            share=s,
            total_shares=sum_share,
            allocation=allocations[i],
            total_alloc=sum_allocations,
        )
        for i, s in enumerate(shares)
    ]

    if proportional:
        proportional_errors = [
            s / sum_share * sqr_asr_errors[i] for i, s in enumerate(shares)
        ]
        return sum(proportional_errors)

    else:
        return sum(sqr_asr_errors)


def rep_weight(share, allocation):
    """
    Calculate the representative weight of an allocation to a region or group.

    Parameters
    ----------
        share : int
            The proportion to be checked

        allocation : int
            The allocation provided

    Returns
    -------
        rep_weight : float
            The number of shares per allocation
    """
    return share / allocation


def sqr_rep_weight_error(share, total_shares, allocation, total_alloc):
    """
    Calculate the squared error of an assignment's representative weight for a population or group.

    Parameters
    ----------
        share : int
            The proportion to be checked

        total_shares : int
            The total amount of shares

        allocation : int
            The share of allocations given to the region or group

        total_alloc : int
            The number of allocations to provide

    Returns
    -------
        sqr_rw_err : float
            The squared of the error of the allocation to share ratio
    """
    rw = rep_weight(share=share, allocation=allocation)

    return (rw - total_shares / total_alloc) ** 2


def total_rep_weight_error(shares, allocations, proportional=True):
    """
    Calculate the total squared error of an assignment's representative weight error.

    Parameters
    ----------
        shares : list
            The proportion of the original shares for the regions or groups

        allocations : list
            The share of allocations given to the regions or groups

        proportional : bool (default=False)
            Whether the assignment's error is calculated as proportional to the region or group shares

    Returns
    -------
        total_rw_err : float
            The summation of the representative weight error for all populations or groups
    """
    assert len(shares) == len(
        allocations
    ), "The total different shares of a population or vote must equal that of the allocations."

    sum_share = sum(shares)
    sum_allocations = sum(allocations)

    sqr_rw_errors = [
        sqr_rep_weight_error(
            share=s,
            total_shares=sum_share,
            allocation=allocations[i],
            total_alloc=sum_allocations,
        )
        for i, s in enumerate(shares)
    ]

    if proportional:
        proportional_errors = [
            s / sum_share * sqr_rw_errors[i] for i, s in enumerate(shares)
        ]
        return sum(proportional_errors)

    else:
        return sum(sqr_rw_errors)


def div_index(shares, q=None, metric_type="Shannon"):
    """
    Calculates the diversity index: the uncertainty associated with predicting further elements within the vote or population distributions.

    Parameters
    ----------
        shares : list
            The proportion of the original shares for the regions or groups

        q : float
            The order of diversity (a weight value for the sensitivity of the diversity value to rare vs. abundant)

        metric_type : str (default=Shannon)
            The type of formula to use

            Options:
                The available measures of diversity

                - Shannon : approaches zero (one) when shares are concentrated (dispersed), uncertainty (certainty) of the next element goes to zero

                - Renyi : generalization of the Shannon diversity

                - Simpson : probability that two entities taken at random from the dataset of interest represent the same type (assumes replacement)

                - Gini-Simpson : opposite of the Simpson diversity, the probability that two entities are from different types

                - Berger-Parker : proportional abundance of the most abundant type

                - Effective : number of equally abundant types needed for the average proportional abundance of types to equal that of the dataset

    Returns
    -------
        index : float
            The measure of diversity given the share distribution
    """
    norm_shares = normalize(vals=shares)

    if metric_type == "Shannon":
        index = -1 * sum(share * log(share) for share in norm_shares)

    elif metric_type == "Renyi":
        assert (
            q
        ), "The order of diversity 'q' argument must be used with Renyi diversity calculations"
        index = 1.0 / (1 - q) * log(sum([share ** q for share in norm_shares]))

    elif metric_type == "Simpson":
        index = sum(share ** 2 for share in norm_shares)

    elif metric_type == "Gini-Simpson":
        index = 1 - sum(share ** 2 for share in norm_shares)

    elif metric_type == "Berger-Parker":
        index = max(norm_shares)

    elif metric_type == "Effective":
        assert (
            q
        ), "The order of diversity 'q' argument must be used with Effective diversity calculations"
        if q == 1:
            index = exp(div_index(shares=shares, q=None, metric_type="Shannon"))
        else:
            index = sum(share ** q for share in norm_shares) ** (1.0 / (1 - q))

    else:
        ValueError(
            f"{metric_type} is not a valid value for the 'metric_type' argument."
        )

    return index


def effective_number_of_groups(shares, metric_type="Laakso-Taagepera"):
    """
    Calculates the effective number of groups given vote or population distributions.

    Parameters
    ----------
        shares : list
            The proportion of the original shares for the regions or groups

        metric_type : str (default=Laakso-Taagepera, option=Golosov, Inverse-Simpson)
            The type of formula to use

    Returns
    -------
        num_groups : float
            A float representing the efficient number of groups given the share distributions
    """
    norm_shares = normalize(vals=shares)

    if metric_type == "Laakso-Taagepera":
        return 1.0 / sum(share ** 2 for share in norm_shares)

    elif metric_type == "Golosov":
        max_share = max(shares)
        return sum(
            share / (share + max_share ** 2 - share ** 2) for share in norm_shares
        )

    elif metric_type == "Inverse-Simpson":
        return 1.0 / div_index(shares=shares, metric_type="Shannon")


def dispr_index(shares, allocations, metric_type="Gallagher"):
    """
    Measures of the degree to which the actual allocations deviates from the shares, with larger indexes implying greater disproportionality.

    Parameters
    ----------
        shares : list
            The proportion of the original shares for the regions or groups

        allocations : list
            The share of allocations given to the regions or groups

        metric_type : str (default=Gallagher)
            The type of formula to use

            Options:
                The available measures of disproportionality

                - Gallagher : measure of absolute difference in percent of allocations received to true proportion
                    Note 1: accounts for magnitudes of the individual shifts

                    Note 2: deals with the magnitudes of the disproportionality, not the percentage differences from ideality

                    Note 3: a general form with k instead of the square root, 1/2 and second power is not monotone to k, as is thus not included

                - Loosemore–Hanby : the total excess of allocated shares of overrepresented groups over the exact quota and the total shortage accruing to other groups
                    Note 1: is not consistent (it fails Dalton's principle of transfers, where transfering shares may lead to adverse effects on allocations)

                    Note 2: does not account for the magnitude of individual disproportionality (that few large shifts should potentially be worse than many small)

                - Rose : 100 minus the Loosemore–Hanby index, so in this case larger numbers are better (suffers from similar issues)

                - Rae : measure of the average absolute difference in percent of allocations received to true proportion
                    Note 1: includes the number of groups in the calculation, and thus is effected if there are many small groups

                    Note 2: don't use to compare appointments across situations with different numbers of groups

                - Sainte-Laguë (chi-squared) : measure of relative difference in percent of allocations received to true proportion
                    Note 1: has no upper limit

                    Note 2: downplays the disproportionality that effects larger groups

                    Note 3: sensitive to if there are is large portion of the shares that are 'other' and don't receive votes

                - d’Hondt : measure of relative difference in percent of allocations received to true proportion
                    Note: does not account for the magnitude of individual disproportionality (that few large shifts should be worse than many small)

                - Cox-Shugart : the slope of the line of best fit between the shares and allocations
                    Note 1: main advantage is directly showing whether larger or smaller groups are benefitting (>1 or <1 respectively)

                    Note 2: this index can be negative, and if it is, that implies a negative shares-allocations ratio

                Note: the Gini index as a measure of disproportionality is not included, as in many cases smaller groups have a greater allocation proportion

    Returns
    -------
        index : float
            A measure of disproportionality between allocations and original shares
    """
    assert len(shares) == len(
        allocations
    ), "The number of different shares must equal the number of different allocations."

    available_metrics = [
        "Gallagher",
        "Loosemore–Hanby",
        "Rose",
        "Rae",
        "Sainte-Laguë",
        "d’Hondt",
        "Cox-Shugart",
        "Gini",
    ]
    assert metric_type in available_metrics, (
        f"{metric_type} is not a valid value for the 'metric_type' argument. Please choose from the following options: "
        + ", ".join(available_metrics)
        + "."
    )

    norm_shares = normalize(vals=shares)
    norm_allocations = normalize(vals=allocations)

    if metric_type == "Gallagher":
        index = sqrt(1.0 / 2) * sqrt(
            sum(
                (share - allocation) ** 2
                for share, allocation in zip(norm_shares, norm_allocations)
            )
        )

    elif metric_type == "Loosemore–Hanby":
        index = (
            1.0
            / 2
            * sum(
                [
                    abs(share - allocation)
                    for share, allocation in zip(norm_shares, norm_allocations)
                ]
            )
        )

    elif metric_type == "Rose":
        index = 100 - dispr_index(
            shares=shares, allocations=allocations, metric_type="Loosemore–Hanby"
        )

    elif metric_type == "Rae":
        index = (
            1.0
            / len(norm_shares)
            * sum(
                abs(share - allocation)
                for share, allocation in zip(norm_shares, norm_allocations)
            )
        )

    elif metric_type in ["Sainte-Laguë", "Sainte-Lague"]:
        index = sum(
            1.0 / share * (share - allocation) ** 2
            for share, allocation in zip(norm_shares, norm_allocations)
        )

    elif metric_type in ["dHondt", "dhondt", "d’Hondt", "d’hondt"]:
        index = max(
            1.0 * allocation / share
            for share, allocation in zip(norm_shares, norm_allocations)
        )

    elif metric_type == "Cox-Shugart":
        index = linregress(shares, allocations)[0]

    return index
