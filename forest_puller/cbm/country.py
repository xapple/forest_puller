#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule this like:

    >>> from forest_puller.cbm.country import countries
    >>> country = countries['FR']
    >>> print(country.stock_comp_genus)
"""

# Built-in modules #

# Internal modules #
from forest_puller import cache_dir
from forest_puller.common import country_codes

# First party modules #
from plumbing.cache import property_cached, property_pickled_at

# Third party modules #
import numpy, pandas

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
        # Create fake dataframes for cyprus that is missing #
        if self.iso2_code == 'CY':
            self.area_df          = pandas.DataFrame(columns=['year', 'area'])
            self.increments_df    = pandas.DataFrame()
            self.stock_comp_genus = pandas.DataFrame(columns=['genus', 'year', 'stock_m3'])

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.iso2_code)

    #----------------------------- Common years ------------------------------#
    @property_cached
    def area_years(self):
        """
        Determine the years for which there is a data point in every single
        country of this data source for the area statistic.
        Return a list of integers, e.g. [1999, 2000, 2001, 2004].
        """
        return self.area_df['year'].unique()

    #-------------------------------- Area -----------------------------------#
    @property_pickled_at('area_cache_path')
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

    #------------------------------- Fluxes ----------------------------------#
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

    #----------------------------- Increments --------------------------------#
    loss_cols = ['soft_production', 'hard_production']
    gain_cols = ['gross_growth_ag'] # 'delta_biomass_ag'

    @property_pickled_at('increments_cache_path')
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

    @property
    def increments_country_cols(self):
        """Same as `self.increments_df` but we add a column with the current country."""
        # Load #
        df = self.increments_df.copy()
        # Add column #
        df.insert(0, 'country', self.iso2_code)
        # Return #
        return df

    #------------------------------- Genera ----------------------------------#
    @property_pickled_at('stock_comp_cache_path')
    def stock_comp_genus(self):
        """
        Looks like:

               genus  year      stock_m3
               -----  ----      --------
               abies  1997  1.003850e+08
               abies  1998  1.009454e+08
               abies  1999  1.014880e+08
                 ...   ...           ...
             quercus  2013  6.360644e+08
             quercus  2014  6.478733e+08
             quercus  2015  6.596905e+08
        """
        # Cross-module import #
        from cbmcfs3_runner.core.continent import continent
        # Get the corresponding country and scenario #
        cbm_runner = continent.get_runner('historical', self.iso2_code, -1)
        # Load the table that interests us #
        df = cbm_runner.post_processor.ipcc.pool_indicators_long.copy()
        # The status variable represents more a "category" in fact #
        df = df.rename(columns = {'status': 'category'})
        # Take all categories that are forested (not non-forested) #
        df = df.query("category != 'NF'").copy()
        # Keep only the above ground biomass entries #
        df = df.query("ipcc_pool == 'abogr_bmass'")
        # Add the conversion coefficient's from mass to density #
        coefs = cbm_runner.post_processor.coefficients[['forest_type', 'density']]
        # Join the volumetric mass density in [tons/m^3] #
        df = df.left_join(coefs, on='forest_type')
        # Check there are no NaNs in density #
        assert not df['density'].isna().any()
        # Multiply mass by coefficients #
        df['stock_m3'] = df['tc'] / df['density']
        # Import species names #
        from cbmcfs3_runner.pump.tree_species_info import df as species_info_cbm
        # Join species names #
        df = df.left_join(species_info_cbm, on='forest_type')
        # Replace NaN values by 'missing' #
        df['genus']   = df['genus'].fillna('missing')
        df['species'] = df['species'].fillna('missing')
        # Reorder the two columns columns #
        cols = list(df.columns)
        cols.remove("genus")
        cols.remove("species")
        cols.insert(0, "species")
        cols.insert(0, "genus")
        df = df.reindex(columns=cols)
        # Drop some columns #
        to_drop = ['time_step', 'area', 'ipcc_pool', 'common_name', 'tc', 'density']
        df = df.drop(columns=to_drop)
        # Aggregate by year and genus #
        df = df.groupby(['genus', 'year'])
        df = df.aggregate({'stock_m3': 'sum'})
        df = df.reset_index()
        # Sort the dataframe #
        df = df.sort_values(by=['year', 'stock_m3'])
        # Return #
        return df

    #--------------------------------- Cache ---------------------------------#
    @property
    def area_cache_path(self):
        return cache_dir + 'eu_cbm/area/' + self.iso2_code + '.pickle'

    @property
    def increments_cache_path(self):
        return cache_dir + 'eu_cbm/increments/' + self.iso2_code + '.pickle'

    @property
    def stock_comp_cache_path(self):
        return cache_dir + 'eu_cbm/stock_comp/' + self.iso2_code + '.pickle'

###############################################################################
# Create every country object #
all_countries = [Country(iso2) for iso2 in country_codes['iso2_code']]
countries     = {c.iso2_code: c for c in all_countries}
