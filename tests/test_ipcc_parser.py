# -*- coding: utf-8 -*-



"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.

Test methods parsing data from the IPCC Common Reporting FOrmat (CRF) tables.
"""

# Expected data #
dm = string_to_df("""           | merch | prod_irw |
                      merch     | 0.7   | 0.3      |
                      prod_irw  | 0     | 1        | """)


###############################################################################
def test_parse_austria_2000():
    """
    Load IPCC CRF data for austria
    """
    ipcc_crf.download
