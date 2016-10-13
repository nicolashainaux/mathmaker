Changelog
=========

New in version 0.7.1dev2 (2016-10-13)
-------------------------------------

* New sheets:
  - expansion of simple brackets (declined in two versions)
  - clever multiplications (mental calculation)
  - intercept theorem: write the correct quotients' equalities
  - intercept theorem: solve simple exercises

These sheets and all future sheets will be defined in xml files.

New in version 0.7.1dev1 (2016-09-14)
-------------------------------------

* A new sheet (declined in two versions): expansion of double brackets. Defined in an xml sheet as for mental calculation sheets.

New in version 0.7.0-6 (2016-08-19)
-----------------------------------

* Added a setting to let the user change mathmaker's path (to be used by the daemon)

New in version 0.7.0-5 (2016-08-19)
-----------------------------------

* Bugfix

New in version 0.7.0-4 (2016-08-19)
-----------------------------------

* If an IP address is passed as parameter to mathmaker's daemon, it will return a 429 http status code (too many requests) if the last request from the same address is not older than 10 seconds.

New in version 0.7.0-3 (2016-07-18)
-----------------------------------

* Fixed the install of locale files and font listing file

New in version 0.7 (2016-07-15)
-------------------------------

* Standardized structure (``mathmaker`` becomes pip3-installable, available on PyPI and github; its documentation is hosted on readthedocs; tests are made with py.test)

* A daemon is added (``mathmakerd``) to provide communication with ``mathmaker`` through http connections.

* A bunch of mental calculation sheets

* The use of XML frameworks for the sheets (yet only for mental calculation, so far)
