#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #

# Internal modules #
from forest_puller import module_dir

# First party modules #

# Third party modules #
import pandas

###############################################################################
def load_bcef():
    """
    Parse the hard-coded table of biomass conversion and expansion factors BCEF.
    Copied from IPCC good practice guidance chapter 4, table 4.5.

    https://www.ipcc-nggip.iges.or.jp/public/2006gl/pdf/4_Volume4/V4_04_Ch4_Forest_Land.pdf

    Load and assemble the biomass expansion factors into one table.
    Columns are:

    ['climatic_zone', 'forest_type', 'lower', 'upper', 'bcefi', 'bcefr', 'bcefs']

    Lower and upper columns are the bounds on the stock per hectare
    (in cubic meters).

    * bcefi is the biomass conversion and expansion factor for the increment.
    * bcefr is the biomass conversion and expansion factor for the removals.
    * bcefs is the biomass conversion and expansion factor for the stock.

    We replace hardwood by "broad" and "other conifers" by "con".
    These replacements as well as others are performed in this function
    to allow changing this in the future.

    # TODO load the root to shoot ratio here or somewhere else.
    """
    # Constants #
    bore = module_dir + 'extra_data/ipcc_bcef_boreal.csv'
    medi = module_dir + 'extra_data/ipcc_bcef_mediterranean.csv'
    temp = module_dir + 'extra_data/ipcc_bcef_temperate.csv'
    # Load CSVs #
    bore = pandas.read_csv(str(bore))
    medi = pandas.read_csv(str(medi))
    temp = pandas.read_csv(str(temp))
    # Unpivot #
    index = ['climatic_zone', 'forest_type', 'bcef']
    bore = bore.melt(id_vars=index)
    medi = medi.melt(id_vars=index)
    temp = temp.melt(id_vars=index)
    # Concatenate #
    df = pandas.concat([bore, medi, temp])
    # Parse the upper and lower bounds in the column names #
    df['lower'] = df['variable'].str.split('_').str[1].astype(float)
    df['upper'] = df['variable'].str.split('_').str[2].astype(float)
    # Set index and pivot #
    df = df.pipe(pandas.pivot_table,
                 index   = ['climatic_zone', 'forest_type', 'lower', 'upper'],
                 columns = ['bcef'],
                 values  = ['value'])
    # Reset index #
    df = df.reset_index()
    # Replace hardwood by broad and others by coniferous #
    replacements = (('hardwoods',         'broad'),
                    ('firs and spruces',  'con'),
                    ('.*conifers',        'con'))
    # Rename all items (see docstring) #
    for orig, dest in replacements:
        df['forest_type'] = df['forest_type'].replace(to_replace = orig,
                                                      value      = dest,
                                                      regex      = True)
    # Flatten the index
    df.columns = [col[0] if not col[1] else col[1] for col in df.columns.values]
    # Return #
    return df

###############################################################################
# Create a dataframe #
df = load_bcef()
