#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.

Typically you can use this class this like:

    >>> from forest_puller.ipcc.crf import dataset as crf
    >>> print(crf.df)
"""

# Built-in modules #

# Internal modules #
from forest_puller import cache_dir
from forest_puller import module_dir
from forest_puller.ipcc.downloads import downloads

# First party modules #
from plumbing.cache import property_cached

# Third party modules #
from tqdm import tqdm
import pandas

# Load IPCC column name mapping to short names #
col_name_map = module_dir + 'variable_mapping/ipcc_columns.csv'
col_name_map = pandas.read_csv(str(col_name_map))

###############################################################################
class IPCC_CRF:
    """
    For every country: download the Common Reporting Format (CRF) file from the
    IPCC website. Then parse table no. 4 of every year.
    See the `DownloadsIPCC` class for more information on the provenance of the
    data.
    """

    def __init__(self, crf_cache_dir):
        # Record where the cache will be located on disk #
        self.cache_dir = crf_cache_dir

    # ---------------------------- Properties --------------------------------#
    @property_cached
    def df(self):
        """
        The data frame containing all the parsed data.
        Columns are: [...]
        """
        # Check if files downloaded #
        if not self.cache_is_valid: self.refresh_cache()
        # Parse #
        pass
        # Return #
        return

    @property
    def cache_is_valid(self):
        """Checks if every file needed has been correctly downloaded."""
        return False

    # ------------------------------ Methods ---------------------------------#
    def refresh_cache(self):
        """Will download all the required zip files to the cache directory."""
        for i, row in tqdm(downloads.df.iterrows()):
            print(row['zip'])

    def parse_table_4(self, excel_file_path):
        """Extract information from table 4 into a pandas data frame."""
        # Parameters for the position of rows used for the header
        # zero-index (offset of one compared to the excel row numbers)
        begin_head = 4
        end_head   = 9
        # Load table into pandas
        table4 = pandas.read_excel(excel_file_path,
                                   sheet_name = 'Table4.A',
                                   header     = None,
                                   na_values  = ['IE','NE','NO','NO,NE'])
        # Extract headers
        header = table4.iloc[begin_head:end_head]
        header = header.fillna(method='ffill')
        header = header.reset_index(drop=True)
        # Add information on per area columns in t C /ha
        # so they have different name than the kt C columns
        header.iloc[3,5:12] = header.iloc[3,5:12] + '_per_area'
        # Convert to short headers
        # Check column names for the reason why this doesn't work properly
        header = header.iloc[3].replace(list(col_name_map['ipcc']),
                                        list(col_name_map['forest_puller']))
        # Extract table body
        # Look for the position of the first mostly empty row
        # at the end of the table in order to remove all links after that
        selector = table4.isnull().sum(axis=1) > 18
        selector[0:end_head] = False
        selector = selector.cumsum() == 0
        last_row = max(selector.index[selector])
        df       = table4.iloc[end_head+1:last_row+1]
        # Rename columns #
        df.columns = header
        # Return #
        return df

###############################################################################
# Create a singleton #
dataset = IPCC_CRF(cache_dir + 'ipcc/crf/')