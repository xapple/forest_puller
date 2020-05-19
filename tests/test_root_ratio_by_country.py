
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
from forest_puller.conversion.root_ratio_by_country import country_root_ratio

# First party modules #

# Third party modules #
import pandas
from pandas.testing import assert_frame_equal
from pandas.testing import assert_series_equal

def test_by_country_year_interpolated():
    """
    Test if the interpolation result keep coefficients identical for existing years.
    """
    expected = country_root_ratio.by_country_year
    interpolated = country_root_ratio.by_country_year_interpolated
    years = expected['year'].drop_duplicates()
    # Compute expected
    result = interpolated.query("year in @years").reset_index()
    # Compare
    assert_series_equal(result['root_ratio'], expected['root_ratio'])



