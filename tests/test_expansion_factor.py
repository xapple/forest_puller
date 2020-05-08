#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

This test suite can be run with pytest.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #
from forest_puller.conversion import expansion_factor

# First party modules #

# Third party modules #
import pandas
from pandas.testing import assert_frame_equal

###############################################################################
def test_distribute_unknown_forest_type():
    """
    Test the function that distribute the unknown or mixed forest type to
    the given categories, for example coniferous and broad leaves.
    """
    # Initialize input values #
    df = pandas.DataFrame({'area':        [10, 20, 30],
                           'forest_type': ['con', 'other', 'broad']})
    # Expected output #
    df_expected = pandas.DataFrame({'area':        [20, 40],
                                    'forest_type': ['con', 'broad']})
    # Call the function #
    remaining_forest_types = ['con', 'broad']
    df_computed = expansion_factor.split_unknown_forest_type(df, remaining_forest_types)
    # Test #
    assert_frame_equal(df_computed, df_expected)

###############################################################################
def test_compute_bcef():
    """
    Test the function that aggregates and compute the
    biomass conversion and expansion factors
    """
    pass

