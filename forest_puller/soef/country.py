#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.soef.country import all_countries
    >>> print([(c.xls.path, c.xls.exists) for c in all_countries])
"""

# Built-in modules #

# Internal modules #
from forest_puller import cache_dir
from forest_puller.soef.table_parser import ForestArea, AgeDist, Fellings
from forest_puller.soef.growing_stock import GrowingStockComp
from forest_puller.common import country_codes

# First party modules #
from plumbing.cache import property_cached

# Third party modules #

###############################################################################
class Country:
    """
    Represents one country's dataset.
    """

    def __init__(self, iso2_code, xls_dir):
        # The reference ISO2 code #
        self.iso2_code = iso2_code
        # Record where the cache will be located on disk #
        self.xls_dir   = xls_dir
        # Record where the excel file will be located on disk #
        self.xls_file  = self.xls_dir + self.iso2_code + '.xls'

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.iso2_code)

    def tables(self):
        return [self.forest_area, self.age_dist, self.fellings]

    #------------------------------ Tables -----------------------------------#
    @property_cached
    def forest_area(self): return ForestArea(self)

    @property_cached
    def age_dist(self):    return AgeDist(self)

    @property_cached
    def fellings(self):    return Fellings(self)

    @property_cached
    def stock_comp(self):  return GrowingStockComp(self)

###############################################################################
# Create every country object #
cache_path    = cache_dir + 'soef/xls/'
all_countries = [Country(iso2, cache_path) for iso2 in country_codes['iso2_code']]
countries     = {c.iso2_code: c for c in all_countries}