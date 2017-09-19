import daft

def pgm_cepheids():

    # Instantiate a PGM.
    pgm = daft.PGM([2.9, 2.7], origin=[0.3, 0.3], grid_unit=2.6, node_unit=1.3, observed_style="inner")

    # Model parameters:
    pgm.add_node(daft.Node("a", r"$a$", 1.0, 2.6))
    pgm.add_node(daft.Node("b", r"$b$", 2.0, 2.6))

    # Latent variable - intrinsic magnitude:
    pgm.add_node(daft.Node("m", r"$m_k$", 1.5, 1.4, fixed=True, offset=(0,-20)))

    # Data - observed magnitude:
    pgm.add_node(daft.Node("mobs", r"$m^{\rm obs}_k$", 2.5, 1.4, observed=True))

    # Constants - magnitude errors and log Periods:
    pgm.add_node(daft.Node("logP", r"$\log_{10} P_k$", 0.9, 1.4, fixed=True, offset=(-3,1)))
    pgm.add_node(daft.Node("merr", r"$\sigma_k$", 1.9, 0.9, fixed=True, offset=(-3,2)))

    # Add in the edges.
    pgm.add_edge("a", "m")
    pgm.add_edge("b", "m")
    pgm.add_edge("logP", "m")
    pgm.add_edge("merr", "mobs")
    pgm.add_edge("m", "mobs")

    # And a plate for the pixels
    pgm.add_plate(daft.Plate([0.5, 0.7, 2.5, 1.4], label=r"cepheids $k$", shift=-0.1))

    # Render and save.
    pgm.render()
    pgm.figure.savefig("pgms_cepheids.png", dpi=300)

    return


# Just make the PGM:

pgm_cepheids()
