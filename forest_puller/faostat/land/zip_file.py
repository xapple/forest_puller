#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.faostat.land.zip_file import zip_file
    >>> print(zip_file.cache_is_valid)

To re-download the files you can do:

    >>> from forest_puller.faostat.land.zip_file import zip_file
    >>> zip_file.refresh_cache()

To see the large data frame you can do:

    >>> from forest_puller.faostat.land.zip_file import zip_file
    >>> print(zip_file.df)
"""

# Built-in modules #
import zipfile, io

# Internal modules #
from forest_puller import cache_dir
from forest_puller.faostat import fix_faostat_tables
from forest_puller.common import country_codes

# First party modules #
from plumbing.cache import property_cached
from plumbing.scraping import download_from_url

# Third party modules #
import pandas

###############################################################################
class ZipFile:
    """
    Download the zipped CSV file containing all countries for "forest land" from
    the FAOSTAT webserver.

    This data is acquired by picking the "All Data Normalized" option from the
    "Bulk download" sidebar at this address:

    * http://www.fao.org/faostat/en/#data/GF

    The final file structure will look like this:

        /puller_cache/faostat/zips/:
        400K Jan 12 18:15 land_all_data_norm.zip
    """

    url = "http://fenixservices.fao.org/faostat/static/bulkdownloads/Emissions_Land_Use_Forest_Land_E_All_Data_(Normalized).zip"
    csv_name = "Emissions_Land_Use_Forest_Land_E_All_Data_(Normalized).csv"
    encoding = "ISO-8859-1"

    def __init__(self, zip_cache_dir):
        # Record where the cache will be located on disk #
        self.cache_dir = zip_cache_dir
        # Where the file should be downloaded to #
        self.zip_path = self.cache_dir + 'land_all_data_norm.zip'

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
        # Fix the data frame #
        df = fix_faostat_tables(self.raw_csv)
        # Fix the units (hecatres) #
        selector = df['unit']     == '1000 ha'
        df.loc[selector, 'unit']   = 'hectares'
        df.loc[selector, 'value'] *= 1000
        # Fix the units (gigagrams) #
        selector = df['unit']     == 'gigagrams'
        df.loc[selector, 'unit']   = 'kg'
        df.loc[selector, 'value'] *= 1000000
        # Return #
        return df

###############################################################################
# Create a singleton #
zip_file = ZipFile(cache_dir + 'faostat/zips/')