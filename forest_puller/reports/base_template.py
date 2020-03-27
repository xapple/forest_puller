#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Written by Lucas Sinclair and Paul Rougieux.

JRC Biomass Project.
Unit D1 Bioeconomy.
"""

# Built-in modules #
import socket

# Internal modules #
import forest_puller

# First party modules #
from pymarktex.templates import Template
from plumbing.common     import pretty_now

###############################################################################
class ReportTemplate(Template):
    """Things that are common to most reports in forest_puller."""

    # Process info #
    def project_name(self):      return forest_puller.project_name
    def project_url(self):       return forest_puller.project_url
    def project_version(self):   return forest_puller.__version__
    def now(self):               return pretty_now()
    def hostname(self):          return socket.gethostname()
    def git(self):
        if not forest_puller.git_repo: return False
        return {'git_hash'  : forest_puller.git_repo.hash,
                'git_tag'   : forest_puller.git_repo.tag,
                'git_branch': forest_puller.git_repo.branch}
