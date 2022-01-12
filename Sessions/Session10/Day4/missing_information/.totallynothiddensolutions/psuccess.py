def P_success(T, T0, Ts):
    return 1.0 / (1.0 + np.exp(-(T-T0)/Ts))
