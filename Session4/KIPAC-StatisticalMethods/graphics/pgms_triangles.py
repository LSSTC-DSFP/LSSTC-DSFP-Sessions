def pgms_triangles(option='a-c-d'):
    """
    Draws one of two triangular PGMs.

    Parameters
    ----------
    option: string
        which PGM to draw, 'a-c-d' or 'c-y-d'
    """
    # Start diagram:
    import daft
    pgm = daft.PGM([2.3, 1.9], origin=[0.2, 0.6], grid_unit=2.6, node_unit=1.0, observed_style="inner")

    # Parameter:
    pgm.add_node(daft.Node("theta", r"$\theta$", 1.3, 2))

    # Latent variable:
    pgm.add_node(daft.Node("c", r"$c$", 0.6, 1, fixed=True, offset=(-7,4)))

    # Data:
    pgm.add_node(daft.Node("d", r"$d$", 2, 1))

    # Add in the edges.
    pgm.add_edge("theta", "c")
    pgm.add_edge("c", "d")

    if option == 'a-c-d':
        pgm.add_edge('theta', 'd')
    elif option == 'c-y-d':
        pgm.add_edge('d', 'theta')
    else:
        assert False

    # Render and save.
    pgm.render()
    outfile = "pgms_"+option+".png"
    pgm.figure.savefig(outfile, dpi=300)

    return


# Make images for lecture notes:
pgms_triangles(option='a-c-d')
pgms_triangles(option='c-y-d')
