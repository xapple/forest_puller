#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #
import os, inspect

# Internal modules #
from pymarktex.templates import Template

# First party modules #
from autopaths import Path

# Get current directory #
file_name = os.path.abspath((inspect.stack()[0])[1])
this_dir  = Path(os.path.dirname(os.path.abspath(file_name)) + '/')

###############################################################################
class Header(Template):
    """All the parameters to be rendered in the LaTeX header template"""
    def image_path(self): return (this_dir + 'logo.png').unix_style

###############################################################################
class Footer(Template):
    """All the parameters to be rendered in the LaTeX footer template"""
    pass