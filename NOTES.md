# Done for the project:

* Fix detection of last line

* Decide which ISO3 code
    - DK, take "DNK".
    - BG, take "GBR".
    - FR, take "FRA".

* Fix repetition in `land_use` and `subdivision`

* Row headers, make them all readable

* Convert all units

* Specific NaNs with all combination of identifiers.

* Recompute the line 10 (total) as a sanity check

* Check there are only `float64` columns directly in the package

* Rewrite the sanity check

* Pickle the final df in the cache repository

* Update repositories on gitlab (logos, public)

* Publish also on github

* Rewrite the sample test

* Rewrite the indexed dataframe

* Write the documentation

* Debug the problem with the sanity check

* Add README in puller_cache

* Auto-clone the cache repository on install

* Check the tutorial works on a fresh Ubuntu

* Add new data source: Forest Europe

* Rename columns to short name for soef

* Convert units for soef

* Create pickled df for soef

* Created a large concatenated df for soef

* Write doc for the new data source

* Add data source: faostat (the flag file with all products)

* Add data source: diabolo

* Check conversion factor for hpffre

* Drop a mail for the extra C++ model

* Check that the FRA faostat matches the classical faostat data for area

* Add data source: faostat forest area

* Refactor: Centralize the import of "country_codes" to one file

* Make area compare visualizations

* Reverse the HPFFRE line

* Make PDF with figure legend

* For each source a separate plot of increment and fellings in unit/ha on total forest area if available otherwise on forest area available for wood supply. 


# TODO

* Make comparison of net loss/gains between different data sources (convert the m^3 into net CO2 emission in tons for faostat and ipcc)

  - for all source on one plot, using a conversion factor from m3 to tons of carbon plot increment 
  - for all source on one plot, using a conversion factor from m3 to tons of carbon plot fellings 
  - for all source on one plot, using a conversion factor from m3 to CO2 plot net emissions 
  
* Add Malta and Cyprus to countries available

* Write up introduction and methods

* Make a total of all EU countries 


# Ideas

Example variable descriptions:

    no |  variable |    name_in_ipcc | name_in_faostat | si_unit
    --------------------------------------------------------------------
     1 |      area |     forest area |   area_forested | hectare
     2 | emissions | total emissions |             NaN | tons of carbon


# Obtaining the cache

There are several ways the end-users can get a copy of the cached data upon installation or first use:

- Add to the source code repository directly
- Add to source tarball and upload on pypi with python package
- (+) Clone to `tempfile.gettempdir()`
- Clone to `~/.forest_puller`
- Clone to `__module_dir__` but permission problem if not `--user`
- (+) Force or suggest the setting of `$FOREST_PULLER_CACHE_DIR` environment variable
- Have it download every time to RAM on each python process
- Prompt the user with `input()` to specify a dir and save to a dotfile
- Split up sources into different `puller_cache` repositories
