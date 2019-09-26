# TODO

## Important

### Data mapping
* Interpolation method as described by Raimer et al. required (see p.212)
    * Method is based on FEM shape functions

* Add methods to map loads onto a FEM mesh (see Raimer et al.)

* Methods for merging load and deformations fields (How does this affect the mapping methods?)

### Plotting
* Plot load and deformation fields
* Plot load and deformation VECTORS!
* Plot deformed undeformed mesh data

### Data sharing
* Loads may have to be applied to structure model in *undeformed* state (e.g. lin. Euler-Bernoulli beam)
    * Save undeformed points of attack?
    * Or use deformation field to compute backwards where undeformed points of attack were if required
    * Perhaps, there should be a flag indicating if points of attack are from deformed or undeformed state

## Save AeroFrame results
* Option in settings file to save load and deformations fields (serialise as JSON?)
* Can then be used for plotting

## Add 'conventions' module
* Module which lists general conventions...? (useful?)
    * Component uid which ends with "_m" is a mirrored component...

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
