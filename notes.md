# Done for every excel file:

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

# TODO

* Check the tutorial works on a fresh Ubuntu

* Add new data source: Forest Europe

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
