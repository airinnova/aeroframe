.. _sec_conventions:

Conventions
===========

|name| itself does not perform any aerodynamics or structure analyses. It merely exchanges data and coordinates the CFD_ and structure solvers. A correct holistic aeroelasticity model can only be achieved if the CFD_ and structure wrappers comply with certain conventions. If different modules are to used truly modular (i.e. fully interchangeable) it is very important that the wrappers expose the same interface and provide data in a consistent format. This page gives informations on important conventions in |name|.

TODO
