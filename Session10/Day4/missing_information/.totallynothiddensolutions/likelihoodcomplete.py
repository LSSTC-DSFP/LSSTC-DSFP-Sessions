def ln_like_complete(T0, Ts):
    fail_part = np.sum(np.log( 1.0 - P_success(failure_temps, T0, Ts) ))
    success_part = np.sum(np.log( P_success(success_temps, T0, Ts) ))
    return fail_part + success_part
