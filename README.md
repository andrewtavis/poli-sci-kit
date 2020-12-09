<div align="center">
  <a href="https://github.com/andrewtavis/poli-sci-kit"><img src="https://raw.githubusercontent.com/andrewtavis/poli-sci-kit/master/resources/poli-sci-kit_logo_transparent.png" width="521" height="281"></a>
</div>

--------------------------------------

[![PyPI Version](https://badge.fury.io/py/poli-sci-kit.svg)](https://pypi.org/project/poli-sci-kit/)
[![Python Version](https://img.shields.io/badge/python-3.5%20%7C%203.6%20%7C%203.7-blue.svg)](https://pypi.org/project/poli-sci-kit/)
[![GitHub](https://img.shields.io/github/license/andrewtavis/poli-sci-kit.svg)](https://github.com/andrewtavis/poli-sci-kit/blob/master/LICENSE)

### Political science appointment and analysis in Python

**Jump to:** [Appointment](#appointment) • [To-Do](#to-do)

**poli-sci-kit** is a Python package for politcal science appointment and election analysis.

# Installation via PyPi
```bash
pip install poli-sci-kit
```

```python
import poli_sci_kit
```

# Appointment

[appointment/methods](https://github.com/andrewtavis/poli-sci-kit/blob/master/poli_sci_kit/appointment/methods.py) includes functions to allocate parliamentary seats based on population or vote shares. Along with deriving results for visualization and reporting, these functions allow the user to analyze outcomes given systematic or situational changes. The [appointment/metrics](https://github.com/andrewtavis/poli-sci-kit/blob/master/poli_sci_kit/appointment/metrics.py) module further provides diagnostics to analyze the results of elections, apportionments, and other politcal science scenarios.

An example of political appointment using poli-sci-kit is:

```python
from poli_sci_kit import appointment

vote_counts = [250, 150, 100, 85, 75, 25]
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
# [18, 11, 7, 6, 6, 2]

# The Gallagher method is a measure of absolute difference similar to summing square residuals
disproportionality = appointment.metrics.dispr_index(shares=vote_counts, 
                                                     allocations=ha_allocations, 
                                                     mertric_type='Gallagher')

disproportionality
# 0.01002
```

# To-Do

- Checks for the appointment method implementations
- Creating and improving [examples](https://github.com/andrewtavis/poli-sci-kit/tree/master/examples)

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