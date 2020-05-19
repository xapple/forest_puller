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
from forest_puller.conversion.bcef_by_country import country_bcef

# First party modules #

# Third party modules #
import pandas
from pandas.testing import assert_frame_equal
from pandas.testing import assert_series_equal

###############################################################################
def test_by_country_year_interpolated():
    """
    Test if the interpolation result keep coefficients identical for existing years.
    """
    # Input arguments #
    expected = country_bcef.by_country_year
    interpolated = country_bcef.by_country_year_interpolated
    years = expected['year'].drop_duplicates()
    # Compute expected
    result = interpolated.query("year in @years").reset_index()
    # Compare
    assert_series_equal(result['bcefi'], expected['bcefi'])
    assert_series_equal(result['bcefr'], expected['bcefr'])
    assert_series_equal(result['bcefs'], expected['bcefs'])

