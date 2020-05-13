#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

This test suite can be run with pytest.
"""

# Built-in modules #

# Internal modules #
from forest_puller.conversion import expand_biomass

# First party modules #

# Third party modules #
import pandas
from pandas.testing import assert_frame_equal
from pandas.testing import assert_series_equal

###############################################################################
def test_choose_bcef():
    """
    Test the function that aggregates and compute the
    biomass conversion and expansion factors.

    This test cannot work because the corresponding methods 
    are not implemented in a functional way. 
    """
    # Input arguments #
    df = pandas.DataFrame({'climatic_zone': ['Temperate', 'Boreal', 'Mediterranean'],
                           'forest_type':   ['broad', 'con', 'broad'],
                           'area':          [1, 2, 1],
                           'stock':         [50, 80, 50]})
    # Expected bcef series
    # Note: the result data frame might contain more columns than this one,
    # test should pass as long as it contains these series
    expected = pandas.DataFrame({'bcefi': [0.900, 0.470, 0.550],
                                 'bcefr': [1.55,   0.73, 0.89],
                                 'bcefs': [1.40,   0.66, 0.80]})
    # Call the function #
    result = expand_biomass.country_bcef

    # Test #
    assert_series_equal(result['bcefi'], expected['bcefi'])
    assert_series_equal(result['bcefr'], expected['bcefr'])
    assert_series_equal(result['bcefs'], expected['bcefs'])

###############################################################################
def test_convert_merch_vol_to_abg_mass_by_country():
    """
    Test the function that converts merchantable biomass volume (m3 of trunk)
    to above ground biomass weight (tons of dry biomass of trunk plus branches).
    """
    # Input arguments #
    # This assumption is wrong, we don't have the increment by con and broad
    # We only have the increment by country
    # but is this a problem?
    df = pandas.DataFrame({'country': ['FI', 'AT', 'GR'],
                           'increment_v':   [10, 20, 30],
                           'removal_v':     [10, 20, 30]})
    bcef = pandas.DataFrame({'country': ['FI', 'AT', 'GR'],
                             'bcefi': [1, 1.2, 2],
                             'bcefr': [1.2,2.2,1.2]})
    bcef = pandas.DataFrame({'climatic_zone': ['Temperate', 'Boreal', 'Mediterranean'],
                           'leaf_type':   ['broad', 'con', 'broad'],
    # Expected #
    expected_i = pandas.DataFrame({'increment_abg': [9.0,   9.4, 16.5]})
    expected_r = pandas.DataFrame({'removal_abg':   [15.5, 14.6, 26.7]})
    # Call the function on the increment #
    result_i  = expand_biomass.convert_merch_vol_to_abg_mass(
        df, value = 'increment_v', irs ='increment'
    )
    # Call the function on the removal #
    result_r  = expand_biomass.convert_merch_vol_to_abg_mass(
        df, value = 'increment_v', irs ='increment'
    )
    # Test #
    assert_series_equal(result_i['increment_abg'], expected_i['increment_abg'])
    assert_series_equal(result_r['removal_abg'],   expected_r['removal_abg'])

def test_convert_merch_vol_to_abg_mass_by_climate_leaf_type():
    """
    Test the function that converts merchantable biomass volume (m3 of trunk)
    to above ground biomass weight (tons of dry biomass of trunk plus branches).
    by other index variables.
    """
    # Input arguments #
    # This assumption is wrong, we don't have the increment by con and broad
    # We only have the increment by country
    # but is this a problem?
    df = pandas.DataFrame({'climatic_zone': ['Temperate', 'Boreal', 'Mediterranean'],
                           'leaf_type':   ['broad', 'con', 'broad'],
                           'area':          [1, 2, 1],
                           'stock':         [50, 80, 50],
                           'increment_v':   [10, 20, 30],
                           'removal_v':     [10, 20, 30]})
    bcef = pandas.DataFrame({'climatic_zone': ['Temperate', 'Boreal', 'Mediterranean'],
                           'leaf_type':   ['broad', 'con', 'broad'],i
    # Expected #
    expected_i = pandas.DataFrame({'increment_abg': [9.0,   9.4, 16.5]})
    expected_r = pandas.DataFrame({'removal_abg':   [15.5, 14.6, 26.7]})
    # Call the function on the increment #
    result_i  = expand_biomass.convert_merch_vol_to_abg_mass(
        df, value = 'increment_v', irs ='increment'
    )
    # Call the function on the removal #
    result_r  = expand_biomass.convert_merch_vol_to_abg_mass(
        df, value = 'increment_v', irs ='increment'
    )
    # Test #
    assert_series_equal(result_i['increment_abg'], expected_i['increment_abg'])
    assert_series_equal(result_r['removal_abg'],   expected_r['removal_abg'])

###############################################################################
def test_convert_abg_mass_to_abg_bg_c():
    """
    Test the function that converts the above ground mass (tons of dry biomass
    of trunk plus branches) to the above ground plus below ground biomass
    expressed in tons of carbon.
    """
    pass

