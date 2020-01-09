#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.

Test the methods for parsing data from `forest_puller.ipcc`
"""

# Built-in modules #

# Third party modules #
import pandas

# Expected data #
crf_at_test = pandas.read_csv("ipcc_crf_austria_2017.csv")

###############################################################################
def test_parse():
    """
    Try to extract some IPCC CRF data for e.g. Austria.
    """
    # Import #
    from forest_puller.ipcc.crf import dataset as crf
    # Define one particular value #
    index  = ['country', 'year', 'land_use',              'subdivision']
    values = ['AT',      '2017', 'forest_land_remaining', 'coniferous']
    # Get one value #
    provided = crf.df.set_index(index).loc[values, 'stock_change'][0]
    # Get the same value #
    expected = crf_at_test.df.set_index(index).loc[values, 'stock_change'][0]
    # Test #
    assert expected == provided
