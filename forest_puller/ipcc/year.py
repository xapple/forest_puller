#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #
import re

# Internal modules #

# First party modules #

# Third party modules #

###############################################################################
class Year:
    """
    Represents a specific year from a specific country's dataset.
    """

    def __init__(self, country, xls_file):
        # The parent country #
        self.country = country
        # THe file that contains data for this year #
        self.xls_file = xls_file
        # The year itself from the file name #
        self.year = int(re.findall("^[A-Z]+_[0-9]+_([0-9]+)", xls_file.name)[0])