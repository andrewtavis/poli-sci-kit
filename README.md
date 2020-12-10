<div align="center">
  <a href="https://github.com/andrewtavis/poli-sci-kit"><img src="https://raw.githubusercontent.com/andrewtavis/poli-sci-kit/master/resources/poli-sci-kit_logo_transparent.png" width="521" height="281"></a>
</div>

--------------------------------------

[![PyPI Version](https://badge.fury.io/py/poli-sci-kit.svg)](https://pypi.org/project/poli-sci-kit/)
[![Python Version](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue.svg)](https://pypi.org/project/poli-sci-kit/)
[![GitHub](https://img.shields.io/github/license/andrewtavis/poli-sci-kit.svg)](https://github.com/andrewtavis/poli-sci-kit/blob/master/LICENSE)

### Political science appointment and analysis in Python

**Jump to:** [Appointment](#appointment) • [Examples](#examples) • [To-Do](#to-do)

**poli-sci-kit** is a Python package for politcal science appointment and election analysis. The goal is to provide a comprehensive tool for all methods needed to analyze and simulate election results.

# Installation via PyPi
```bash
pip install poli-sci-kit
```

```python
import poli_sci_kit
```

# Appointment

[appointment.methods](https://github.com/andrewtavis/poli-sci-kit/blob/master/poli_sci_kit/appointment/methods.py) includes functions to allocate parliamentary seats based on population or vote shares. Arguments to allow allocation threshholds, minimum allocations per group, tie break conditions, and other election features are also provided. Along with deriving results for visualization and reporting, these functions allow the user to analyze outcomes given systematic or situational changes. The [appointment.metrics](https://github.com/andrewtavis/poli-sci-kit/blob/master/poli_sci_kit/appointment/metrics.py) module further provides diagnostics to analyze the results of elections, apportionments, and other politcal science scenarios.

A basic example of political appointment using poli-sci-kit is:

```python
from poli_sci_kit import appointment

vote_counts = [2700, 900, 3300, 1300, 2150, 500]
seats_to_allocate = 50

# Huntington-Hill is the method used to allocate House of Represenatives seats to US states
ha_allocations = appointment.methods.highest_average(averaging_style='Huntington-Hill',
                                                     shares=vote_counts, 
                                                     total_alloc=seats_to_allocate, 
                                                     alloc_threshold=None, 
                                                     min_alloc=1, 
                                                     tie_break = 'majority', 
                                                     majority_bonus=False, 
                                                     modifier=None)

ha_allocations
# [26, 9, 37, 12, 23, 5]

# The Gallagher method is a measure of absolute difference similar to summing square residuals
disproportionality = appointment.metrics.dispr_index(shares=vote_counts, 
                                                     allocations=ha_allocations, 
                                                     mertric_type='Gallagher')

disproportionality
# 0.01002
```

Let's visualize the results with [stdviz](https://github.com/andrewtavis/stdviz):

```python
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import stdviz

# German political parties
parties = ['CDU/CSU', 'FDP', 'Greens', 'Die Linke', 'SPD', 'AfD']
party_colors = ['#000000', '#ffed00', '#64a12d', '#be3075', '#eb001f', '#009ee0']
```

```python
ax = stdviz.plot.bar(counts=ha_allocations, names=parties, 
                     faction_names=None, colors=party_colors, 
                     horizontal=False, stacked=False, 
                     label_bars=True, axis=None)

# Initialize empty handles and labels
handles, labels = stdviz.plot.legend.gen_elements()

# Add a majority line
ax.axhline(int(sum(ha_allocations)/2)+1, ls='--', color='black')
handles.insert(0, Line2D([0], [0], linestyle='--', color='black'))
labels.insert(0, 'Majority: {} seats'.format(int(sum(ha_allocations)/2)+1))

ax.legend(handles=handles, labels=labels,
          title='Bundestag: {} seats'.format(sum(ha_allocations)),
          loc='upper left', bbox_to_anchor=(0, 0.9),
          title_fontsize=20, fontsize=15, 
          frameon=True, facecolor='#FFFFFF', framealpha=1)

ax.set_ylabel('Seats', fontsize=15)
ax.set_xlabel('Party', fontsize=15)

plt.show()
```

<p align="middle">
  <img src="https://github.com/andrewtavis/poli-sci-kit/blob/master/resources/gh_images/bar.png" width="600" />
</p>


```python
ax = stdviz.plot.parliament(seat_counts=ha_allocations, 
                            names=parties, colors=party_colors, 
                            style='semicircle', num_rows=4, marker_size=175, 
                            speaker=False, df_seat_lctns=None, axis=ax2)

plt.show()
```

<p align="middle">
  <img src="https://github.com/andrewtavis/poli-sci-kit/blob/master/resources/gh_images/semicircle_parliament.png" width="600" />
</p>

# Examples

Examples in poli-sci-kit use publically available Wikidata statistics sourced via the Python package [wikirepo](https://github.com/andrewtavis/wikirepo). Current examples include:

- [US HoR](https://github.com/andrewtavis/poli-sci-kit/blob/master/examples/us_house_of_rep.ipynb)
    - Allocates seats to a version of the US House of Representatives that includes all US territories and Washington DC given census data, with this further being used to derive relative vote strengths of state citizens in the US presidential election

- [Global Parliament](https://github.com/andrewtavis/poli-sci-kit/blob/master/examples/global_parliament.ipynb)
    - Analyzes the allocation of seats in a hypothetical global parliament given the prevalance of certain counties and organizations, the distribution of seats based on Freedom House indexes, and disproportionality metrics

# To-Do

- Checks for [appointment.methods] implementations
- Deriving further needed arguments to assure that all current and historic appointment systems can be simulated using poli-sci-kit
- Potentially indexing preset versions of [appointment.methods](https://github.com/andrewtavis/poli-sci-kit/blob/master/poli_sci_kit/appointment/methods.py) that coincide with the systems used by governments around the world
    - This would allow quick comparisons of actual systems with variations
- Creating, improving and sharing [examples](https://github.com/andrewtavis/poli-sci-kit/tree/master/examples)
- Testing for poli-sci-kit

# References
<details><summary><strong>Full list of references<strong></summary>
<p>

- https://github.com/crflynn/voting
- https://blogs.reading.ac.uk/readingpolitics/2015/06/29/electoral-disproportionality-what-is-it-and-how-should-we-measure-it/
- Balinski, M. L., and Young, H. P. (1982). Fair Representation: Meeting the Ideal of One Man, One Vote. New Haven, London: Yale University Press.
- Karpov, A. (2008). "Measurement of disproportionality in proportional representation systems". Mathematical and Computer Modelling, Vol. 48, pp. 1421-1438. URL: https://www.sciencedirect.com/science/article/pii/S0895717708001933.
- Kohler, U., and Zeh, J. (2012). “Apportionment methods”. The Stata Journal, Vol. 12, No. 3, pp. 375–392. URL: https://journals.sagepub.com/doi/pdf/10.1177/1536867X1201200303.
- Taagepera, R., and Grofman, B. (2003). "Mapping the Indices of Seats-Votes Disproportionality and Inter-Election Volatility". Party Politics, Vol. 9, No. 6, pp. 659–677. URL: https://escholarship.org/content/qt0m9912ff/qt0m9912ff.pdf.

</p>
</details>