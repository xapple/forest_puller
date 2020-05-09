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
from forest_puller.conversion import expand_biomass
from forest_puller.conversion.load_expansion_factor import df as bcef

# First party modules #

# Third party modules #
import pandas
from pandas.testing import assert_frame_equal
from pandas.testing import assert_series_equal

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
    df_computed = expand_biomass.distribute_unknown_forest_type(df, remaining_forest_types)
    # Test #
    assert_frame_equal(df_computed, df_expected)

###############################################################################
def test_choose_bcef():
    """
    Test the function that aggregates and compute the
    biomass conversion and expansion factors
    """
    # Input arguments
    df = pandas.DataFrame({'climatic_zone': ['Temperate', 'Boreal','Mediterranean']
                           'forest_type': ['broad', 'con', 'broad'],
                           'area':        [1, 2, 1],
                           'stock':      [50, 80, 50]}) 
    # Expected bcef series
    # Note: the result data frame might contain more columns than this one, 
    # test should pass as long as it contains these series
    expected = pandas.DataFrame({'bcefi':[0.900, 0.470, 0.550],
                                 'bcefr':[1.55, 0.73, 0.89],
                                 'bcefs':[1.40, 0.66, 0.80]})
    # Call the function
    result = expand_biomass.choose_bcef(df)
    # Test 
    assert_series_equal(result['bcefi'], expected['bcefi']) 
    assert_series_equal(result['bcefr'], expected['bcefr']) 
    assert_series_equal(result['bcefs'], expected['bcefs']) 


def test_convert_merch_vol_to_abg_mass():
    """Test the function that converts merchantable biomass volume (m3 of trunk) 
       to above ground biomass weight (tons of dry biomass of trunk plus branches)"""
    # Input arguments
    df = pandas.DataFrame({'climatic_zone': ['Temperate', 'Boreal','Mediterranean']
                           'forest_type': ['broad', 'con', 'broad'],
                           'area':        [1, 2, 1],
                           'stock':      [50, 80, 50],
                           'increment_v':  [10,20,30],
                           'removal_v':   [10,20,30]}) 
    # Expected 
    expected_i = pandas.DataFrame({'increment_abg':[ 9.,  9.4, 16.5]})
    expected_r = pandas.DataFrame({'removal_abg':[15.5, 14.6, 26.7]})
    # Call the function on the increment
    result_i  = expand_biomass.convert_merch_vol_to_abg_mass(df, value = 'increment_v', irs ='increment')
    # Call the function on the removal 
    result_r  = expand_biomass.convert_merch_vol_to_abg_mass(df, value = 'increment_v', irs ='increment')
    # Test
    assert_series_equal(result_i['increment_abg'], expected_i['increment_abg']) 
    assert_series_equal(result_r['removal_abg'], expected_r['removal_abg']) 


def test_convert_abg_mass_to_abg_bg_c():
    """Test the function that convers the aboveground mass (tons of dry biomass
    of trunk plus branches) to the above ground plus below ground biomass
    expressed in tons of carbon.
    
    """
    # Input arguments

    # Expected

    # test
    pass

