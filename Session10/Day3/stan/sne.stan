functions {
  vector mu_of_z(vector z, real M, real Om, real w) {
    int nobs = dims(z)[1];

    real w2 = w*w;
    real wOm = w*Om;
    real w2Om = w2*Om;
    real w2Om2 = w2Om*Om;

    vector[nobs] numer = z + (z .* z)*(3 - 10*w + 3*w2 + 10*wOm + 6*w2Om - 9*w2Om2)/(4*(1 - 3*w + 3*wOm));
    vector[nobs] denom = 1 + z*(1-2*w-3*w2+2*wOm+12*w2Om-9*w2Om2)/(2*(1-3*w+3*wOm));

    vector[nobs] dL = numer ./ denom;

    /* mu = 5*log10(d/(10 pc)) = 5*log10(d/(1 Mpc)) + 25 */
    return 5*log10(dL) + M;
  }
}

data {
  int nobs;
  vector[nobs] zobs;
  vector[nobs] muobs;
  vector[nobs] sigma_mu;
}

parameters {
  real M;
  real<lower=0,upper=1> Om;
  real w;
}

model {
  /* Impose some weak priors on the parameters */
  Om ~ normal(0.3, 0.1);
  w ~ normal(-1, 0.5);

  muobs ~ normal(mu_of_z(zobs, M, Om, w), sigma_mu);
}

generated quantities {
  vector[nobs] mu_true = mu_of_z(zobs, M, Om, w);
}
