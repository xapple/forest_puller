#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Special variables #
__version__ = '1.4.0'

# Built-in modules #
import os, sys

# First party modules #
from autopaths    import Path
from plumbing.git import GitRepo

# Constants #
project_name  = 'forest_puller'
project_url   = 'https://github.com/xapple/forest_puller'
cache_git_url = 'https://github.com/xapple/puller_cache.git'

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
    cache_dir = os.path.expanduser('~/.forest_puller/')

# Guarantee it exists #
cache_dir = GitRepo(cache_dir, empty=True)

# Guarantee it exists #
cache_dir.create_if_not_exists()

# If it's empty: clone it #
if cache_dir.empty:
    print("Cloning forest puller cache repository into '%s'." % cache_dir)
    cache_dir.clone_from(cache_git_url, shell=True)

# If it's not a repository: raise #
if not cache_dir.is_a_repos:
    raise Exception("It appears the cache directory was not cloned successfully.")

# Monkey patch pandas library #
import plumbing.pandas_patching
