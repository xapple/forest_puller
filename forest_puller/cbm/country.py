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
        # Take all categories that are forested (not non-forested) #
        df = df.query("category != 'NF'").copy()
        # We have to sum the area over all classifiers #
        df = df.groupby(['year'])
        df = df.agg({'area': sum})
        df = df.reset_index()
        # Return #
        return df

    @property
    def area_country_cols(self):
        """Same as `self.area_df` but we add a column with the current country."""
        # Load #
        df = self.area_df.copy()
        # Add column #
        df.insert(0, 'country', self.iso2_code)
        # Return #
        return df

    @property_cached
    def losses_df(self):
        """
        Retrieve the provided volume from the post_processor in the
        historical scenario for this country and divide by the area.

        Relevant lines in `cbmcfs3_runner` are:

            df['vol_merch']     = (df['tc'] * 2)             / df['density']
            df['vol_sub_merch'] = (df['co2_production'] * 2) / df['density']
            df['vol_snags']     = (df['dom_production'] * 2) / df['density']
            df['tot_vol']       = df['vol_merch'] + df['vol_sub_merch'] + df['vol_snags']
        """
        # Cross-module import #
        from cbmcfs3_runner.core.continent import continent
        # Get the corresponding country and scenario #
        cbm_runner = continent.get_runner('historical', self.iso2_code, -1)
        # Load the table that interests us #
        df = cbm_runner.post_processor.harvest.provided_volume.copy()
        # We have to add the year column #
        df['year'] = cbm_runner.country.timestep_to_year(df['time_step'])
        # Drop the categories that have NaNs #
        df = df.dropna()
        # The status variable represents more a "category" in fact #
        df = df.rename(columns = {'status': 'category'})
        # Take all categories that are forested (not non-forested) #
        df = df.query("category != 'NF'").copy()
        # The values we are interested in #
        values = ['vol_merch', 'vol_snags', 'vol_sub_merch', 'vol_forest_residues',
                  'prov_carbon', 'tc', 'tot_vol']
        # We have to sum the values over all classifiers but keep the years #
        df = df.groupby(['year'])
        df = df.agg({v: 'sum' for v in values})
        df = df.reset_index()
        # Rename #
        df = df.rename(columns = {'tot_vol': 'losses'})
        # Add the area #
        df = df.left_join(self.area_df, on='year')
        # Divide by the area #
        df['loss_per_ha'] = df['losses'] / df['area']
        # By default losses are negative #
        df['loss_per_ha'] = - df['loss_per_ha']
        # Keep only some columns #
        df = df.filter(['year', 'loss_per_ha'])
        # Return #
        return df

    @property_cached
    def gains_df(self):
        """
        Lorem ipsum.
        """
        # Cross-module import #
        from cbmcfs3_runner.core.continent import continent
        # Get the corresponding country and scenario #
        cbm_runner = continent.get_runner('historical', self.iso2_code, -1)
        # Load straight from the database #
        flux_indicators  = self.database['tblFluxIndicators']
        # Return #
        return df

    @property_cached
    def increments_df(self):
        """Combine the losses and gains data frames for plotting."""
        # Load #
        losses = self.losses_df
        gains  = None # self.gains_df
        # Combine #
        df     = losses
        # Process #
        #df.rename(columns={'tot_vol': 'loss_per_ha'})
        # Return #
        return df

    #TODO cache this property once it's done
    @property
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
