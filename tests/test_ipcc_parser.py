# -*- coding: utf-8 -*-



"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Test methods parsing data from the IPCC Common Reporting FOrmat (CRF) table 4.
"""
# First party modules #
from plumbing.dataframes import string_to_df

# Expected data #
crf = string_to_df("""protection_status | area  | gain | loss | stock_change|
                      merch             | 0.7   | 0.3  | 0.3  | 0.3         |
                      prod_irw          | 0     | 1    | 0.3  | 0.3         |""")


###############################################################################
def test_parse_austria_2000():
    """
    Load IPCC CRF data for austria
    """
    ipcc_crf.download
