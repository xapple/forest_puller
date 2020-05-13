#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #
from forest_puller.conversion.bcef_by_country import country_bcef

# First party modules #

# Third party modules #


###############################################################################
def convert_merch_vol_to_abg_mass(df, value, irs, bcef):
    """
    Convert merchantable biomass volume (m3 of trunk) to above ground biomass
    weight (tons of dry biomass of trunk plus branches) 

    Parameters
    ----------
    df: data frame containing climatic_zone, forest_type, area and stock columns.
    value: name of the value column
    irs: nature of the value columns ('stock', 'increment' or 'removals')

    Returns
    -------
    df: data frame (or series? to be determined) with the value converted in
    tons of above ground dry biomass
    """
    bcef = country_bcef.by_country_year 
    df = df.copy()
    result = result.lev

    pass

###############################################################################
def convert_abg_mass_to_abg_bg_mass(df):
    """
    Function that convers the aboveground mass (tons of dry biomass
    of trunk plus branches) to the above ground plus below ground biomass
    expressed in tons of carbon.
    i.e. given the 2 first term as input respectively I_v * BCEF_I and H_v * BCEF_R
    use (1+R) * CF to finish computing these forumlas:
    $$I_{c} = I_v * BCEF_I * (1+R) * CF$$
    $$L = H_v * BCEF_R * (1+R) * CF$$

    Note: the choice of R the root to shoot ratio is based on the stock level
    expressed in tons of above-ground biomass (tons of dry biomass)
    obtained from the convert_merch_vol_to_abg_mass function.

    R was loaded Chapter 4: Forest Land 2006 IPCC Guidelines for National Greenhouse Gas
    Inventories 4.49 TABLE 4.4 RATIO OF BELOW-GROUND  BIOMASS TO ABOVE-GROUND
    BIOMASS (R)
    https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_04_Ch4_Forest_Land.pdf
    """
    pass


