#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.hpffre.zip_file import zip_file
    >>> print(zip_file.cache_is_valid)

To re-download the files you can do:

    >>> from forest_puller.hpffre.zip_file import zip_file
    >>> zip_file.refresh_cache()

To see the large data frame you can do:

    >>> from forest_puller.hpffre.zip_file import zip_file
    >>> print(zip_file.df)
"""

# Built-in modules #
import zipfile, io

# Internal modules #
from forest_puller import cache_dir
from forest_puller.common import country_codes

# First party modules #
from plumbing.cache import property_cached
from plumbing.scraping import download_from_url

# Third party modules #
import pandas

###############################################################################
class ZipFile:
    """
    Download the zipped CSV file containing all countries and all projections
     from the datadryad webserver.

    This data is acquired by picking the "Download dataset" option from the
    page's sidebar at this address:

    * https://doi.org/10.5061/dryad.4t880qh

    The final file structure will look like this:

        /puller_cache/hpffre/zip/:
        300K Jan 12 18:15 forestry_all_data_norm.zip
    """

    url = "https://datadryad.org/stash/downloads/download_resource/29290"
    zip_name = "efdm_23_countries_data.zip"
    csv_name = "dataset.csv"

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
                          uncompress = False)

    # ---------------------------- Properties --------------------------------#
    @property_cached
    def raw_csv(self):
        """Loads the big CSV that's inside the ZIP into memory."""
        # Load the archive #
        zip_archive = zipfile.ZipFile(self.zip_path)
        # Load the CSV #
        with zip_archive.open(self.csv_name) as csv_handle:
            text_mode = io.TextIOWrapper(csv_handle)
            df = pandas.read_csv(text_mode)
        # Return #
        return df

    @property_cached
    def df(self):
        """Format and filter the data frame and store it in cache."""
        # Load the data frame #
        df = self.raw_csv.copy()
        # Lower case column titles #
        df.columns = map(str.lower, df.columns)
        # Wrong name for several countries #
        df['country'] = df['country'].replace({'Czech': 'Czech Republic'})
        df['country'] = df['country'].replace({'UK': 'United Kingdom'})
        # Use country short codes instead of long names #
        name_to_iso_code = dict(zip(country_codes['country'], country_codes['iso2_code']))
        df['country'] = df['country'].replace(name_to_iso_code)
        # Return #
        return df

###############################################################################
# Create a singleton #
zip_file = ZipFile(cache_dir + 'hpffre/zip/')