def pvalue(Model):
    """
    Compute the posterior predictive p-value, P(T > T(y)|y,H):
    """
    # Compute the posterior predictive distribution of T(yrep)
    TT = distribution_of_T(Model)    
    # Compare this distribution with T(y)
    return len(TT[TT > T(y)]) / len(TT)

