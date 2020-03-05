#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule this like:

    >>> from forest_puller.viz.converted_to_tons import converted_tons_data
    >>> print(converted_tons_data.df)
"""

# Built-in modules #

# Internal modules #
from forest_puller.viz.increments import GainsLossNetGraph, GainsLossNetLegend
from forest_puller.viz.increments import gain_loss_net_data
from forest_puller.common         import country_codes
from forest_puller                import cache_dir

# First party modules #
from plumbing.cache  import property_cached

# Third party modules #
import pandas, numpy

###############################################################################
class ConvertedTonsData:
    """
    Aggregate and prepare all the dataframes that will be used in the
    'converted to tons' visualization.

    * The following is considered in each country per year per hectare.
    * Start with: one cubic meter.
    * Obtain: the density in [kg / m^3].
    * Multiply the volume with the density to obtain [kg].
    * Multiply the result by 1000 to obtain [tons].
    * Multiply the result with the bark correction factor.
    * The result is now in tons of carbon over bark.
    """

    # This value comes from:
    # https://www.unece.org/fileadmin/DAM/timber/publications/DP-49.pdf
    bark_correction_factor = 0.88

    #----------------------------- Data sources ------------------------------#
    @property
    def avg_dnsty_intrpld(self):
        """Convenience shortcut to the avg_dnsty_intrpld dataframe."""
        # Import #
        from forest_puller.soef.composition import composition_data
        # Load #
        df = composition_data.avg_dnsty_intrpld
        # Filter #
        df = df.drop(columns=['frac_missing'])
        # Return #
        return df

    #------------------------ Data sources modified --------------------------#
    @property
    def soef(self):
        """SOEF data is over bark."""
        # Load #
        df = gain_loss_net_data.soef
        # Join #
        df = df.left_join(self.avg_dnsty_intrpld, on=['country', 'year'])
        # Multiply #
        df['gain_per_ha'] *= df['avg_density'] / 1000
        df['loss_per_ha'] *= df['avg_density'] / 1000
        df['net_per_ha']  *= df['avg_density'] / 1000
        # Drop #
        df = df.drop(columns=['avg_density'])
        # Reset index #
        df = df.reset_index(drop=True)
        # Return #
        return df

    @property_cached
    def faostat(self):
        """FAOSTAT data is under bark."""
        # Load #
        df = gain_loss_net_data.faostat.copy()
        # Join #
        df = df.left_join(self.avg_dnsty_intrpld, on=['country', 'year'])
        # Multiply #
        df['loss_per_ha'] *= df['avg_density'] / (1000 * self.bark_correction_factor)
        # Drop #
        df = df.drop(columns=['avg_density'])
        # Reset index #
        df = df.reset_index(drop=True)
        # Return #
        return df

    @property_cached
    def hpffre(self):
        """HPFFRE data is over bark."""
        # Load #
        df = gain_loss_net_data.hpffre.copy()
        # Join #
        df = df.left_join(self.avg_dnsty_intrpld, on=['country', 'year'])
        # Multiply #
        df['gain_per_ha'] *= df['avg_density'] / 1000
        df['loss_per_ha'] *= df['avg_density'] / 1000
        df['net_per_ha']  *= df['avg_density'] / 1000
        # Drop #
        df = df.drop(columns=['avg_density'])
        # Reset index #
        df = df.reset_index(drop=True)
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

    #------------------------------- Combine ---------------------------------#
    @property_cached
    def df(self):
        # Load all data sources #
        sources = [self.ipcc, self.soef, self.faostat, self.hpffre, self.eu_cbm]
        # Combine data sources #
        df = pandas.concat(sources, ignore_index=True)
        # Return #
        return df

###############################################################################
class ConvertedTonsGraph(GainsLossNetGraph):

    # Cosmetic params #
    share_y        = True

    # Optional extras #
    add_soef_line  = False

    # Mapping of unit to each source #
    source_to_y_label = {
        'ipcc':    "Tons of carbon per hectare",
        'soef':    "",
        'faostat': "",
        'hpffre':  "",
        'eu-cbm':  "",
    }

    @property
    def all_data(self):
        """A link to the dataframe containing all countries."""
        return converted_tons_data.df

###############################################################################
class ConvertedTonsLegend(GainsLossNetLegend):
    add_soef_line = False

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