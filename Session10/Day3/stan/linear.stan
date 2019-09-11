data {
  int nobs;
  vector[nobs] xobs;
  vector[nobs] yobs;
  vector[nobs] sigma_y;
}

parameters {
  real m;
  real b;
}

transformed parameters {
  vector[nobs] y_true = m*xobs + b;
}

model {
  /* Flat in m and b. */

  yobs ~ normal(y_true, sigma_y);
}
