.. image:: https://raw.githubusercontent.com/andrewtavis/poli-sci-kit/main/.github/resources/logo/poli-sci-kit_logo_transparent.png
    :width: 463
    :height: 251
    :align: center
    :target: https://github.com/andrewtavis/poli-sci-kit

|rtd| |ci_static_analysis| |ci_pytest| |pyversions| |pypi| |pypistatus| |license| |coc| |colab|

.. |rtd| image:: https://img.shields.io/readthedocs/poli-sci-kit.svg?logo=read-the-docs
    :target: http://poli-sci-kit.readthedocs.io/en/latest/

.. |ci_static_analysis| image:: https://img.shields.io/github/actions/workflow/status/andrewtavis/poli-sci-kit/.github/workflows/ci_static_analysis.yaml?branch=main&label=ci&logo=ruff
    :target: https://github.com/andrewtavis/poli-sci-kit/actions/workflows/ci_static_analysis.yaml

.. |ci_pytest| image:: https://img.shields.io/github/actions/workflow/status/andrewtavis/poli-sci-kit/.github/workflows/ci_pytest.yaml?branch=main&label=build&logo=pytest
    :target: https://github.com/andrewtavis/poli-sci-kit/actions/workflows/ci_pytest.yaml

.. |pyversions| image:: https://img.shields.io/pypi/pyversions/poli-sci-kit.svg?logo=python&logoColor=FFD43B&color=306998
    :target: https://pypi.org/project/poli-sci-kit/

.. |pypi| image:: https://img.shields.io/pypi/v/poli-sci-kit.svg?color=4B8BBE
    :target: https://pypi.org/project/poli-sci-kit/

.. |pypistatus| image:: https://img.shields.io/pypi/status/poli-sci-kit.svg
    :target: https://pypi.org/project/poli-sci-kit/

.. |license| image:: https://img.shields.io/github/license/andrewtavis/poli-sci-kit.svg
    :target: https://github.com/andrewtavis/poli-sci-kit/blob/main/LICENSE.txt

.. |coc| image:: https://img.shields.io/badge/coc-Contributor%20Covenant-ff69b4.svg
    :target: https://github.com/andrewtavis/poli-sci-kit/blob/main/.github/CODE_OF_CONDUCT.md

.. |colab| image:: https://img.shields.io/badge/%20-Open%20in%20Colab-097ABB.svg?logo=google-colab&color=097ABB&labelColor=525252
    :target: https://colab.research.google.com/github/andrewtavis/poli-sci-kit

Political elections, appointment, analysis and visualization in Python

Installation
------------

``poli-sci-kit`` is available for installation via `uv <https://docs.astral.sh/uv/>`_ (recommended) or `pip <https://pypi.org/project/poli-sci-kit/>`_.

.. code-block:: shell

    # Using uv (recommended - fast, Rust-based installer):
    uv pip install poli-sci-kit

    # Or using pip:
    pip install poli-sci-kit

.. code-block:: shell

    # For a development build of the package:
    git clone https://github.com/andrewtavis/poli-sci-kit.git
    cd poli-sci-kit

    # With uv (recommended):
    uv sync --all-extras  # install all dependencies
    source .venv/bin/activate  # activate venv (macOS/Linux)
    # .venv\Scripts\activate  # activate venv (Windows)

    # Or with pip:
    python -m venv .venv  # create virtual environment
    source .venv/bin/activate  # activate venv (macOS/Linux)
    # .venv\Scripts\activate  # activate venv (Windows)
    pip install -e .

.. code-block:: python

    import poli_sci_kit

.. toctree::
    :maxdepth: 2
    :caption: Contents:

    appointment/index
    plot
    utils
    notes

Project Indices
===============

* :ref:`genindex`
