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
def split_unknown_forest_type(df, remaining_forest_types, groups=None):
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


def compute_bcef(df):
    """
    Compute the biomass conversion and expansion factors.

    Based on data from table 4.5 of
    https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_04_Ch4_Forest_Land.pdf

    Parameters
    ----------
    df: data frame containing stock, area and forest type column.

    Returns
    -------
    df: data frame containing the bcef factors.
    """
    return df

