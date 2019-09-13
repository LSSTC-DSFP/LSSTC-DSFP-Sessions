class ExponentialModel(Model):
    """
    Simple exponential model for mis-centering.
    """
    def __init__(self):
        # Define any hyperparameters for the a1 prior here.
        # E.g., for uniform, something like "self.min_a1 = value" and "self.max_a1 = value"
        # More sophisticatedly, you could make these values arguments of __init__.
        self.min_a1 = 0.0
        self.max_a1 = 1000.0
        # The next line finishes initialization by calling the parent class' __init__
        Model.__init__(self)
  
    def log_prior(self, a1):
        """
        Evaluate the log prior PDF P(a1|H)
        """
        if a1 <= self.min_a1 or a1 > self.max_a1:
            return -np.inf
        return 0.0

    def draw_samples_from_prior(self, N):
        """
        Return N samples of a1 from the prior PDF P(a1|H)
        """
        return st.uniform.rvs(loc=self.min_a1, scale=self.max_a1-self.min_a1, size=N)

    def log_likelihood(self, a1):
        """
        Evaluate the log of the likelihood function L(a1) = P(y|a1,H)
        """
        return np.sum(st.expon.logpdf(y, scale=a1))
    
    def sampling_distribution(self, yy, a1):
        """
        Evaluate the sampling distribution P(yy|a,H) at a point in data space yy given parameter value a1
        We expect a vector input yy, and return the corresponding probabilities.
            
        Note: This is useful for making plots of "the model" overlaid on the histogram of the data
        """
        return st.expon.pdf(yy, scale=a1)
        
    def generate_replica_dataset(self, a1):
        """
        Draw a replica data set y_rep from the sampling distribution P(y_rep|a1,H).
        y_rep should have the same length as the true data set.
        """
        return st.expon.rvs(size=len(y), scale=a1)
