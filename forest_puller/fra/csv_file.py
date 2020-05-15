#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class like this:

    >>> from forest_puller.fra.csv_file import forest_chars
    >>> print(forest_chars.raw_csv)
"""

# Built-in modules #

# Internal modules #
from forest_puller import cache_dir
from forest_puller.common import country_codes

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
import pandas

###############################################################################
class CSVFile:
    """
    The original link is http://www.fao.org/forest-resources-assessment/en/
    """

    # Params #
    conv_fact = None

    def __init__(self, zip_cache_dir):
        # Record where the cache will be located on disk #
        self.cache_dir = zip_cache_dir
        # Where the file should be downloaded to #
        self.csv_path = self.cache_dir + self.filename

    # ---------------------------- Properties --------------------------------#
    @property_cached
    def raw_csv(self):
        """Load the big CSV into memory."""
        # Load the CSV #
        df = pandas.read_csv(str(self.csv_path), encoding="ISO-8859-1")
        # Return #
        return df

    @property_cached
    def df(self):
        """Format and filter the data frame and store it in cache."""
        # Load the data frame #
        df = self.raw_csv.copy()
        # Lower case column titles #
        df.columns = map(str.lower, df.columns)
        # Drop some columns #
        df = df.drop(columns=['country (code)'])
        df = df.drop(columns=['fra categories (code)'])
        # Rename some columns #
        df = df.rename(columns={'fra categories': 'category'})
        df = df.rename(columns={'forest/other wooded land': 'land_type'})
        # Wrong name for one country "Czech Republic" #
        df['country'] = df['country'].replace({'Czech Republic': 'Czechia'})
        # Use country short codes instead of long names #
        name_to_iso_code = country_codes['country'], country_codes['iso2_code']
        name_to_iso_code = dict(zip(*name_to_iso_code))
        df['country']    = df['country'].replace(name_to_iso_code)
        # Drop the flag #
        if df['flag'].isnull().all(): df = df.drop(columns=['flag'])
        # Optionally drop other stuff #
        if 'forest/other wooded land (code)' in df.columns:
            df = df.drop(columns=['forest/other wooded land (code)'])
        # Rename some category values #
        df['category'].replace({'Dead wood': 'Dead wood biomass'})
        df['category'].replace({'Commercial': 'Commercial growing stock'})
        # Fix horrendous spelling mistake #
        before = 'Other nataturally regenerated forest'
        after  = 'Other naturally regenerated forest'
        df['category'].replace({before: after})
        # Use the conversion factor for different units #
        if self.conv_fact is not None: df['value'] *= self.conv_fact
        # Return #
        return df

###############################################################################
class ForestChars(CSVFile):
    """
    ['Planted forest' 'Primary forest' 'Other naturally regenerated forest']
    """
    name      = "forest_chars"
    title     = "Forest characteristics (1 000 ha) by FRA categories"
    filename  = "T04FO000.csv"
    url       = "http://countrystat.org/home.aspx?c=FOR&tr=1"
    conv_fact = 1000

class ForestExtent(CSVFile):
    """
    ['Other wooded land' 'Inland water' 'Forest' 'Other land']
    """
    name      = "forest_extent"
    title     = "Extent of forest and other wooded land (1 000 ha)"
    filename  = "T01FO000.csv"
    url       = "http://countrystat.org/home.aspx?c=FOR&tr=1"
    conv_fact = 1000

class ForestEstabl(CSVFile):
    """
    ['Reforestation' 'Natural expansion of forest' 'Afforestation']
    """
    name     = "forest_establ"
    title    = "Forest establishment total (ha/yr) by FRA categories"
    filename = "T05FO000.csv"
    url      = "http://countrystat.org/home.aspx?c=FOR&tr=3"

class GrowingStock(CSVFile):
    """
    * ['Total growing stock' 'Commercial']
    * ['Other wooded land' 'Forest']
    """
    name      = "growing_stock"
    title     = "Growing stock (Million m3 over bark) by Forest/Other wooded land"
    filename  = "T06FO000.csv"
    url       = "http://countrystat.org/home.aspx?c=FOR&tr=4"
    conv_fact = 1e6

class CarbonStock(CSVFile):
    """
    * ['Soil carbon' 'Carbon in living biomass' 'Carbon in litter'
       'Carbon in dead wood' 'Carbon in below-ground biomass'
       'Carbon in above-ground biomass']
    * ['Other wooded land' 'Forest']
    """
    name      = "carbon_stock"
    title     = "Carbon stock (Million metric tonnes) by Forest/Other wooded land"
    filename  = "T08FO000.csv"
    url       = "http://countrystat.org/home.aspx?c=FOR&tr=4"
    conv_fact = 1e6

class BiomassStock(CSVFile):
    """
    * ['Above-ground biomass' 'Below-ground biomass' 'Dead wood']
    * ['Forest' 'Other wooded land']
    """
    name      = "biomass_stock"
    title     = "Biomass stock (Million metric tonnes) by Forest/Other wooded land"
    filename  = "T07FO000.csv"
    url       = "http://countrystat.org/home.aspx?c=FOR&tr=4"
    conv_fact = 1e6

###############################################################################
# Choose the cache location #
fra_csv_dir = cache_dir + 'fra/csv/'

# Create the singletons #
forest_chars  = ForestChars(fra_csv_dir)
forest_extent = ForestExtent(fra_csv_dir)
forest_establ = ForestEstabl(fra_csv_dir)
growing_stock = GrowingStock(fra_csv_dir)
carbon_stock  = CarbonStock(fra_csv_dir)
biomass_stock = BiomassStock(fra_csv_dir)
