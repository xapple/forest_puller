#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.faostat.zip_file import zip_file
    >>> print(zip_file.cache_is_valid)

To re-download the files you can do:

    >>> from forest_puller.faostat.zip_file import zip_file
    >>> zip_file.refresh_cache()

To see the large data frame you can do:

    >>> from forest_puller.faostat.zip_file import zip_file
    >>> print(zip_file.df)
"""

# Built-in modules #
import zipfile, io

# Internal modules #
from forest_puller import cache_dir, module_dir

# First party modules #
from plumbing.cache import property_cached
from plumbing.scraping import download_from_url

# Third party modules #
import pandas

# Load country codes #
country_codes = module_dir + 'extra_data/country_codes.csv'
country_codes = pandas.read_csv(str(country_codes))

###############################################################################
class ZipFile:
    """
    Download the zipped CSV file containing all countries and all products from
    the FAOSTAT webserver (for the forestry category).

    This data is acquired by picking the "All Data Normalized" option from the
    "Bulk download" sidebar at this address:

    * http://www.fao.org/faostat/en/#data/FO

    The final file structure will look like this:

        /puller_cache/faostat/zip/:
        16M Jan 12 18:15 aut-2019-crf-15apr19.zip
    """

    url = "http://fenixservices.fao.org/faostat/static/bulkdownloads/Forestry_E_All_Data_(Normalized).zip"
    csv_name = "Forestry_E_All_Data_(Normalized).csv"
    encoding = "ISO-8859-1"

    def __init__(self, zip_cache_dir):
        # Record where the cache will be located on disk #
        self.cache_dir = zip_cache_dir
        # Where the file should be downloaded to #
        self.zip_path = self.cache_dir + 'forestry_all_data_norm.zip'

    @property
    def cache_is_valid(self):
        """Checks if the file needed has been correctly downloaded."""
        return True

    def refresh_cache(self):
        """Will download the required zip files to the cache directory."""
        download_from_url(self.url,
                          self.zip_path,
                          stream     = True,
                          progress   = True,
                          uncompress = False)

    # ---------------------------- Properties --------------------------------#
    @property_cached
    def raw_csv(self):
        """Loads the big CSV that's inside the ZIP into memory."""
        # Load the archive #
        zip_archive = zipfile.ZipFile(self.zip_path)
        # Load the CSV #
        with zip_archive.open(self.csv_name) as csv_handle:
            text_mode = io.TextIOWrapper(csv_handle, encoding=self.encoding)
            df = pandas.read_csv(text_mode)
        # Return #
        return df

    @property_cached
    def df(self):
        """Format and filter the data frame and store it in cache."""
        # Load the data frame #
        df = self.raw_csv.copy()
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

###############################################################################
# Create a singleton #
zip_file = ZipFile(cache_dir + 'faostat/zip/')