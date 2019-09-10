import numpy as np
import matplotlib.pyplot as plt


def hastings_ratio(theta_1, theta_0, y, x, y_unc):
    '''
    Calculate the Hastings ratio
    
    Parameters
    ----------
    theta_1 : tuple
        proposed new posterior position 
    
    theta_0 : tuple
        current posterior position
    
    y : arr-like, shape (n_samples)
        Array of observational measurements
    
    x : arr-like, shape (n_samples)
        Array of positions where y is measured
    
    y_unc : arr-like, shape (n_samples)
        Array of uncertainties on y
        
    Returns
    -------
    h_ratio : float
        The Hastings ratio
    '''
    lnpost1 = lnposterior(theta_1, y_obs, x, y_unc)
    lnpost0 = lnposterior(theta_0, y_obs, x, y_unc)
    
    h_ratio = np.exp(lnpost1)/np.exp(lnpost0)
    
    return h_ratio

def propose_jump(theta, cov):
    '''
    Generate a proposed new position for MCMC chain
    
    Parameters
    ----------
    theta : 1-D array_like, of length N
        current position of the MCMC chain
    
    cov : 1-D or 2-D array_like, of shape (N,) or (N, N)
        Covariance matrix of the distribution. It must be symmetric 
        and positive-semidefinite for proper sampling.
        
        1-D inputs for cov require the standard deviation along 
        each axis of the N-dimensional Gaussian.

    
    Returns
    -------
    proposed_position : 1-D array_like, of length N
    '''
    if np.shape(theta) == np.shape(cov):
        cov = np.diag(np.array(cov)**2)
    
    proposed_position = np.random.multivariate_normal(theta, cov)
    
    return proposed_position

def mh_mcmc(theta_0, cov, nsteps, y, x, y_unc):
    '''
    Metropolis-Hastings MCMC algorithm
    
    Parameters
    ----------
    theta_0 : 1-D array_like of shape N
        starting position for the MCMC chain
    
    cov : 1-D or 2-D array_like, of shape (N,) or (N, N)
        Covariance matrix of the distribution. It must be symmetric 
        and positive-semidefinite for proper sampling.
        
        1-D inputs for cov require the standard deviation along 
        each axis of the N-dimensional Gaussian.

    nsteps : int
        Number of steps to take in the MCMC chain
        
    y : arr-like, shape (n_samples)
        Array of observational measurements
    
    x : arr-like, shape (n_samples)
        Array of positions where y is measured
    
    y_unc : arr-like, shape (n_samples)
        Array of uncertainties on y
        
    Returns
    -------
    (positions, lnpost_at_pos, acceptance_ratio) : tuple
        positions : 2-D array_like of shape (nsteps+1, N)
            Position of the MCMC chain at every step
        
        lnpost_at_pos : 1-D array_like of shape nsteps+1
            log-posterior value at the position of the MCMC chain
        
        acceptance_ratio : 1-D array_like of shape nsteps+1
            acceptance ratio of all previous steps in the chain    
    '''
    
    positions = np.zeros((nsteps+1, len(theta_0)))
    lnpost_at_pos = -np.inf*np.ones(nsteps+1)
    acceptance_ratio = np.zeros_like(lnpost_at_pos)
    accepted = 0
    
    positions[0] = theta_0
    lnpost_at_pos[0] = lnposterior(theta_0, y, x, y_unc)
    
    for step_num in np.arange(1, nsteps+1):
        proposal = propose_jump(positions[step_num-1], cov)
        H = hastings_ratio(proposal, positions[step_num-1], y, x, y_unc)
        R = np.random.uniform()
        
        if H > R:
            accepted += 1
            positions[step_num] = proposal
            lnpost_at_pos[step_num] = lnposterior(proposal, y, x, y_unc)
            acceptance_ratio[step_num] = float(accepted)/step_num
        else:
            positions[step_num] = positions[step_num-1]
            lnpost_at_pos[step_num] = lnpost_at_pos[step_num-1]
            acceptance_ratio[step_num] = float(accepted)/step_num
    
    return (positions, lnpost_at_pos, acceptance_ratio)

def plot_post(theta_0, cov, nsteps, y, x, y_unc):
    '''
    Plot posterior trace from MH MCMC
    
    Parameters
    ----------
    theta_0 : 1-D array_like of shape N
        starting position for the MCMC chain
    
    cov : 1-D or 2-D array_like, of shape (N,) or (N, N)
        Covariance matrix of the distribution. It must be symmetric 
        and positive-semidefinite for proper sampling.
        
        1-D inputs for cov require the standard deviation along 
        each axis of the N-dimensional Gaussian.

    nsteps : int
        Number of steps to take in the MCMC chain
        
    y : arr-like, shape (n_samples)
        Array of observational measurements
    
    x : arr-like, shape (n_samples)
        Array of positions where y is measured
    
    y_unc : arr-like, shape (n_samples)
        Array of uncertainties on y
    '''
    pos, lnpost, acc = mh_mcmc(theta_0, cov, nsteps, y_obs, x, y_unc)
    
    fig, (ax1, ax2) = plt.subplots(1,2,figsize=(9,4))
    
    ax1.plot(pos[:,0], pos[:,1], 'o-', alpha=0.3)
    ax1.plot(2.3, 15, '*', ms=30, 
            mfc='Crimson', mec='0.8', mew=2, 
            alpha=0.7)
    ax1.set_xlabel('m', fontsize=14)
    ax1.set_ylabel('b', fontsize=14)

    ax2.plot(pos[:,0], pos[:,1], 'o-', alpha=0.3)
    cax = ax2.scatter(pos[:,0], pos[:,1], c = lnpost, zorder=10)
    ax2.plot(2.3, 15, '*', ms=30, 
            mfc='Crimson', mec='0.8', mew=2, 
            alpha=0.7, zorder=20)
    ax2.set_xlabel('m', fontsize=14)
    ax2.set_ylabel('b', fontsize=14)
    cbar = fig.colorbar(cax)
    cbar.ax.set_ylabel(r'$\log \; \pi (\theta)$', fontsize=12)
    fig.tight_layout()
    
    return

def plot_mh_summary(theta_0, cov, nsteps, y, x, y_unc):
    '''
    Plot the posterior, draws from the posterior, and 1-d chains
    
    Parameters
    ----------
    theta_0 : 1-D array_like of shape N
        starting position for the MCMC chain
    
    cov : 1-D or 2-D array_like, of shape (N,) or (N, N)
        Covariance matrix of the distribution. It must be symmetric 
        and positive-semidefinite for proper sampling.
        
        1-D inputs for cov require the standard deviation along 
        each axis of the N-dimensional Gaussian.

    nsteps : int
        Number of steps to take in the MCMC chain
        
    y : arr-like, shape (n_samples)
        Array of observational measurements
    
    x : arr-like, shape (n_samples)
        Array of positions where y is measured
    
    y_unc : arr-like, shape (n_samples)
        Array of uncertainties on y
    '''
    pos, lnpost, acc = mh_mcmc(theta_0, cov, nsteps, y_obs, x, y_unc)

    fig = plt.figure(figsize=(7.5,6))
    ax1 = plt.subplot2grid((4,5), (0, 0), colspan=2, rowspan=2)
    ax2 = plt.subplot2grid((4,5), (2, 0), colspan=2, rowspan=2)
    ax3 = plt.subplot2grid((4,5), (0, 2), colspan=3)
    ax4 = plt.subplot2grid((4,5), (1, 2), colspan=3, sharex=ax3)
    ax5 = plt.subplot2grid((4,5), (2, 2), colspan=3, sharex=ax3)
    ax6 = plt.subplot2grid((4,5), (3, 2), colspan=3, sharex=ax3)

    # posterior
    ax1.hexbin(pos[:,0], pos[:,1], gridsize=50, mincnt=1, bins='log')
    ax1.plot(2.3, 15, '*', ms=30, 
        mfc='Crimson', mec='0.8', mew=2, 
        alpha=0.7)
    ylims = ax1.get_ylim()
    xlims = ax1.get_xlim()
    ax1.plot([2.3, 2.3], ylims, 'Crimson', alpha=0.3)
    ax1.plot(xlims, [15, 15], 'Crimson', alpha=0.3)
    ax1.set_ylim(ylims)
    ax1.set_xlim(xlims)
    ax1.set_xlabel('m')
    ax1.set_ylabel('b')
    ax1.xaxis.set_ticks_position('top')
    ax1.xaxis.set_label_position('top')
    ax1.tick_params(top=True, bottom=False)
    
    # posterior draws
    ax2.errorbar(x, y_obs, y_unc, fmt='o')
#     ax2.plot([0,100], 
#              b_true + m_true*np.array([0,100]),
#              '--', color='DarkOrange', lw=2, zorder=-10)
    for draw in np.random.choice(len(pos), 10, replace=False):
        ax2.plot([0,100], pos[draw,1] + pos[draw,0]*np.array([0,100]),
                 'DarkOrange', alpha=0.4)
    ax2.set_xlabel('x')
    ax2.set_ylabel('y')
    
    ax3.plot(pos[:,0])
    ax3.set_ylabel('m')
    
    ax4.plot(pos[:,1])
    ax4.set_ylabel('b')

    ax5.plot(lnpost)
    ax5.set_ylabel('$\ln \; \pi$')

    ax6.plot(acc)
    ax6.set_ylabel('acceptance')
    ax6.set_xlabel('step number')
    plt.setp(ax3.get_xticklabels(), visible=False)
    plt.setp(ax4.get_xticklabels(), visible=False)
    plt.setp(ax5.get_xticklabels(), visible=False)
    
    fig.tight_layout()
    fig.subplots_adjust(top=0.93, left=0.09, right=0.99, hspace=0.07, wspace=0.75)