#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC biomass Project.
Unit D1 Bioeconomy.
"""

# Special variables #
__version__ = '1.0.0'

# Built-in modules #
import os, sys

# First party modules #
from autopaths    import Path
from plumbing.git import GitRepo

# Constants #
project_name = 'forest_puller'
project_url  = 'https://gitlab.com/bioeconomy/puller/forest_puller'

# Get paths to module #
self       = sys.modules[__name__]
module_dir = Path(os.path.dirname(self.__file__))

# The repository directory #
repos_dir = module_dir.directory

# The module is maybe in a git repository #
git_repo = GitRepo(repos_dir, empty=True)

# Determine where to cache things #
env_var_name = "FOREST_PULLER_CACHE"

# If it is specified by user #
if env_var_name in os.environ:
    cache_dir = os.environ[env_var_name]
    if not cache_dir.endswith('/'): cache_dir += '/'

# If it is not specified by user #
else:
    import tempfile
    cache_dir = tempfile.gettempdir() + '/forest_puller/'
    import warnings
    message = ("\n\n The cache location for forest puller's data is not defined in"
               " the '%s' environment variable.\n In this case it will default"
               " to:\n\n '%s',\n which might lead to re-caching after every startup.\n")
    warnings.warn(message % (env_var_name, cache_dir))

# Guarantee it exists #
cache_dir = Path(cache_dir)
cache_dir.create_if_not_exists()
