data {
  int nobs;
  vector[nobs] xobs;
  vector[nobs] yobs;
  vector[nobs] sigma_x;
  vector[nobs] sigma_y;
}

parameters {
  real m;
  real b;
  vector[nobs] x_true;
}

transformed parameters {
   vector[nobs] y_true = m*x_true + b;
}

model {
  /* Flat in m and b and x_true. */

  yobs ~ normal(y_true, sigma_y);
  xobs ~ normal(x_true, sigma_x);
}
