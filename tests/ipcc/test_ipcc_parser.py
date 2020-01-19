#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.

Test the methods for parsing data from `forest_puller.ipcc`

Typically you would run this file from a command line like this:

     ipython3 -i -- ~/deploy/forest_puller/tests/ipcc/test_ipcc_parser.py
"""

# Built-in modules #
import os, inspect, math

# Third party modules #
import pandas

# Get current directory #
file_name = os.path.abspath((inspect.stack()[0])[1])
this_dir  = os.path.dirname(os.path.abspath(file_name)) + '/'

# Expected data #
manually = pandas.read_csv(this_dir + "austria_1990.csv")
manually = manually.fillna('')
manually = manually.set_index(['land_use', 'subdivision'])

###############################################################################
def test_parse():
    """
    Try to extract some IPCC CRF data for e.g. Austria in 1990.
    """
    # Import #
    from forest_puller.ipcc.country import countries
    # Get the country Austria #
    austria = countries['AT']
    # Get the year 1990 #
    at_1990 = austria.years[1990]
    # Get one value #
    provided = at_1990.indexed.loc['total_forest', '']['area']
    # Get the same value #
    expected = manually.loc['total_forest', '']['area']
    # Test #
    assert math.isclose(expected, provided)

###############################################################################
if __name__ == '__main__':
    test_parse()