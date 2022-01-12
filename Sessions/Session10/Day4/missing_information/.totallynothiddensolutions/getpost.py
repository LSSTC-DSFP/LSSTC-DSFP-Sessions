post_lnp = np.array( [ [ln_prior(T0,Ts)+ln_like(T0,Ts) for T0 in post_T0] for Ts in post_Ts] )
