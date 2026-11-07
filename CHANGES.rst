1.3.0 (unreleased)
------------------

General
^^^^^^^

- The minimum required Python is now 3.12. [#74]

- The C extension is now built with ``extension-helpers``, and
  ``setup.py`` was removed. [#78]

New Features
^^^^^^^^^^^^

- Added support for free-threaded Python builds. The C extension can
  now be called concurrently from multiple threads without the GIL.
  [#78]

Bug Fixes
^^^^^^^^^

- Fixed a use-after-free memory bug in the C extension, which released
  the converted input and output arrays before using their data. [#78]

API Changes
^^^^^^^^^^^


1.2.0 (2026-01-20)
------------------

- The minimum required Python is now 3.11. [#51]

- The minimum required NumPy is now 2.0. [#51]


1.1.0 (2024-04-17)
------------------

- Added support for NumPy 2.0. [#22]


1.0.1 (2023-11-16)
------------------

- Added Zenodo badge.


1.0.0 (2023-11-06)
------------------

- Initial release.


0.1a (2023-08-02)
-----------------

- Initial alpha release.
