#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""@author: Paul Rougieux and Lucas Sinclair

Execute the test suite from bash with py.test as follows:

    cd ~/repos/forest_puller/forest_puller/soef
    pytest
    # enter debugger on failure
    pytest --pdb

"""

# Third party modules
import pandas
from pandas.testing import assert_frame_equal
# Project modules
import expansion_factor


def test_split_unknown_forest_type():
    """
    Test the function that splits the unknown or mixed forest type to
    the given categories, for example coniferous and broad leaves.
    """
    # Initialize input values
    remaining_forest_types = ['con', 'broad']
    df = pandas.DataFrame({'area': [10,20,30],
                           'forest_type':['con','other','broad']})
    # Expected output
    df_expected = pandas.DataFrame({'area': [20,40],
                                    'forest_type':['con','broad']})
    # Call the function
    df_con_broad = expansion_factor.split_unknown_forest_type(df, remaining_forest_types)
    # Test
    assert_frame_equal(df_con_broad, df_expected)


def test_compute_bcef():
    """Test the function that aggregates and compute the
    biomass conversion and expansion factors
    """


