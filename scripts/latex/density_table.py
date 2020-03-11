#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
Script to check what years are available for which country in `forest_puller.ipcc`

Typically you would run this file from a command line like this:

     ipython3 -i
"""

import pandas
from forest_puller.soef.composition import composition_data
avg_densities = composition_data.avg_densities
avg_densities['year'] = avg_densities['year'].apply(pandas.to_numeric, errors="coerce", downcast='integer')
avg_densities_wide = avg_densities.pivot(index = 'country', columns='year',
                    values=['avg_density', 'frac_missing'])
tex = avg_densities_wide.to_latex(float_format="%.3f", na_rep='',
                            label = 'Weighted average density by country')
file_name = density_table.tex
print(tex , file='')
