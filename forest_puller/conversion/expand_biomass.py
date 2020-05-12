#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #

# First party modules #

# Third party modules #

###############################################################################
def distribute_unknown_forest_type(df, remaining_forest_types, groups=None):
    """
    Distribute the unknown or mixed forest type among the given categories,
    for example if the input forest type are:

        forest type | con | unknown | broad
        area        |   2 |      2  |     2

    Split the unknown area 50%/50% between con and broad
    then aggregate back with con and broad.

        forest_type | con | broad
        area        |   3 |     3

    This function works both for area, stock or any other variable.

    Parameters
    ----------
    df: data frame containing a forest_type column. Any numeric column
        will be split and merged as described above.

    remaining_forest_types : forest types that should remain
                             in the output data frame.

    groups: list of additional grouping variables, besides forest type
            which should remain unchanged (enable to keep country groupings).

    Returns
    -------
    df: data frame
    """
    return df.query("")

###############################################################################
def choose_bcef(df):
    """
    Choose the biomass conversion and expansion factors.
    Based on climatic_zone, forest_type
    and the lower and upper bounds on stock per hectare levels.

    # TODO, this function might actually be
    # join_bcef() if that makes things easier to return df and the 3 additional bcef columns.

    Parameters
    ----------
    df: data frame containing climatic_zone, forest_type, area and stock columns.

    Returns
    -------
    df: data frame containing the bcef factors.
    """

return df

###############################################################################
def convert_merch_vol_to_abg_mass(df, value, irs):
    """
    Convert merchantable biomass volume (m3 of trunk)
       to above ground biomass weight (tons of dry biomass of trunk plus branches)
    Parameters
    ----------
    df: data frame containing climatic_zone, forest_type, area and stock columns.
    value: name of the value column
    irs: nature of the value columns ('increment' or 'removals')

    Returns
    -------
    df: data frame (or series? to be determined) with the value converted in
    tons of above ground dry biomass
    """
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


