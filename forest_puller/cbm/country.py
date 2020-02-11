#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #
from forest_puller.common import country_codes

# First party modules #
from plumbing.cache import property_cached

# Third party modules #

###############################################################################
class Country:
    """
    A simple wrapper to the Country object found in the `cbmcfs3_runner`
    package and the corresponding data in the `cbmcfs3_data` repository.
    Unfortunately this data was prepared by our predecessor and is not made
    public. We reference it here for comparison purposes only.
    """

    def __init__(self, iso2_code):
        # The reference ISO2 code #
        self.iso2_code = iso2_code

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.iso2_code)

    @property_cached
    def area_df(self):
        """
        Load the age indicators table for this country in the
        historical scenario and prepare the data.
        """
        # Cross-module import #
        from cbmcfs3_runner.core.continent import continent
        # Get the corresponding country and scenario #
        cbm_runner = continent.get_runner('historical', self.iso2_code, -1)
        # Load the table that interests us #
        df = cbm_runner.post_processor.inventory.age_indicators.copy()
        # We have to add the year column #
        df['year'] = cbm_runner.country.timestep_to_year(df['time_step'])
        # The status variable represents more a "category" in fact #
        df = df.rename(columns = {'status': 'category'})
        # Drop the categories that have NaNs #
        df = df.dropna()
        # Take all categories that are not non-forested #
        df = df.query("category != 'NF'").copy()
        # We have to sum the area over all classifiers #
        df = df.groupby(['year'])
        df = df.agg({'area': sum})
        df = df.reset_index()
        # Return #
        return df

    @property
    def area_country_cols(self):
        """Same as `self.df` but we add a column with the current country."""
        # Load #
        df = self.area_df.copy()
        # Add column #
        df.insert(0, 'country', self.iso2_code)
        # Return #
        return df

###############################################################################
# Create every country object #
all_countries = [Country(iso2) for iso2 in country_codes['iso2_code']]
countries     = {c.iso2_code: c for c in all_countries}
