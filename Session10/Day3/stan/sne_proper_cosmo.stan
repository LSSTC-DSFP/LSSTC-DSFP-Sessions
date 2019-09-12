functions {
  /* To solve for the proper cosmology, we use Stan's ODE integrator (the latest
     versions of Stan actually can perform 1D integrals, but you may not have
     the latest version).  The idea is that the integral we want,

     dC = \int_0^z dz 1/E(z)

     can be phrased as a solution to an ODE, where

     d(dC)/dz = 1/E(z)

     with dC(z=0) = 0.  The function below gives the RHS of d(dC)/dz.  Because
     Stan's ODE solver is meant to solve *systems* of ODEs, we need to return
     the RHS as a real array, even though it only has one component.

     The x_r and x_i arguments must be data (i.e. from the data or transformed
     data blocks), and can be used to pass in "fixed" values; this saves some
     computation of gradients.  The theta vector is used to pass in parameters
     (so gradients must be computed w.r.t. these).

     */
  real [] d_dC_d_z(real z, real [] y, real [] theta, real [] x_r, int [] x_i) {
    real Om = theta[1];
    real w = theta[2];
    real ddCdz[1];

    real opz = 1 + z;
    real opz2 = opz*opz;
    real opz3 = opz2*opz;

    ddCdz[1] = 1.0/sqrt(Om*opz3 + (1-Om)*(1+z)^(3*(1+w)));

    return ddCdz;
  }

  vector mb_of_z(vector z, vector dC, real M) {
    return 5*log10(dC .* (1+z)) + M;
  }
}

data {
  int nobs;
  vector[nobs] zobs; /* Assumed in sorted order! */
  vector[nobs] mbobs;
  vector[nobs] sigma_mb;
}

transformed data {
  real x_r[0];
  int x_i[0];
}

parameters {
  real M;
  real<lower=0,upper=1> Om;
  real w;
}

transformed parameters {
  vector[nobs] mb_true;

  {
    vector[nobs] dC;

    real theta[2] = {Om, w};
    real dC_state0[1] = {0.0};
    real dC_states[nobs, 1];

    dC_states = integrate_ode_rk45(d_dC_d_z, dC_state0, 0.0, to_array_1d(zobs), theta, x_r, x_i);
    dC = to_vector(dC_states[:,1]);

    mb_true = mb_of_z(zobs, dC, M);
  }
}

model {
  /* Impose some weak priors on the parameters */
  Om ~ normal(0.3, 0.1);
  w ~ normal(-1, 0.5);

  mbobs ~ normal(mb_true, sigma_mb);
}
