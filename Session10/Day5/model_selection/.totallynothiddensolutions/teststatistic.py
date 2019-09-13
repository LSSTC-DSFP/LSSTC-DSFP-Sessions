def T(yy):
    """
    Argument: a data vector (either the real data or a simulated data set)
    Returns: a scalar test statistic computed from the argument
    """
    #return len(np.where(yy > 200.0)[0])
    return len(np.where(yy < 100.0)[0])
    #return np.std(yy)

