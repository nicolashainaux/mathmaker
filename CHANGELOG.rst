Changelog
=========

Unreleased
----------


Version 0.7.18 (2022-09-20)
---------------------------

* Add y2b2 mental calculation level.
* Remove some deprecation warnings in tests.

Version 0.7.17 (2022-09-04)
---------------------------

* Update y1b2 mental calculation level.
* Read metadata from pyproject.toml (not all of them yet, though)
* Update french translation.


Version 0.7.16 (2022-09-04)
---------------------------

* Add "belts" directive.
* Update y2b1 mental calculation level.

Version 0.7.15 (2022-09-01)
---------------------------

* divi_vocabulary questions may now be asked using numbers not divisible by each other (answer is a fraction)
* Add y2b1 mental calculation level.

Version 0.7.14 (2022-09-01)
---------------------------

* Patch version (some more required files included).

Version 0.7.13 (2022-09-01)
---------------------------

* Patch version (some more required files included).

Version 0.7.12 (2022-09-01)
---------------------------

* Patch version (include required files).

Version 0.7.11 (2022-08-29)
---------------------------

* Patch version (fix pyproject.toml contents).

Version 0.7.10 (2022-08-29)
---------------------------

* Make use of siunitx version 2, so far, when siunitx is the default version.
* New option --cotinga-template to create the templates to be used by cotinga.
* New directive: config, to print loaded configuration (loadable as json, if necessary)
* Minor improvements
* Maintenance.
* Do not compile all sheets created during tests to reduce the time spent.
* Rename all mental calculation sheets; organize them in 2 years; provide default titles
* Add --belts option to let the user provide its own belts names (use like this: --belts=/path/to/belts.json; belts.json must redefine some or all of the belts identifiers like in the default settings file mathmaker/settings/defaults/mc_belts.json)

Version 0.7.9 (dev) (2022-02-17)
--------------------------------

* New questions types for mental calculation: read abscissa of a point on an axis; find the missing length of a polygon, knowing its perimeter and other sides; calculate a simple fraction of a simple quantity. multi_direct questions may have 3 factors.
* Update yellow1, yellow2 and orange belts in mental calculation.
* Support python>=3.8 (drop 3.6 support)
* Several minor improvements.
* Bug fixes.

Version 0.7.7 (dev) (2021-09-21)
--------------------------------

* Bug fix.
* Minor modifications to some mental calculation sheets.


Version 0.7.6 (2021-09-20)
--------------------------

* Add mental calculation questions: simple conversions between a fraction and a decimal; additions and subtractions of clock times.
* Bug fixes and upgrade of mental calculation sheets (white1 to yellow).


Version 0.7.5 (2019-04-22)
--------------------------

* Bug fixes and upgrade of mental calculation sheets.


Version 0.7.4 (2018-10-20)
---------------------------------

* Add mental calculation sheets for fifth level ("yellow belt, 2d stripe")
* Add mental calculation sheets for sixth level ("orange belt")
* Automatically adapt LaTeX preamble, depending on packages really required to compile the document
* mathmaker project moves to gitlab.com

Version 0.7.3 (2018-01-15)
--------------------------

* Add mental calculation sheets for fourth level ("yellow belt, 1st stripe")

Version 0.7.2 (2017-10-18)
--------------------------

* Add mental calculation sheets for third level ("yellow belt")
* The mental calculation pdf may now be "interactive" (answers can be written in text fields, they can be validated pushing a button; this validation is done by some javascript)
* The daemon now accepts an optional argument in the request (written right after sheet's name, separated with a '|'. Only interactive is allowed, so far)

Version 0.7.1-3 (2017-08-30)
----------------------------

* Patch the daemon to let it accept the new YAML sheet names.
* The output dir will always be in user's home.
* Fix several bugs.

Version 0.7.1 (2017-08-29)
--------------------------

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

Version 0.7.0-6 (2016-08-19)
----------------------------

* Added a setting to let the user change mathmaker's path (to be used by the daemon)
* Bugfix [0.7.0-5 (2016-08-19)]
* If an IP address is passed as parameter to mathmaker's daemon, it will return a 429 http status code (too many requests) if the last request from the same address is not older than 10 seconds. [0.7.0-4 (2016-08-19)]
* Fixed the install of locale files and font listing file [0.7.0-3 (2016-07-18)]

Version 0.7 (2016-07-15)
------------------------

* Standardized structure (``mathmaker`` becomes pip3-installable, available on PyPI and github; its documentation is hosted on readthedocs; tests are made with py.test)
* A daemon is added (``mathmakerd``) to provide communication with ``mathmaker`` through http connections.
* A bunch of mental calculation sheets
* The use of XML frameworks for the sheets (yet only for mental calculation, so far)
