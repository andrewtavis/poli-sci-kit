"""Fixtures"""
import pytest

from poli_sci_kit.utils import normalize
from poli_sci_kit.utils import gen_list_of_lists
from poli_sci_kit.utils import gen_faction_groups
from poli_sci_kit.utils import gen_parl_points
from poli_sci_kit.utils import swap_parl_allocations

from poli_sci_kit.appointment.checks import quota_condition
from poli_sci_kit.appointment.checks import consistency_condition

from poli_sci_kit.appointment.methods import largest_remainder
from poli_sci_kit.appointment.methods import highest_average

from poli_sci_kit.appointment.metrics import ideal_share
from poli_sci_kit.appointment.metrics import alloc_to_share_ratio
from poli_sci_kit.appointment.metrics import sqr_alloc_to_share_error
from poli_sci_kit.appointment.metrics import total_alloc_to_share_error
from poli_sci_kit.appointment.metrics import rep_weight
from poli_sci_kit.appointment.metrics import sqr_rep_weight_error
from poli_sci_kit.appointment.metrics import total_rep_weight_error
from poli_sci_kit.appointment.metrics import div_index
from poli_sci_kit.appointment.metrics import effective_number_of_groups
from poli_sci_kit.appointment.metrics import dispr_index


@pytest.fixture(params=[[2560, 3315, 995, 5012]])
def votes(request):
    return request.param


@pytest.fixture(
    params=[
        [
            1918578,
            1348072,
            1023503,
            937901,
            639747,
            625263,
            621832,
            610408,
            455025,
            429811,
            405843,
            399454,
            343031,
            319922,
            297665,
            280657,
            269326,
            262508,
            171904,
            157147,
            130419,
            110358,
            97194,
            75432,
        ]
    ]
)
def long_votes_list(request):
    return request.param


@pytest.fixture(params=[[1918578, 1348072, 1023503, 937901, 639747,]])
def short_votes_list(request):
    return request.param


@pytest.fixture(params=[[1918578, 1023503, 1023503, 937901, 639747,]])
def tie_votes_list(request):
    return request.param


@pytest.fixture(params=[20])
def seats(request):
    return request.param


@pytest.fixture(params=[200])
def seats_large(request):
    return request.param


@pytest.fixture(params=list(range(4, 50)))
def seats_val(request):
    return request.param


@pytest.fixture(params=[[5, 6, 7, 8]])
def seats_list(request):
    return request.param


@pytest.fixture(params=["Hare", "Droop", "Hagenbach–Bischoff"])
def largest_remainder_styles(request):
    return request.param


@pytest.fixture(params=["Jefferson", "Webster", "Huntington-Hill"])
def highest_average_styles(request):
    return request.param


# Jefferson highest average from tie_votes_list[0] and total_alloc=seats
@pytest.fixture(params=[1918578])
def share(request):
    return request.param


# Jefferson highest averages from tie_votes_list with total_alloc=seats
@pytest.fixture(params=[[7, 4, 4, 3, 2]])
def allocations(request):
    return request.param


# Jefferson highest average from tie_votes_list[0] and total_alloc=seats
@pytest.fixture(params=[7])
def allocation(request):
    return request.param


# sum(tie_votes_list)
@pytest.fixture(params=[5543232])
def total_shares(request):
    return request.param


@pytest.fixture(
    params=["Shannon", "Renyi", "Simpson", "Gini-Simpson", "Berger-Parker", "Effective"]
)
def div_index_metrics(request):
    return request.param


@pytest.fixture(
    params=["Laakso-Taagepera", "Golosov", "Inverse-Simpson",]
)
def effective_group_metrics(request):
    return request.param


@pytest.fixture(
    params=[
        "Gallagher",
        "Loosemore–Hanby",
        "Rose",
        "Rae",
        "Sainte-Laguë",
        "d’Hondt",
        "Cox-Shugart",
    ]
)
def dispr_index_metrics(request):
    return request.param


@pytest.fixture(params=[0.5, 2])
def q(request):
    return request.param
