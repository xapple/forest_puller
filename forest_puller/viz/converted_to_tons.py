#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule like this:

    >>> from forest_puller.viz.converted_to_tons import converted_tons_data
    >>> print(converted_tons_data.df)
"""

# Built-in modules #

# Internal modules #
from forest_puller.viz.increments    import GainsLossNetGraph, GainsLossNetLegend
from forest_puller.common            import country_codes
from forest_puller                   import cache_dir
from forest_puller.viz.increments_df import increments_data as gain_loss_net_data

# First party modules #
from plumbing.cache  import property_cached

# Third party modules #

###############################################################################
class ConvertedTonsData:
    """
    Aggregate and prepare all the dataframes that will be used in the
    'converted to tons' visualization.

    * The following is considered in each country per year per hectare.
    * Start with: cubic meter in [m^3].
    * Obtain: the tons per carbon in [kg].
    """

    # This value comes from:
    # https://www.unece.org/fileadmin/DAM/timber/publications/DP-49.pdf
    bark_correction_factor = 0.88

    # This value comes from:
    # https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_04_Ch4_Forest_Land.pdf
    carbon_fraction = 0.47

    #----------------------------- Data sources ------------------------------#
    @property
    def bcef(self):
        """Convenience shortcut to the bcef_by_country dataframe."""
        # Import #
        from forest_puller.conversion.bcef_by_country import country_bcef
        # Load #
        df = country_bcef.by_country_year_intrpld
        # Return #
        return df

    @property
    def root_ratio(self):
        """Convenience shortcut to the root_ratio_by_country dataframe."""
        # Import #
        from forest_puller.conversion.root_ratio_by_country import country_root_ratio
        # Load #
        df = country_root_ratio.by_country_year_intrpld
        # Return #
        return df

    #------------------------ Data sources modified --------------------------#
    @property
    def soef(self):
        """
        Biomass gains i.e. increments and losses i.e. fellings from the State of
        Europe's Forest dataset expressed in tons of carbon.
        SOEF data is over bark.
        """
        # Load #
        df = gain_loss_net_data.soef.copy()
        # Join the biomass conversion and expansion factors bcef #
        index = ['country', 'year']
        df = df.left_join(self.bcef, on=index)
        # Join the root to shoot ratio #
        df = df.left_join(self.root_ratio, on=index)
        # Convert the gains to tons of carbon #
        df['gain_per_ha'] *= df['bcefi'] * (1 + df['root_ratio']) * self.carbon_fraction
        # Convert the losses to tons of carbon #
        df['loss_per_ha'] *= df['bcefr'] * (1 + df['root_ratio']) * self.carbon_fraction
        # Compute the net again #
        df['net_per_ha'] = df['gain_per_ha'] + df['loss_per_ha']
        # Remove unnecessary columns #
        df = df[gain_loss_net_data.soef.columns]
        # Return #
        return df

    @property_cached
    def faostat(self):
        """FAOSTAT data is under bark."""
        # Load #
        df = gain_loss_net_data.faostat.copy()
        # Join the biomass conversion and expansion factors bcef #
        index = ['country', 'year']
        df = df.left_join(self.bcef, on=index)
        # Join the root to shoot ratio #
        df = df.left_join(self.root_ratio, on=index)
        # Convert the losses to tons of carbon #
        df['loss_per_ha'] *= df['bcefr'] * (1 + df['root_ratio']) * self.carbon_fraction
        # Bark correction factor #
        df['loss_per_ha'] /= self.bark_correction_factor
        # Remove unnecessary columns #
        df = df[gain_loss_net_data.faostat.columns]
        # Return #
        return df

    @property_cached
    def hpffre(self):
        """HPFFRE data is over bark."""
        # Load #
        df = gain_loss_net_data.hpffre.copy()
        # Join the biomass conversion and expansion factors bcef #
        index = ['country', 'year']
        df = df.left_join(self.bcef, on=index)
        # Join the root to shoot ratio #
        df = df.left_join(self.root_ratio, on=index)
        # Convert the losses to tons of carbon #
        df['loss_per_ha'] *= df['bcefr'] * (1 + df['root_ratio']) * self.carbon_fraction
        # Remove unnecessary columns #
        df = df[gain_loss_net_data.hpffre.columns]
        df = df.drop(columns=['gain_per_ha', 'net_per_ha'])
        # Return #
        return df

    #----------------------- Data sources unmodified -------------------------#
    @property_cached
    def ipcc(self):
        """No changes for the IPCC data."""
        # Load #
        df = gain_loss_net_data.ipcc.copy()
        # Return #
        return df

    @property
    def eu_cbm(self):
        """No changes for the EU-CBM data."""
        # Load #
        df = gain_loss_net_data.eu_cbm.copy()
        # Return #
        return df

###############################################################################
class ConvertedTonsGraph(GainsLossNetGraph):

    # Cosmetic params #
    share_y        = True

    # Optional extras #
    add_soef_line  = False
    add_fra_line   = False

    # Mapping of unit to each source #
    source_to_y_label = {
        'ipcc':    "Tons of carbon per hectare",
        'soef':    "",
        'faostat': "",
        'hpffre':  "",
        'eu-cbm':  "",
    }

    # The lines we want on each axes #
    curves = ('gain_per_ha', 'loss_per_ha', 'net_per_ha')

    @property
    def all_data(self):
        """A link to the dataframe containing all countries."""
        return converted_tons_data

###############################################################################
class ConvertedTonsLegend(GainsLossNetLegend):
    add_soef_line = False
    add_fra_line  = False

###############################################################################
# Create the large df #
converted_tons_data = ConvertedTonsData()

# Create a facet for each country #
export_dir = cache_dir + 'graphs/converted_tons/'
all_codes  = list(country_codes['iso2_code'])
all_graphs = [ConvertedTonsGraph(iso2, export_dir) for iso2 in all_codes]
countries  = {c.parent: c for c in all_graphs}

# Create a separate standalone legend #
legend = ConvertedTonsLegend(base_dir = cache_dir + 'graphs/increments/')