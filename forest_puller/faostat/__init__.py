#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Third party modules #
import pandas

# Internal modules #
from forest_puller import module_dir
from forest_puller.common import country_codes

###############################################################################
def fix_faostat_tables(df):
    """Format and filter the data frame and store it in cache."""
    # Load the data frame by copy #
    df = df.copy()
    # The column "Year code" is redundant with "Year" #
    df.drop(columns=['Year Code'], inplace=True)
    # We won't be using area codes to refer to countries #
    df.drop(columns=['Area Code'], inplace=True)
    # Better names for the columns #
    df.rename(inplace = True,
              columns = {'Area':         'country',
                         'Item Code':    'item_code',
                         'Item':         'item',
                         'Unit':         'unit',
                         'Element Code': 'element_code',
                         'Element':      'element',
                         'Year':         'year',
                         'Value':        'value',
                         'Flag':         'flag'})
    # Wrong name for one country "Czechia" #
    df['country'] = df['country'].replace({'Czechia': 'Czech Republic'})
    # Remove countries we are not interested in #
    selector = df['country'].isin(country_codes['country'])
    df       = df[selector]
    # Use country short codes instead of long names #
    name_to_iso_code = dict(zip(country_codes['country'], country_codes['iso2_code']))
    df['country'] = df['country'].replace(name_to_iso_code)
    # We will multiply the USD value by 1000 and drop the 1000 from "unit" #
    selector = df['unit'] == '1000 US$'
    df.loc[selector, 'unit']   = 'usd'
    df.loc[selector, 'value'] *= 1000
    # Return #
    return df
