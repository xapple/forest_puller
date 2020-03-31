#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

A script to regenerate all the pickle files in `puller_cache`

Typically you would run this file from a command line like this:

     ipython3 -i -- ~/deploy/forest_puller/tests/test_dev.py
"""

# Built-in modules #
from pprint import pprint

# Third party modules #
import pandas
from tqdm import tqdm

###############################################################################
from forest_puller.ipcc.country import all_countries
for c in tqdm(all_countries, desc='Countries'):
    for y in tqdm(c, desc='Years', leave=False):
        del y.df
        df = y.df

###############################################################################
from forest_puller.cbm.country import all_countries
for country in tqdm(all_countries):
    del country.area_df
    df = country.area_df
    del country.increments_df
    df = country.increments_df
    del country.stock_comp_genus
    df = country.stock_comp_genus

###############################################################################
from forest_puller.faostat.land.country import all_countries
for country in tqdm(all_countries):
    del country.df
    df = country.df

###############################################################################
from forest_puller.faostat.forestry.country import all_countries
for country in tqdm(all_countries):
    del country.df
    df = country.df

###############################################################################
from forest_puller.fra.country import all_countries
for country in tqdm(all_countries):
    del country.df
    df = country.df

###############################################################################
from forest_puller.hpffre.country import all_countries
for country in tqdm(all_countries):
    del country.stock_comp.df
    df = country.stock_comp.df

###############################################################################
from forest_puller.soef.country import all_countries
for country in tqdm(all_countries):
    del country.forest_area
    del country.age_dist
    del country.fellings
    del country.stock_comp
    table1 = country.forest_area
    table2 = country.age_dist
    table3 = country.fellings
    table4 = country.stock_comp

###############################################################################
from forest_puller.soef.composition import composition_data
del composition_data.avg_dnsty_intrpld
interpolated = composition_data.avg_dnsty_intrpld

