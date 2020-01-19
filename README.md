[![PyPI version](https://badge.fury.io/py/forest_puller.svg)](https://badge.fury.io/py/forest_puller)
[![GitHub last commit](https://img.shields.io/github/last-commit/xapple/forest_puller.svg)](https://github.com/xapple/forest_puller/commits/master)
[![GitHub](https://img.shields.io/github/license/xapple/forest_puller.svg)](https://github.com/xapple/forest_puller/blob/master/LICENSE)

# `forest_puller` version 1.0.2

`forest_puller` is a package for retrieving data concerning forests on the European continent. This includes forest growth rates, amount of forested areas and forest inventory (standing stock).

There are several public data sources that are accessible online to retrive this type of information. This package will automate the process of scrapping these website and parsing the resulting excel files.

Once `forest_puller` is installed you can easily access forest data through standard pandas data frames.

## Installing

`forest_puller` is a python package and so is compatible with all operating systems, Linux, macOS and Windows. Once python 3 is installed on your computer, if it is not already, simply type the following on your terminal:

    $ pip3 install forest_puller

## Usage

For instance to retrieve the net carbon emission of austria in 2007 you could do the following:

    # Import #
    from forest_puller.ipcc.country import countries
    # Get the country #
    austria = countries['AT']
    # Get the year #
    at_2017 = austria.years[2017]
    # Print some data #

## Data sources

### IPCC

To download the forest data from the IPCC you would have to ...

### More sources to be added in the future

Stay tuned.
