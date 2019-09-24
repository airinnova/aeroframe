# TODO

## Important
* Data exchange can be made "in-memory" instead of through files
    * Make `SharedState()` class (contains deformation and loads, etc.)

* Interpolation method as described by Raimer et al. required (see p.212)
    * Method is based on FEM shape functions

## Testing
* ...

## Documentation
* ...

## Ideas
* Use a "master model" class for geometry?
* Aeroelastic sizing loop? Similar to Seywald

## Obtaining input data
* How can equivalent beam properties be extracted/derived from CPACS
    * Perhaps "Seywalds flight manoeuvre" sizing loop necessary

## SharedData class
* Currently for beam-like displacement filed (i.e. ux, uy, uz, tx, ty, tz) --> Generalise!

## Long-term
* Add support for dynamic aeroelastic analyses
