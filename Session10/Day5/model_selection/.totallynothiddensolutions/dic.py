def DIC(Model):
    """
    Compute the Deviance Information Criterion for the given model
    """
    # Compute the deviance D for each sample, using the vectorized code.
    D = -2.0*Model.vectorized_log_likelihood(Model.samples)
    # Two terms
    mean_of_D = np.mean(D)    
    D_of_mean = -2.0*Model.log_likelihood(np.mean(Model.samples, axis=0))
    # Combine to form the outputs
    pD = mean_of_D - D_of_mean
    DIC = mean_of_D + 2.0*pD
    return DIC, pD
