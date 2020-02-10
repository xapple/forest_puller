#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #
from forest_puller.core.country import Country
from forest_puller.common import country_codes
from forest_puller.reports.comparison import ComparisonReport

# Third party modules #

# First party modules #
from plumbing.cache import property_cached

###############################################################################
class Continent(object):
    """Aggregates countries together."""

    def __getitem__(self, key): return [c for c in self.countries if c.iso2_code == key][0]

    def __iter__(self): return iter(self.countries)

    def __len__(self):  return len(self.countries)

    def __init__(self):
        pass

    @property_cached
    def countries(self):
        return [Country(iso2) for iso2 in country_codes['iso2_code']]

    @property
    def first(self):
        return self.countries[0]

    @property_cached
    def report(self):
        return ComparisonReport(self)

###############################################################################
# Main object #
continent = Continent()
