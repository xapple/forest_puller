#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.

Test methods parsing data from the IPCC Common Reporting Format (CRF) table 4.
"""

# Built-in modules #

# First party modules #
from plumbing.dataframes import string_to_df

# Expected data #
crf = string_to_df("""country | year | land_use    | subdivision | area | gain | loss | stock_change |
                              |      |             |             |      |      |      |              |
                           AT | 2017 | forest_land | coniferous  | 0.7  | 0.3  | 0.3  | 0.3          |
                           AT | 2017 | forest_land | deciduous   | 0    | 1    | 0.3  | 0.3          |""")

###############################################################################
def test_parse():
    """
    Load IPCC CRF data for Austria.
    """
    # Import #
    from forest_puller.ipcc import dataset as ipcc
    # Check one value #
    index  = ['country', 'year', 'land_use',    'subdivision']
    values = ['AT',      '2017', 'forest_land', 'coniferous']
    assert ipcc.set_index(index).loc[values, 'stock_change'][0] == 0.3
