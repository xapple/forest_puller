#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class like this:

    >>> from forest_puller.conversion.tree_species_info import df as species_info
    >>> print(species_info)
"""

# Built-in modules #

# Internal modules #
from forest_puller import module_dir

# First party modules #

# Third party modules #
import pandas

###############################################################################
def load_species_info():
    """
    Parse the hard-coded table genus and species to density.
    These values come from a publication:

        Chapter 4: Forest Land 2006 IPCC Guidelines for National Greenhouse Gas Inventories
        Table 4.14 Basic Wood Density (d) Of Selected Temperate And Boreal Tree Taxa
        https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_04_Ch4_Forest_Land.pdf
        See page 71.

    The density in [tons / m³] more precisely [oven-dry tonnes of C per moist m³].
    We convert it to [kg / m³] here.
    Note: we do not know if they measure the volume over or under bark.
    """
    # Constants #
    result = module_dir + 'extra_data/tree_species_info.csv'
    result = pandas.read_csv(str(result))
    # Strip white space #
    for col in ['species', 'genus']:
        result[col] = result[col].str.strip()
    # Fill missing values #
    for col in ['species', 'genus']:
        result[col] = result[col].fillna('missing')
    # We want kilograms, not tons #
    result['density'] *= 1000
    # Transform the plot colors form strings to tuples #
    to_color = lambda s: tuple(map(float, s.split(' ')))
    result['plot_color'] = result['plot_color'].apply(to_color)
    # Return #
    return result

###############################################################################
# Create a dataframe #
df = load_species_info()

# Make a list of conifers and broadleaved genera #
genera   = df.groupby('genus').first().reset_index()
conifers = genera.query('kind=="conifer"')['genus'].tolist()
broads   = genera.query('kind=="broad"')['genus'].tolist()
