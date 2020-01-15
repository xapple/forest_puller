#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.ipcc.country import all_countries
    >>> for country in tqdm(all_countries): country.uncompress()
"""

# Built-in modules #
import re

# Internal modules #
from forest_puller.ipcc.year import Year
from forest_puller.ipcc.zip_files import all_zip_files
from forest_puller import cache_dir, module_dir

# First party modules #
from autopaths import Path
from plumbing.cache import property_cached

# Third party modules #
from tqdm import tqdm
import pandas

# Load country codes #
country_codes = module_dir + 'extra_data/country_codes.csv'
country_codes = pandas.read_csv(str(country_codes))

###############################################################################
class Country:
    """
    Represents one country's dataset.
    Contains many Year objects.
    Each Year contains one excel file.
    """

    def __init__(self, zip_dir, xls_cache_dir):
        # Main directory #
        self.zip_dir = Path(zip_dir)
        # Record where the cache will be located on disk #
        self.cache_dir = xls_cache_dir
        # The reference ISO2 code #
        self.iso2_code = self.zip_dir.name

    def __repr__(self):
        return '%s object code "%s"' % (self.__class__, self.iso2_code)

    # Convenience shortcut to self.all_years #
    def __getitem__(self, key): return self.all_years[key]
    def __iter__(self):         return iter(self.all_years)
    def __len__(self):          return len(self.all_years)

    # ---------------------------- Properties --------------------------------#
    @property_cached
    def zip_files(self):
        """Return a list of all zip files present for this country."""
        return self.zip_dir.flat_files

    @property_cached
    def zip_file(self):
        """
        Return only the single zip that we are interested in for this country.
        If there are several zip files available, we pick the one that matches
        the country's ISO3 code.
        For instance, in this study, we don't want to include large areas such
        as greenland when considering Denmark, nor French islands etc.
        """
        # Standard case #
        if len(self.zip_files) == 0: return self.zip_files[0]
        # How to parse the ISO3 code from the filename #
        def find_iso3_code(zip_file):
            matches = re.findall("^([a-z]+)-[0-9]+", zip_file.name)
            if not matches: return None
            return matches[0]
        # Case with multiple choices #
        for z in self.zip_files:
            if find_iso3_code(z).upper() == self.iso3_code: return z

    @property_cached
    def iso3_code(self):
        """Get the ISO3 code for this country."""
        # Find the right row #
        row = country_codes.loc[country_codes['iso2_code'] == self.iso2_code].iloc[0]
        # Get the ISO3 #
        return row['iso3_code']

    @property_cached
    def xls_dir(self):
        """Determine where to store all the xls files for this country."""
        return self.cache_dir + self.iso2_code + '/'

    @property_cached
    def all_xls_files(self):
        """For each country we have N excel files, one for each year."""
        return [f for f in self.xls_dir.flat_files if f.extension == '.xlsx']

    @property_cached
    def all_years(self):
        """Every file holds data for a specific year."""
        return [Year(self, xls) for xls in self.all_xls_files]

    @property_cached
    def years(self):
        """A dictionary of every year for which we have data."""
        return {y.year: y for y in self.all_years}

    # ------------------------------ Convenience ---------------------------------#
    @property
    def first_year(self):
        """The earliest year for which we have data."""
        return self.all_years[0]

    @property
    def last_year(self):
        """The latest year for which we have data."""
        return self.all_years[-1]

    # ------------------------------ Methods ---------------------------------#
    def uncompress(self):
        """Uncompress the zip file contents to its own directory."""
        # Remove and regenerate #
        self.xls_dir.remove()
        self.zip_file.unzip_to(self.xls_dir, single=False)
        # Sometimes randomly the zip contains a directory so we have to unnest #
        all_dirs  = self.xls_dir.flat_directories
        all_files = self.xls_dir.flat_files
        if len(all_dirs) == 1 and len(all_files) == 0:
            nested_dir = all_dirs[0]
            nested_dir.unnest()

###############################################################################
# All directories with zip_files
all_dirs = all_zip_files.cache_dir.flat_directories

# Warning #
if len(all_dirs) == 0:
    import warnings
    message = ("\n\n The directory that stores the downloaded zip files ('%s')"
               "\nwas empty, and hence no country has been created. Check you have"
               "\ndownloaded the files and properly set the cache directory path.\n")
    warnings.warn(message % all_zip_files.cache_dir)

# Create every country object #
path          = cache_dir + 'ipcc/xls/'
all_countries = [Country(d, path) for d in all_dirs]
countries     = {c.iso2_code: c for c in all_countries}
