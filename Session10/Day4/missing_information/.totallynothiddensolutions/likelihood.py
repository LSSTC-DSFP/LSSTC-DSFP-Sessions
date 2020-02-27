def integral_P_success(start, end, T0, Ts):
    return Ts * np.log( (1.0 + np.exp((end-T0)/Ts)) / (1.0 + np.exp((start-T0)/Ts)) )

def ln_like(T0, Ts):
    fail_part = np.sum(np.log( 1.0 - P_success(failure_temps, T0, Ts) ))
    success_part = Nsuccess * np.log( integral_P_success(success_Tmin, success_Tmax, T0, Ts) )
    return fail_part + success_part
