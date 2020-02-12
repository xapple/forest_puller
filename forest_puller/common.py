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

# Third party modules #
import numpy, pandas

# Load country codes #
country_codes = module_dir + 'extra_data/country_codes.csv'
country_codes = pandas.read_csv(str(country_codes))

###############################################################################
def convert_row_names(df, row_name_map, col_name_map, data_source_name):
    # Prepare row_name_map #
    before = list(row_name_map[data_source_name])
    after  = list(row_name_map['forest_puller'])
    # Load the row titles #
    row_titles = df.iloc[:, 0]
    # Strip whitespace #
    row_titles = row_titles.str.strip()
    # Convert to short titles using row_name_map #
    row_titles = row_titles.replace(before, after)
    # Assign #
    df.iloc[:, 0] = row_titles
    # Units #
    convert_units(df, col_name_map)
    # Return #
    return df

###############################################################################
def convert_units(df, col_name_map):
    # Convert units (such that we never have kilo hectares, only hectares etc.) #
    col_name_to_ratio = dict(zip(col_name_map['forest_puller'], col_name_map['unit_convert_ratio']))
    for col_name in df.columns:
        ratio = col_name_to_ratio.get(col_name, numpy.NaN)
        if numpy.isnan(ratio): continue
        df[col_name] = df[col_name].astype(float)
        df[col_name] = df[col_name] * ratio
    # Return #
    return df