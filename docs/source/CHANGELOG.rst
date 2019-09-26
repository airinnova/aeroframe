Changelog
=========

Changelog for FramAT. Version numbers try to follow `Semantic
Versioning <https://semver.org/spec/v2.0.0.html>`__.

[0.1.1] -- 2019-09-26
---------------------

Added
~~~~~

Added package `aeroframe.plot` which provides tools to plot load and deformation fields

[0.1.0] -- 2019-09-25
---------------------

Added
-----

* Added module `aeroframe.data.shared` for load and deformation field sharing

* Added module `aeroframe.fileio.serialise` for serialisation of field data

* Added module `aeroframe.templates.wrappers` which contains template wrapper
  classes for the CFD and the structure. The template wrappers can be sub-classed.

* Added wrappers for *PyTornado* and *FramAT* and working examples (based on [Dett19]_)

Changed
-------

* Exchange of load and deformation data takes place in memory rather than trough
  file operations. Load and deformation fields are exchanged through a shared
  data class. An instance of this shared data class is passed to the CFD and to
  the structure wrapper.

        * It is generally more efficient to forward data in memory. This makes
          data exchange particularly convenient for CFD and structure tools
          which provide a Python API. However, wrappers can always deserialise
          from a file to the required Python load and data fields.

* Convergence criterion is now based on the absolute difference (not relative)
  difference between the last two solutions (same as in [WGJZ18]_)

[0.0.1] -- 2019-09-17
---------------------

* First public release of `AeroFrame` (Aeroelastic Framework)
