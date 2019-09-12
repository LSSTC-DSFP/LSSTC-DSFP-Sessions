post_lnp_complete = np.array( [ [ln_prior(T0,Ts)+ln_like_complete(T0,Ts) for T0 in post_T0] for Ts in post_Ts] )
