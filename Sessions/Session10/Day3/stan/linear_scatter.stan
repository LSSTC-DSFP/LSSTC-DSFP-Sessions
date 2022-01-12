data {
  int nobs;
  vector[nobs] xobs;
  vector[nobs] yobs;
  vector[nobs] sigma_y;
}

parameters {
  real m;
  real b;
  real<lower=0> sigma_int;
  vector[nobs] y_true;
}

transformed parameters {
   vector[nobs] mu_y_true = m*xobs + b;
}

model {
  /* Flat in m and b. */

  y_true ~ normal(mu_y_true, sigma_int);
  yobs ~ normal(y_true, sigma_y);
}
