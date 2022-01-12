def log_evidence(Model, N=1000):
    """
    Compute the log evidence for the model
    
    Need to take care to do the sum without numerical error...
    """
    # Draw large number of samples from the prior
    a_from_prior = Model.draw_samples_from_prior(N)
    
    # Compute the log likelihood for each one
    ll_from_prior = Model.vectorized_log_likelihood(a_from_prior)
    
    # Exponentiate, take the average, and take the log again.
    # More stably, use scipy special function to sum the 
    log_evidence = logsumexp(ll_from_prior) - np.log(N)
    
    return log_evidence
