def pgms_xray_image(pars_fixed=True, multiple_pixels=False, inverse=False):
    """
    Draws various PGMs for the Xray image simulation example.

    Parameters
    ----------
    pars_fixed: boolean
        whether or not the input cluster parameters are fixed or sampled from some PDF
    multiple_pixels: boolean
        whether or not to add a plate to show many pixels being predicted
    inverse: boolean
        whether or not we are describing an inverse problem, with "observed" data.
    """
    # Start diagram:
    import daft
    pgm = daft.PGM([2.3, 2.05], origin=[0.2, 0.3], grid_unit=2.6, node_unit=1.0, observed_style="inner")

    # Input cluster parameters:
    pgm.add_node(daft.Node("theta", r"$\theta$", 0.5, 2, fixed=pars_fixed))

    # Latent variable (expected counts):
    pgm.add_node(daft.Node("muk", r"$\mu_k$", 1, 1, fixed=True, offset=(7,4)))

    # Data:
    if inverse:
        pgm.add_node(daft.Node("Nk", r"$N_k$", 2, 1, observed=True))
    else:
        pgm.add_node(daft.Node("Nk", r"$N_k$", 2, 1))

    # Add in the edges.
    pgm.add_edge("theta", "muk")
    pgm.add_edge("muk", "Nk")

    # And a plate:
    if multiple_pixels: pgm.add_plate(daft.Plate([0.5, 0.5, 2, 1], label=r"pixels $k$", shift=-0.1))

    # Render and save.
    pgm.render()
    if multiple_pixels:
        outfile = "pgms_all_pixels"
    else:
        outfile = "pgms_one_pixel"

    if pars_fixed:
        outfile += "_input_fixed"
    else:
        outfile += "_input_sampled"

    if inverse:
        outfile += "_inverse.png"
    else:
        outfile+= ".png"

    pgm.figure.savefig(outfile, dpi=300)

    return


# Make three images for lecture notes:
pgms_xray_image(pars_fixed=True, multiple_pixels=False, inverse=False)
pgms_xray_image(pars_fixed=False, multiple_pixels=False, inverse=False)
pgms_xray_image(pars_fixed=True, multiple_pixels=True, inverse=False)
pgms_xray_image(pars_fixed=False, multiple_pixels=True, inverse=True)
