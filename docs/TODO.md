# TODO

## Important

### Data mapping
* Interpolation method as described by Raimer et al. required (see p.212)
    * Method is based on FEM shape functions

* Add methods to map loads onto a FEM mesh (see Raimer et al.)

* Methods for merging load and deformations fields (How does this affect the mapping methods?)

* Plot load and deformation fields

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
