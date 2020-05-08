#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.other.tree_species_info import df as species_info
    >>> print(species_info)
"""

# Built-in modules #

# Internal modules #
from forest_puller import module_dir

# First party modules #
from plumbing.dataframes import multi_index_pivot

# Third party modules #
import pandas

###############################################################################
def load_bcef():
    """
    Parse the hard-coded table of biomass conversion and expansion factors BCEF.
    Copied from IPCC good practice guidance chapter 4, table 4.5.
    Load and assemble the biomass expansion factors into one table.

    Replace hardwood by "broad" and "other conifers" by "con" this is performed 
    as well as other replacements.
    in the code to allow changing this in the future
    """
    # Constants #
    bore = module_dir + 'extra_data/ipcc_bcef_boreal.csv'
    medi = module_dir + 'extra_data/ipcc_bcef_mediterranean.csv'
    temp = module_dir + 'extra_data/ipcc_bcef_temperate.csv'
    bore = pandas.read_csv(str(bore))
    medi = pandas.read_csv(str(medi))
    temp = pandas.read_csv(str(temp))
    # Concatenate #
    index = ['climatic_zone','forest_type','bcef']
    df = pandas.concat([bore.melt(id_vars=index),
                        medi.melt(id_vars=index), 
                        temp.melt(id_vars=index)])
    df['lower'] = df['variable'].str.split('_').str[1].astype(float)
    df['upper'] = df['variable'].str.split('_').str[2].astype(float)
    index = ['climatic_zone','forest_type', 'lower','upper']
    df = multi_index_pivot(df.set_index(index), columns='bcef', values='value') 
    # replace hardwood by broad and other conifers by conif see doctring
    replacement = dict({'hardwoods':'broad',
                        'firs and spruces':'con',
                        '.*conifers':'con'})
    for orig, dest in replacement.items(): 
        df['forest_type'] = (df['forest_type']
                .replace(to_replace=orig, value=dest, regex=True))

    # Return #
    return df 

###############################################################################
# Create a dataframe #
df = load_bcef()

