data {
  int nobs;
  vector[nobs] xobs;
  vector[nobs] yobs;
  vector[nobs] sigma_y;
}

parameters {
  real<lower=0,upper=1> A;
  real m;
  real b;
  real mu_bad;
  real<lower=0> sigma_bad;
  real<lower=0> sigma_int;
  vector[nobs] y_true;
}

model {
  /* Flat prior on A. */

  /* We need to impose some priors on sigma_int and sigma_bad to prevent them
     from getting too small (forcing a parameter into too small of a volume
     casues difficulties for the sampler). */
  sigma_bad ~ lognormal(log(200), 1);
  sigma_int ~ lognormal(log(10), 1);

  mu_bad ~ normal(400, 200);

  /* As long as we are imposing priors, let's put a uniform-angle prior on m,
     and a sensible prior on b.*/
  m ~ cauchy(0,1);
  b ~ normal(0, 300);

  /* To implement the mixture model, we need a loop, because each y_true could
     be one of the two cases independently; a vectorized expression would assume
     that *all* y_true are one case or *all* y_true are the other.*/
  for (i in 1:nobs) {
    target += log_mix(A,
                      normal_lpdf(y_true[i] | m*xobs[i] + b, sigma_int),
                      normal_lpdf(y_true[i] | mu_bad, sigma_bad));
  }

  yobs ~ normal(y_true, sigma_y);
}

generated quantities {
  vector[nobs] log_good_bad_ratio;

  for (i in 1:nobs) {
    log_good_bad_ratio[i] = log(A) + normal_lpdf(y_true[i] | m*xobs[i] + b, sigma_int) - (log1p(-A) + normal_lpdf(y_true[i] | mu_bad, sigma_bad));
  }
}
