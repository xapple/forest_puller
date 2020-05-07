#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May  6 17:10:11 2020
@author: paul
"""

def split_unknown_forest_type(df, remaining_forest_types, groups):
    """
    splits the unknown or mixed forest type amoung the given categories,
    for example if the input forest type are:
    forest type con | unknown | broad
    area        2   | 2       | 2
    split the unknown area 50%/50% between con and broad
    then aggregate back with con and broad.
    forest_type con | broad
    area        3   | 3
    This fucntion works both for area, stock or any other variable.

    Parameters
    ----------
    df : data frame containing a forest_type column
    any numeric column will be split and merged as described above.
    remaining_forest_types : forest types that should remain
        in the output data frame
    groups list of additional grouping variables, besides forest type
        which should remain unchanged (enable to keep country groupings)

    Returns
    -------
    df : data frame

    """

    return df


def compute_bcef(df):
    """
    compute the
    biomass conversion and expansion factors
    Based on data from table 4.5 of
    https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_04_Ch4_Forest_Land.pdf

    Parameters
    ----------
    df : data frame containing stock, area and forest type column.

    Returns
    -------
    df : data frame containing the bcef
        DESCRIPTION.
    """
    return df

