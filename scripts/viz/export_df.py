#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass project.
Unit D1 Bioeconomy.

A script to export an intermediary data frame to CSV for inspection
and sharing.

Typically you would run this file from a command line like this:

     ipython3 -i -- ~/deploy/forest_puller/scripts/viz/export_df.py
"""

# Built-in modules #

# Third party modules #

# Internal modules #
from forest_puller.viz.area_aggregate import area_agg
from forest_puller import cache_dir

###############################################################################
export_path = cache_dir + 'exports/area_agg_interim.csv'
area_agg.data.to_csv(str(export_path))