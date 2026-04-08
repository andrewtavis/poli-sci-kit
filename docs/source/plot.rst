plot
====

The :py:mod:`plot` module provides users with Python only implementations of common electoral plots.

A novel addition to social science analysis is the `disproportionality bar plot <https://github.com/andrewtavis/poli-sci-kit/blob/main/poli_sci_kit/plot/disproportionality_bar_plot.py>`_, which graphically depicts the disproportionality between expected and realized results. Bar widths are the proportion of shares (ex: votes received), and heights are the difference or relative difference between shares and allocations (ex: parliament seats received).

**Functions**

* :py:func:`poli_sci_kit.plot.disproportionality_bar_plot`
* :py:func:`poli_sci_kit.plot.parliament_plot`
* :py:func:`poli_sci_kit.utils.gen_parliament_plot_points`
* :py:func:`poli_sci_kit.utils.swap_parl_allocations`

.. autofunction:: poli_sci_kit.plot.disproportionality_bar_plot

poli_sci_kit also provides Python only implementations of both rectangular and semicircle `parliament plots <https://github.com/andrewtavis/poli-sci-kit/blob/main/poli_sci_kit/plot/parliament_plot.py>`_:

.. autofunction:: poli_sci_kit.plot.parliament_plot

The parliament plot function is built on top of scatter plots that are derived in the package's `utils <https://github.com/andrewtavis/poli-sci-kit/blob/main/poli_sci_kit/utils.py>`_ module:

.. autofunction:: poli_sci_kit.utils.gen_parliament_plot_points

A final function to swap poorly allocated seats is also provided in `utils <https://github.com/andrewtavis/poli-sci-kit/blob/main/poli_sci_kit/utils.py>`_:

.. autofunction:: poli_sci_kit.utils.swap_parl_allocations
