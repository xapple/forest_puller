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


def choose_bcef(df):
    """
    Choose the biomass conversion and expansion factors.
    based on climatic_zone, forest_type 
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

def 

def convert_abg_mass_to_abg_bg_c(df):
    """
    """
    pass


