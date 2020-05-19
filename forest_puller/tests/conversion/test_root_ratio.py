#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

This test suite can be run with pytest.
Or you can import it individually:

    >>> from forest_puller.tests.conversion.test_root_ratio import test_root_intrpld
    >>> print(test_root_intrpld())
"""

# Built-in modules #

# Internal modules #
from forest_puller.conversion.root_ratio_by_country import country_root_ratio

# First party modules #

# Third party modules #
from pandas.testing import assert_series_equal

###############################################################################
def test_root_intrpld():
    """
    Test if the interpolation of the root coefficients keeps coefficients
    identical for existing years.
    """
    # Input arguments #
    by_year = country_root_ratio.by_country_year
    intrpld = country_root_ratio.by_country_year_intrpld
    # Load #
    expected = by_year.copy()
    provided = intrpld.copy()
    # Take lines that are in the expected index only #
    expected = expected.set_index(['country', 'year'])
    provided = provided.set_index(['country', 'year'])
    provided = provided[provided.index.isin(expected.index)]
    # Compare #
    assert_series_equal(expected['root_ratio'], provided['root_ratio'])
