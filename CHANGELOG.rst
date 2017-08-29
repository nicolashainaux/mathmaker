Changelog
=========

New in version 0.7.1-1 (2017-08-29)
-----------------------------------

* Patch the daemon to let it accept the new YAML sheet names.

New in version 0.7.1 (2017-08-29)
---------------------------------

* Support for python3.6 only, drop support for older python versions.
* Mental calculation sheets can now be created as slideshows. Add a default slideshows series for white belt, 1st and 2d stripes.
* Reorganization of mental calculation in belts: White belt, 1st stripe and 2d stripe have been added (including new sheets: addition/subtraction, fraction of a rectangle, complements)
* New sheet: order of precedence in operations.
* YAML files will be used to store sheets. The previous ways (XML and Python) will be dropped.
* Huge reorganization of the lib/ source code.
* Fair bunch of bug fixes.
* Issue warnings instead of exceptions when the version of a dependency could not be determined. [0.7.1dev5 (2017-05-04)]
* New sheets about trigonometry: [0.7.1dev4 (2017-05-03)]

  - vocabulary in the right triangle
  - write the correct formulae
  - calculate a length
  - calculate an angle

* New sheets: [0.7.1dev3 (2016-10-21)]

  - intercept theorem: "butterfly" configuration
  - intercept theorem: converse

* New sheets: [0.7.1dev2 (2016-10-13)]

  - expansion of simple brackets (declined in two versions)
  - clever multiplications (mental calculation)
  - intercept theorem: write the correct quotients' equalities
  - intercept theorem: solve simple exercises

* A new sheet (declined in two versions): expansion of double brackets. Defined in an xml sheet as for mental calculation sheets. [0.7.1dev1 (2016-09-14)]

New in version 0.7.0-6 (2016-08-19)
-----------------------------------

* Added a setting to let the user change mathmaker's path (to be used by the daemon)
* Bugfix [0.7.0-5 (2016-08-19)]
* If an IP address is passed as parameter to mathmaker's daemon, it will return a 429 http status code (too many requests) if the last request from the same address is not older than 10 seconds. [0.7.0-4 (2016-08-19)]
* Fixed the install of locale files and font listing file [0.7.0-3 (2016-07-18)]

New in version 0.7 (2016-07-15)
-------------------------------

* Standardized structure (``mathmaker`` becomes pip3-installable, available on PyPI and github; its documentation is hosted on readthedocs; tests are made with py.test)
* A daemon is added (``mathmakerd``) to provide communication with ``mathmaker`` through http connections.
* A bunch of mental calculation sheets
* The use of XML frameworks for the sheets (yet only for mental calculation, so far)
