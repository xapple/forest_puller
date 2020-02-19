#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #
from forest_puller import cache_dir
from forest_puller.common import country_codes

# First party modules #
from plumbing.cache import property_cached, property_pickled_at

# Third party modules #
import numpy

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

    #-------------------------------- Area -----------------------------------#
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
        # Take all categories that are forested (not non-forested) #
        df = df.query("category != 'NF'").copy()
        # We have to sum the area over all classifiers #
        df = df.groupby(['year'])
        df = df.agg({'area': sum})
        df = df.reset_index()
        # Return #
        return df

    @property_pickled_at('area_cache_path')
    def area_country_cols(self):
        """Same as `self.area_df` but we add a column with the current country."""
        # Load #
        df = self.area_df.copy()
        # Add column #
        df.insert(0, 'country', self.iso2_code)
        # Return #
        return df

    #----------------------------- Increments --------------------------------#
    @property_cached
    def fluxes(self):
        """
        Retrieve the flux indicators from the post_processor in the
        historical scenario for this country and process the data.
        """
        # Cross-module import #
        from cbmcfs3_runner.core.continent import continent
        # Get the corresponding country and scenario #
        cbm_runner = continent.get_runner('historical', self.iso2_code, -1)
        # Load the table that interests us #
        df = cbm_runner.post_processor.database['tblFluxIndicators'].copy()
        # Add the classifiers #
        classifiers = cbm_runner.post_processor.classifiers
        df = df.left_join(classifiers, 'user_defd_class_set_id')
        # The status variable represents more a "category" in fact #
        df = df.rename(columns = {'status': 'category'})
        # Take all categories that are forested (not non-forested) #
        df = df.query("category != 'NF'").copy()
        # We only want to keep the 'time_step' and numeric columns #
        to_keep = ['time_step']
        to_drop = [name for name, kind in df.dtypes.items() if kind != numpy.float64]
        # Apply the final column list #
        columns = to_drop.copy()
        for col in to_keep: columns.remove(col)
        df = df.drop(columns=columns)
        # Pivot #
        df = df.melt(id_vars    = ['time_step'],
                     var_name   = 'pool',
                     value_name = 'tons_of_c')
        # Sum all things that are part of the same pool #
        df = (df
              .groupby(['time_step', 'pool'])
              .agg({'tons_of_c': 'sum'})
              .reset_index())
        # Add the year as the first column #
        year_col = cbm_runner.country.timestep_to_year(df['time_step'])
        df.insert(0, 'year', year_col)
        df = df.drop(columns=['time_step'])
        # Add the area #
        df = df.left_join(self.area_df, on='year')
        # Divide by the area #
        df['tons_of_c_per_ha'] = df['tons_of_c'] / df['area']
        # Return #
        return df

    loss_cols = ['soft_production', 'hard_production']
    gain_cols = ['gross_growth_ag'] # 'delta_biomass_ag'

    @property_cached
    def increments_df(self):
        """
        Combine the losses and gains into a dataframe for plotting.
        The columns used for losses and gains are variable.
        NB: Possibly there are some clues in the old
            `volume_increment_summary` MDB query.
        """
        # Load #
        df = self.fluxes
        # Filter based on list of pools #
        loss = df.loc[df['pool'].isin(self.loss_cols)]
        gain = df.loc[df['pool'].isin(self.gain_cols)]
        # Sum all things to make one pool #
        gain = (gain
                .groupby(['year'])
                .agg({'tons_of_c_per_ha': 'sum',})
                .reset_index())
        loss = (loss
                .groupby(['year'])
                .agg({'tons_of_c_per_ha': 'sum',})
                .reset_index())
        # Rename #
        gain = gain.rename(columns={'tons_of_c_per_ha': 'gain_per_ha'})
        loss = loss.rename(columns={'tons_of_c_per_ha': 'loss_per_ha'})
        # Combine #
        df = gain.left_join(loss, on='year')
        # By convention, losses should be negative values #
        df['loss_per_ha'] = - df['loss_per_ha']
        # Compute he net #
        df['net_per_ha'] = df['gain_per_ha'] + df['loss_per_ha']
        # Return #
        return df

    @property_pickled_at('increments_cache_path')
    def increments_country_cols(self):
        """Same as `self.increments_df` but we add a column with the current country."""
        # Load #
        df = self.increments_df.copy()
        # Add column #
        df.insert(0, 'country', self.iso2_code)
        # Return #
        return df

    #--------------------------------- Cache ---------------------------------#
    @property
    def area_cache_path(self):
        return cache_dir + 'eu_cbm/area/' + self.iso2_code + '.pickle'

    @property
    def increments_cache_path(self):
        return cache_dir + 'eu_cbm/increments/' + self.iso2_code + '.pickle'

###############################################################################
# Create every country object #
all_countries = [Country(iso2) for iso2 in country_codes['iso2_code']]
countries     = {c.iso2_code: c for c in all_countries}
