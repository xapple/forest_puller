#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

This test suite can be run with pytest.
Or you can import it individually:

    >>> from forest_puller.tests.conversion.test_bcef import test_bcef_intrpld
    >>> print(test_bcef_intrpld())
"""

# Built-in modules #

# Internal modules #
from forest_puller.conversion.bcef_by_country import country_bcef

# First party modules #

# Third party modules #
from pandas.testing import assert_series_equal

###############################################################################
def test_bcef_intrpld():
    """
    Test if the interpolation of the BCEF coefficients keeps coefficients
    identical for existing years.
    """
    # Input arguments #
    by_year = country_bcef.by_country_year
    intrpld = country_bcef.by_country_year_intrpld
    # Load #
    expected = by_year.copy()
    provided = intrpld.copy()
    # Take lines that are in the expected index only #
    expected = expected.set_index(['country', 'year'])
    provided = provided.set_index(['country', 'year'])
    provided = provided[provided.index.isin(expected.index)]
    # Compare #
    assert_series_equal(expected['bcefi'], provided['bcefi'])
    assert_series_equal(expected['bcefr'], provided['bcefr'])
    assert_series_equal(expected['bcefs'], provided['bcefs'])


