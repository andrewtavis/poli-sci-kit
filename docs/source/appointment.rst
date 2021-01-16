appointment
=============

The :py:mod:`appointment` module allows users to apportion parliamentary seats given vote shares or populations, as well as analyze the results of these allocations.

methods
^^^^^^^
:py:mod:`appointment.methods` includes functions to allocate parliamentary seats based on population or vote shares. Arguments to allow allocation thresholds, minimum allocations per group, tie break conditions, and other election features are also provided. Along with deriving results for visualization and reporting, these functions allow the user to analyze outcomes given systematic or situational changes.

* :py:func:`poli_sci_kit.appointment.methods.largest_remainder`
* :py:func:`poli_sci_kit.appointment.methods.highest_average`

.. autofunction:: poli_sci_kit.appointment.methods.largest_remainder
.. autofunction:: poli_sci_kit.appointment.methods.highest_average

metrics
^^^^^^^
:py:mod:`appointment.metrics` further provides diagnostics to analyze the results of elections, apportionments, and other political science scenarios.

* :py:func:`poli_sci_kit.appointment.metrics.ideal_share`
* :py:func:`poli_sci_kit.appointment.metrics.alloc_to_share_ratio`
* :py:func:`poli_sci_kit.appointment.metrics.sqr_alloc_to_share_error`
* :py:func:`poli_sci_kit.appointment.metrics.total_alloc_to_share_error`
* :py:func:`poli_sci_kit.appointment.metrics.rep_weight`
* :py:func:`poli_sci_kit.appointment.metrics.sqr_rep_weight_error`
* :py:func:`poli_sci_kit.appointment.metrics.total_rep_weight_error`
* :py:func:`poli_sci_kit.appointment.metrics.div_index`
* :py:func:`poli_sci_kit.appointment.metrics.effective_number_of_groups`
* :py:func:`poli_sci_kit.appointment.metrics.dispr_index`

.. autofunction:: poli_sci_kit.appointment.metrics.ideal_share
.. autofunction:: poli_sci_kit.appointment.metrics.alloc_to_share_ratio
.. autofunction:: poli_sci_kit.appointment.metrics.sqr_alloc_to_share_error
.. autofunction:: poli_sci_kit.appointment.metrics.total_alloc_to_share_error
.. autofunction:: poli_sci_kit.appointment.metrics.rep_weight
.. autofunction:: poli_sci_kit.appointment.metrics.sqr_rep_weight_error
.. autofunction:: poli_sci_kit.appointment.metrics.total_rep_weight_error
.. autofunction:: poli_sci_kit.appointment.metrics.div_index
.. autofunction:: poli_sci_kit.appointment.metrics.effective_number_of_groups
.. autofunction:: poli_sci_kit.appointment.metrics.dispr_index


checks
^^^^^^
:py:mod:`appointment.checks` contains functions to check the conditional efficacy of an apportionment.

* :py:func:`poli_sci_kit.appointment.checks.quota_condition`
* :py:func:`poli_sci_kit.appointment.checks.consistency_condition`

.. autofunction:: poli_sci_kit.appointment.checks.quota_condition
.. autofunction:: poli_sci_kit.appointment.checks.consistency_condition
