.. _sec_notes_on_beam_models:

Notes on beam models
====================

**TODO: explain variables**

|name| may be used to couple a so-called VLM_ model (vortex lattice method) and a beam FEM_ model as shown in [Dett19]_. The VLM_ uses a *surface-like* mesh which is made up of quadrilaterals (panels), but the beam FEM_ mesh is *line-like* with discrete nodes. It is obvious that these discretisations do not coincide. A transfer and interpolation of loads and deformations becomes necessary. Since the load mapping from the VLM_ mesh onto the FEM_ beam is fairly illustrative, a few comments will be made here. Note that this page is based on or copied from [Dett19]_ where further information and context can be found.

Comments on beam load mapping schemes
-------------------------------------

When projecting aerodynamic loads onto the FEM_ beam, there are two potentially sensible mapping methods. The first method is to project loads onto the *nearest node or beam element* ([Bouc03]_, [Brau07]_, [RBBW10]_, [Seyw16]_). The second method is to project loads chordwise (stripwise) onto the beam axis (e.g. [Seyw11]_, [BoEl16]_). These two different mapping schemes are illustrated in :numref:`fig_load_mapping_methods`. They are only geometrically equivalent in the case of unswept wings.

.. _fig_load_mapping_methods:
.. figure:: ../_static/images/on_beams/load_mapping_variations.svg
   :width: 800 px
   :alt: Different load mapping methods
   :align: center

   Comparison of load mapping schemes for a swept wing (image from [Dett19]_)

In publications known to the author there is very little or no explanation of why either of these mapping schemes is chosen. Which of the projection methods is more sensible may depend on the real structure and the real load transfer. For instance, the orientation of stiff wing ribs can influence load paths inside the structure and therefore the deformation of the wing [RoWH14]_. A simple beam model as indicated in :numref:`fig_load_mapping_methods` does not have any information about such structural details, and therefore no information of how loads are being transferred. As only the nodal loads matter, one has to make a choice of transferring loads onto the idealised elastic axis. In the following it will be shown that there is no equivalence between the two mentioned mapping methods. In general, work and displacements will differ.

Elastic work
------------

Consider a straight cantilever beam in the global :math:`X`-:math:`Y` plane modelling the structure of a swept wing (:numref:`fig_load_mapping_work`). The beam axis :math:`x` is oriented with an angle :math:`\phi` with respect to the global :math:`Y`-axis. Suppose there is a point force :math:`\mathbf{F}_\text{a} = (0, 0, F)^T` acting at some off-axis point :math:`\mathbf{P}_\text{a}`. As discussed, the force may either be projected onto a point :math:`\mathbf{P}_1` (chordwise projection) or onto a point :math:`\mathbf{P}_2` (nearest element projection).

.. _fig_load_mapping_work:
.. figure:: ../_static/images/on_beams/load_mapping_work.svg
   :width: 400 px
   :alt: Work
   :align: center

   Projection of off-axis loads onto a cantilever beam inclined with respect to the global coordinate system. The global coordinate system (blue axes) and the beam-local coordinate system (green axes) do not coincide. The off-axis loads can be projected onto the beam axis either using a *parallel-to-X* or a *closest-element (closest-node) approach* (image from [Dett19]_).

For the following work consideration, it is convenient to directly express the projected loads in the beam-local coordinate system (axes denoted by lower-case :math:`x`, :math:`y` and :math:`z`). At point :math:`\mathbf{P}_1` the equivalent, projected load is [#]_

.. [#] Notice that :math:`\phi < 0`.

.. math::
    :label: eq_projected_load_P1

    \mathbf{F}_{P_1, \text{loc}} = %%
    \mathbf{F}_\text{a} = %%
    \begin{pmatrix}
        0 \\
        0 \\
        F \\
    \end{pmatrix}
    ~\text{and}\quad %%
    \mathbf{M}_{P_1, \text{loc}} = %%
    %%%%%
    \begin{pmatrix}
        - l_1 \cdot \sin \phi \\
        - l_1 \cdot \cos \phi \\
        0 \\
    \end{pmatrix}
    \times
    \begin{pmatrix}
        0 \\
        0 \\
        F \\
    \end{pmatrix} = %%
    %%%%%
    F l_1
    \begin{pmatrix}
        -\cos \phi \\
        \sin \phi \\
        0 \\
    \end{pmatrix}

At point :math:`\mathbf{P}_2` the equivalent load is

.. math::
    :label: eq_projected_load_P2

    \mathbf{F}_{P_2, \text{loc}} = %%
    \mathbf{F}_\text{a} = %%
    \begin{pmatrix}
        0 \\
        0 \\
        F \\
    \end{pmatrix}
    ~\text{and} \quad
    \mathbf{M}_{P_2, \text{loc}} = %%
    %%%%%
    \begin{pmatrix}
        0 \\
        -l_2 \\
        0 \\
    \end{pmatrix}
    \times
    \begin{pmatrix}
        0 \\
        0 \\
        F \\
    \end{pmatrix} = %%
    %%%%%
    -F l_2
    \begin{pmatrix}
        1 \\
        0 \\
        0 \\
    \end{pmatrix}

Looking at the load components of the projected loads, it is apparent that bending is induced due to a transverse force component :math:`F_{z,\text{proj}} = F` and due to a bending moment :math:`M_{y,\text{proj}}` (:math:`M_{y,\text{proj}}=0` when projecting onto :math:`\mathbf{P}_2`), and twist is induced due to a torsional moment :math:`M_{x,\text{proj}}`. The internal elastic energy due to bending about :math:`y` and torsion (equal to the work done by the external loads) is given as [Sund10]_

.. math::
    :label: eq_work_done

    W = \displaystyle\int_0^{L_2} \left[ \frac{1}{2} \cdot E \cdot I_y \left(\frac{\text{d}{}^2 u_z}{\text{d}{x}^2}\right)^2 + \frac{1}{2} \cdot G \cdot J \left(\frac{\text{d}{\Theta_x}}{\text{d}{x}}\right)^2  \right] \text{d}{x}

where the notation from **TODO** is used, and :math:`L_2` is the beam length. For the sake of keeping the following relations somewhat simpler, the bending stiffness :math:`E \cdot I_y` and the torsional stiffness :math:`G \cdot J` are assumed to be constant. It can be shown that the projected point loads acting at :math:`x = x_\text{i}` will introduce work given by the following expression (c.f. [Sund10]_, [Megs16]_).

.. math::
    :label: eq_work_done_derived

    W &=
    %%%
    \displaystyle\int_0^{L_2} \left( \frac{\widetilde{M}^2_{y}}{2 \cdot E \cdot I_y} + \frac{\widetilde{M}^2_x}{2 \cdot G \cdot J} \right) \text{d}{x} =
    %%%
    \dots \nonumber \\
    %%%
     &= \frac{{M}_{y,\text{proj}}^2 \cdot x_\text{i}}{2 \cdot E \cdot I_y} - \frac{{M}_{y,\text{proj}} \cdot {F}_{z,\text{proj}} \cdot x_\text{i}^2}{2 \cdot E \cdot I_y} + \frac{{F}_{z,\text{proj}}^2 \cdot x_\text{i}^3}{6 \cdot E \cdot I_y} + \frac{{M}_{x,\text{proj}}^2 \cdot x_\text{i}}{2 \cdot G \cdot J}

:math:`\widetilde{M}_y` is the internal bending moment about the :math:`y`-axis and :math:`\widetilde{M}_x` is the internal torsional moment. :math:`F_{z,\text{proj}}`, :math:`M_{x,\text{proj}}` and :math:`M_{y,\text{proj}}` are the projected loads (external loads) introduced at a beam position :math:`x = x_\text{i}`. After inserting the loads from eqs. :eq:`eq_projected_load_P1` and :eq:`eq_projected_load_P2` into :eq:`eq_work_done_derived` and some algebraic manipulations, the total work done by the external loads for the two projection cases can be expressed. In the first case, when projecting onto :math:`\mathbf{P}_1`, the total work is

.. math::
    :label: eq_work_done_caseP1

    W_{P_1} = %%
    %%
    \underbrace{\frac{F^2 \cdot L_1 \cdot l_1^2 \cdot \sin^2 \phi}{2 \cdot E \cdot I_y}}_{\text{a}} %%
    + \underbrace{\frac{-F^2 \cdot L_1^2 \cdot l_1 \cdot \sin \phi}{2 \cdot E \cdot I_y}}_{\text{b}} %%
    + \underbrace{\frac{F^2 \cdot L_1^3}{6 \cdot E \cdot I_y}}_{\text{c}} %%
    + \underbrace{\frac{F^2 \cdot L_1 \cdot l_1^2 \cdot \cos^2 \phi}{2 \cdot G \cdot J}}_{\text{d}} %%

In the second case, when projecting onto :math:`\mathbf{P}_2`, the total work is

.. math::
    :label: eq_work_done_caseP2

    \begin{align}
    W_{P_2} &= %%
    \frac{F^2 \cdot L_2^3}{6 \cdot E \cdot I_y} + \frac{F^2 \cdot L_2 \cdot l_2^2}{2 \cdot G \cdot J} \\
    &= \left\{ \text{using} \quad L_2 = L_1 - l_1 \cdot \sin \phi \quad \text{and} \quad l_2 = l_1 \cdot \cos \phi \right\} = \dots \\[3mm]
    &=
    \underbrace{\frac{F^2 \cdot L_1 \cdot l_1^2 \cdot \sin^2 \phi}{2 \cdot E \cdot I_y}}_{\text{a}} %%
    + \underbrace{\frac{-F^2 \cdot L_1^2 \cdot l_1 \cdot \sin \phi}{2 \cdot E \cdot I_y}}_{\text{b}} %%
    + \underbrace{\frac{F^2 \cdot L_1^3}{6 \cdot E \cdot I_y}}_{\text{c}} %%
    + \underbrace{\frac{F^2 \cdot L_1 \cdot l_1^2 \cdot \cos^2 \phi}{2 \cdot G \cdot J}}_{\text{d}} %%
    \\
    % Additional terms
    &+ \underbrace{\frac{-F^2 \cdot l_1^3 \cdot \sin^3 \phi}{6 \cdot E \cdot I_y}}_{\text{e}} %%
    + \underbrace{\frac{-F^2 \cdot l_1^3 \cdot \sin \phi \cdot \cos^2 \phi}{2 \cdot G \cdot J}}_{\text{f}} %%
    \end{align}

In :eq:`eq_work_done_caseP2` simple geometric relations between lengths :math:`L_1`, :math:`L_2`, :math:`l_1` and :math:`l_2` have been utilised. Comparing eqs. :eq:`eq_work_done_caseP1` and :eq:`eq_work_done_caseP2` shows that the first four terms (*a*, *b*, *c* and *d*) occur in both equations (with the assumption of constant :math:`E \cdot I_y` and :math:`G \cdot J`). However, in the mapping case :math:`\mathbf{P}_2`, there are two *additional* terms (*e* and *f*). Term *e* results from the bending deformation and term *f* from the torsional deformation. In the case illustrated in :numref:`fig_load_mapping_work` (:math:`\phi < 0`), these terms will be positive, hence the beam will store more elastic energy when transferring loads onto point :math:`\mathbf{P}_2` instead of :math:`\mathbf{P}_1`.

Suppose that the off-axis force was located on the opposite side of the beam axis (force shifted in negative :math:`X`-direction, like :math:`\mathbf{F}_\text{b}`) at the same negative beam inclination :math:`\phi`. With the closest-node mapping, the force would be projected *closer* to the wing root than with the projection parallel to :math:`X`. With analogous reasoning, it can be shown that the beam takes up less energy when the load is projected closer to the root.

Example
^^^^^^^

The FEM_ tool |framat| allows to assess work and displacements in a more convenient and general way. The API_ for off-axis loads allows to project onto the nearest node or parallel to :math:`X` (node with the closest :math:`Y`-coordinate). In the FEM_ formulation, the elastic energy is computed as (c.f. [CMPW02]_)

.. math::
    :label: eq_elastic_energy_fem

    W = \frac{1}{2} \cdot \mathbf{U}^T \cdot \mathbf{K} \cdot \mathbf{U}

where :math:`\mathbf{U}` is the vector of nodal deformations and :math:`\mathbf{K}` the global stiffness matrix.

A straight cantilever beam with length :math:`L_2 = 1.5 \text{m}` and variable inclination :math:`\phi` (as illustrated in :numref:`fig_load_mapping_work`) was analysed. The bending stiffness :math:`E \cdot I_y` and the torsional stiffness :math:`G \cdot J` were both set to :math:`1 \text{N/m}^2`. The beam was loaded with off-axis forces :math:`\mathbf{F}_\text{a} = (0 , 0 , F_{z,\text{a}})^T` at point :math:`\mathbf{P}_\text{a}` and :math:`\mathbf{F}_\text{b} = (0 , 0 , F_{z,\text{b}})^T` at :math:`\mathbf{P}_\text{b}`. The points of attack were computed as :math:`\mathbf{P}_\text{a} = \mathbf{P}_1 + l_1 \cdot \mathbf{e}_x` and :math:`\mathbf{P}_\text{b} = \mathbf{P}_1 - l_1 \cdot \mathbf{e}_x` where :math:`\mathbf{P}_1 = L_1 \cdot (-\sin \phi , \cos \phi , 0)^T`. The length :math:`L_1` was set to :math:`1 \text{m}` and :math:`l_1` to :math:`0.5 \text{m}`. Two different load cases were analysed. In the first load case (`A`), :math:`F_{z,\text{a}}` was set to :math:`1 \text{N}` and :math:`F_{z,\text{b}} = 0`. In the second load case (`B`), :math:`F_{z,\text{a}}` and :math:`F_{z,\text{b}}` were both set to :math:`1 \text{N}`. All analyses used 200 beam elements (1206 d.o.f.). **Fig. TODO1 and TODO2** show the elastic energy (or work) and the beam tip deflection :math:`u_z` for different beam inclinations :math:`\phi`.

**TODO** add figure 1

**TODO** add figure 2

In case *B*, a *load pair* is applied. With the parallel-to-:math:`X` projection the two point forces only introduce a force :math:`F_{z,\text{proj}}` into the beam since torsion and bending moments (:math:`M_{x,\text{proj}}` and :math:`M_{y,\text{proj}}`) are cancelled out by contributions acting in opposite directions. In other words, the beam is only loaded in bending due to a point force which is of equal magnitude for all beam inclinations :math:`\phi`. Hence, deflection and work are constant. When projecting with the closest-node approach, there is always one projection point which is closer and one projection point which is further away from point :math:`\mathbf{P}_1` (with the exception :math:`\phi=0`). Both work and tip deflection appear to always be larger than for the parallel-to-:math:`X` mapping scheme. The differences grow larger for larger angles :math:`|\phi|`. With analytical methods it can be easily shown that two individual forces :math:`F_z` applied at :math:`x = x_\text{i} + \Delta x` and at :math:`x = x_\text{i} - \Delta x` will cause a cantilever beam to deflect more than if :math:`2 \cdot F_z` were applied at :math:`x_i` (given constant bending stiffness).

The presented example illustrates that work and deflections generally differ depending on the load mapping choice. Additional differences may arise when the beam has a variable stiffness. Also the overall wing span and the exact locations of the points of attack of the aerodynamic loads will affect results. In the shown example, differences become larger for larger beam inclinations, as the distance between the projection points :math:`\mathbf{P}_1` and :math:`\mathbf{P}_2` grows larger. A general recommendation cannot be made. The preferred (more accurate) mapping scheme may in the end depend on the real internal load transfer which is affected by components such as stiff ribs which are not modelled with a single beam. Nevertheless, one should be aware of differences that can arise in these modelling decisions and their general implications.

.. note::

    This summary is based on/copied from [Dett19]_ with the authors permission.
