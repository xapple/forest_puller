#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.

Test methods parsing data from the IPCC Common Reporting Format (CRF) table 4.
"""

# Built-in modules #

# Third party modules #
import pandas

# Expected data #
crf_test = pandas.read_csv("ipcc_crf_austria_2017.csv")

###############################################################################
def test_parse():
    """
    Test IPCC CRF data for Austria.
    """
    # Import #
    from forest_puller.ipcc.crf import dataset as crf
    # Check one value #
    index  = ['country', 'year', 'land_use',              'subdivision']
    values = ['AT',      '2017', 'forest_land_remaining', 'coniferous']
    expected = crf_test.df.set_index(index).loc[values, 'stock_change'][0]
    provided = crf.df.set_index(index).loc[values, 'stock_change'][0]
    assert expected == provided
