#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this submodule like this:

    >>> from forest_puller.conversion.convert_dynamics import soef_gain_loss_tc
    >>> print(soef_tain_loss_tc)
"""

# Built-in modules #

# Internal modules #
from forest_puller.viz.increments                   import gain_loss_net_data
from forest_puller.conversion.bcef_by_country       import country_bcef
from forest_puller.conversion.root_ratio_by_country import country_root_ratio
from forest_puller.viz.converted_to_tons            import converted_tons_data

# First party modules #

# Third party modules #

###############################################################################
def convert_gain_tc(df):
    """
    Convert the merchantable biomass increment $I_v$ [$m^3/ha$] to a biomass
    increment in tons of carbon (growth of both above and below ground biomass)
    $I_c$ [$10^3kg/ha$] based on equation 2.10 of the IPCC guidelines:

    $$I_{c} = I_v * BCEF_I * (1+R) * CF$$

    Where $BCEF_I$ [$10^3kg/m^3$] is the biomass conversion and expansion factor of
    the annual increment, it accounts both for the density and for the expansion of
    merchantable biomass to above ground biomass $R$ is the root to shoot ratio and
    $CF$ is the carbon fraction of dry biomass.

    Parameter:
        df a data frame containing a gain_per_ha column.
    """
    pass

###############################################################################
def convert_loss_tc(df):
    """
    Convert wood removal volumes (over bark) $H_v$ to losses $L$
    in tons of carbon according to equation 2.12 of the 2006 IPCC guidelines:

    $$L=H_v * BCEF_R * (1+R) * CF$$

    Where $BCEF_R$ is the expansion factor of wood and fuelwood removal volume
    to above-ground biomass removal.

    Parameter:
        df a data frame containing a loss_per_ha column.
    """
    pass

###############################################################################
def soef_gain_loss_tc():
    """
    Biomass gains i.e. increments and losses i.e. fellings from the State of
    Europe's Forest dataset expressed in tons of carbon.
    """
    # Input data
    df                    = gain_loss_net_data.soef.copy()
    bcef_by_country       = country_bcef.by_country_year
    root_ratio_by_country = country_root_ratio.by_country_year
    carbon_fraction       = converted_tons_data.carbon_fraction
    # Remember column names of input data frame
    columns_to_keep = df.columns
    # Join the biomass conversion and expansion factors bcef
    index = ['country', 'year']
    df = df.left_join(bcef_by_country, on=index)
    # Join the root to shoot ratio
    df = df.left_join(root_ratio_by_country, on=index)
    # Convert the gains to tons of carbon
    df['gain_per_ha'] *= df['bcefi'] * (1+df['root_ratio']) * carbon_fraction
    # Convert the losses to tons of carbon
    df['loss_per_ha'] *= df['bcefr'] * (1+df['root_ratio']) * carbon_fraction
    # Compute the net again
    df['net_per_ha'] = df['gain_per_ha'] - df['loss_per_ha']
    # Remove unnecessary columns
    df = df[columns_to_keep]
    # Return #
    return df

###############################################################################
def faostat_loss_tc():
    """
    Biomass losses i.e. removals from the FAOSTAT data converted to tons of carbon.
    """
    # Input data
    df                    = gain_loss_net_data.faostat.copy()
    bcef_by_country       = country_bcef.by_country_year_intrpld
    root_ratio_by_country = country_root_ratio.by_country_year
    carbon_fraction       = converted_tons_data.carbon_fraction
    # Remember column names of input data frame
    columns_to_keep = df.columns
    # Join the biomass conversion and expansion factors bcef
    index = ['country', 'year']
    df = df.left_join(bcef_by_country, on=index)
    # Join the root to shoot ratio
    df = df.left_join(root_ratio_by_country, on=index)
    # Convert the losses to tons of carbon
    df['loss_per_ha'] *= df['bcefr'] * (1+df['root_ratio']) * carbon_fraction
    # Remove unnecessary columns
    df = df[columns_to_keep]
    # Return #
    return df





