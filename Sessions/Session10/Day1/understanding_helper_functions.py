import numpy as  np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

import emcee
import corner
from multiprocessing import Pool, cpu_count


def pollute_namespace():

    np.random.seed(212)

    x = np.random.uniform(0,1000,56)
    sigma = 150
    y = 1.75*x + 41 + np.random.normal(0,sigma,len(x))
    y_unc = sigma*np.ones_like(x)
    
    return x, y, y_unc

def n_obs_n_poly():
    np.random.seed(212)
    
    x = np.ones(5)*4
    y = np.random.uniform(0,100,5)
    
    fig, ax = plt.subplots()
    ax.plot(x, y, 'o')
    ax.set_xlabel('x', fontsize=14)
    ax.set_ylabel('y', fontsize=14)
    ax.set_xlim(0,10)
    fig.tight_layout()

def chi2_example():
    np.random.seed(212)
    
    x = np.random.uniform(0,100,20)
    sigma = 15
    y = 2.1*x + 41 + np.random.normal(0,sigma,len(x))
    y_unc = sigma/3*np.ones_like(x)

    p1 = np.polyfit(x, y, 1)
    p1_eval = np.poly1d(p1)
    chi2_1 = np.sum((y - p1_eval(x))**2/y_unc**2)/(len(x)-2)
    npoly = 14
    p10 = np.polyfit(x, y, npoly)
    p10_eval = np.poly1d(p10)
    chi2_10 = np.sum((y - p10_eval(x))**2/y_unc**2)/(len(x)-npoly)
    
    
    fig = plt.figure(figsize=(7,8))
    ax = plt.subplot2grid((4,1), (0, 0), rowspan=2)
    ax_res1 = plt.subplot2grid((4,1), (2, 0), sharex=ax)
    ax_res10 = plt.subplot2grid((4,1), (3, 0), sharex=ax)

    ax.errorbar(x, y, y_unc, fmt='o')
    ax.plot(np.linspace(0,100,1000), p1_eval(np.linspace(0,100,1000)), 
            label=r'$1^\mathrm{st}$ order polynomial; $\chi^2_\nu = $' + '{:.4f}'.format(chi2_1))
    ax.plot(np.linspace(0,100,1000), p10_eval(np.linspace(0,100,1000)), 
            label=r'$14^\mathrm{th}$ order polynomial; $\chi^2_\nu = $' + '{:.4f}'.format(chi2_10))
    ax.set_ylim(-2700, 3200)
    ax.legend(fancybox=True)

    ax_res1.errorbar(x, y - p1_eval(x), y_unc, fmt='o')
    ax_res1.axhline(color='C1')
    ax_res1.set_ylabel('residuals', fontsize=14)

    ax_res10.errorbar(x, y - p10_eval(x), y_unc, fmt='o')
    ax_res10.axhline(color='C2')
    ax_res10.set_ylabel('residuals', fontsize=14)
    ax_res10.set_xlabel('x', fontsize=14)
    plt.setp(ax.get_xticklabels(), visible=False)
    plt.setp(ax_res1.get_xticklabels(), visible=False)
    fig.tight_layout()
    

def noisy_plot():
    np.random.seed(212)

    x = np.random.uniform(0,10,18)
    sigma = 3
    y = 3*x + 23 + np.random.normal(0,sigma,len(x))

    fig, ax = plt.subplots()
    ax.plot(x, y, 'o')
    ax.set_xlabel('x', fontsize=14)
    ax.set_ylabel('y', fontsize=14)
    fig.tight_layout()
    


def lnlike(theta, x, y):
    m = theta[0]
    b = theta[1]
    sigmas = theta[2:]
    
    lnl = np.sum(np.log(1/(2*np.pi*sigmas**2)) - (y - m*x -b)**2/(2*sigmas**2))
    return lnl

def nuissance_model():
    np.random.seed(212)
    x = np.random.uniform(0,10,18)
    sigma = 3
    y = 3*x + 23 + np.random.normal(0,sigma,len(x))

    ndim = 20
    nwalkers = 2500
    guess_0 = np.array([3,25]+[3]*18)
    nfac = [10**(-1)]*ndim

    pos = guess_0*[1 + nfac*np.random.randn(ndim) for i in range(nwalkers)]

    ncores = cpu_count()
    with Pool(ncores) as pool:


        sampler = emcee.EnsembleSampler(nwalkers, ndim, lnlike, args=[x, y],
                                        pool=pool, moves=emcee.moves.KDEMove())
        for sample in sampler.sample(pos, 
                                     iterations=100, 
                                     progress=False):
            if sampler.iteration == 10:
                print('Fitting a 20 parameter model with 18 data points...')
            elif sampler.iteration == 30:
                print('    Hopefully this does not destroy the universe...')
            elif sampler.iteration == 60:
                print('        We are approaching the singularity...')
            elif sampler.iteration == 90:
                print("            I wish my last day on Earth wasn't with this Adam bozo...")
            else:
                continue


    tau = np.mean(sampler.get_autocorr_time(tol=0)[0:2])
    samples = sampler.get_chain(discard=3*int(tau), thin=int(tau), flat=True)[:,0:2]

    _ = corner.corner(samples, 
                      labels = ['$m$', '$b$'], truths=[3, 23], 
                      show_titles=True, quantiles=[0.1, 0.5, 0.9])

def gen_mix_data():
    np.random.seed(212)
    
    npts = 25
    x = np.random.uniform(0,100,npts)
    y = np.empty_like(x)
    y_unc = np.empty_like(x)
    
    for i in range(npts):
        rand = np.random.uniform()
        if rand > 0.3:
            sigma = np.random.uniform(3,7)
            y[i] = 0.8*x[i] + 13 + np.random.normal(0,sigma)
            y_unc[i] = sigma
        else:
            sigma = np.random.uniform(3,7)
            y[i] = -0.5*x[i] + 60 - np.random.normal(0,20)
            y_unc[i] = sigma
    
    return x, y, y_unc


def plot_mix_model():
    
    x, y, y_unc = gen_mix_data()
    
    fig, ax = plt.subplots()
    ax.errorbar(x, y, y_unc, fmt='o')
    ax.set_xlabel('x', fontsize=14)
    ax.set_ylabel('y', fontsize=14)
    fig.tight_layout()

def weighted_least_squares():
    
    x, y, y_unc = gen_mix_data()
    
    p = np.polyfit(x, y, 1, w=1/y_unc)
    p_eval = np.poly1d(p)

    fig = plt.figure(figsize=(6,5))
    ax = plt.subplot2grid((3,1), (0, 0), rowspan=2)
    ax_res = plt.subplot2grid((3,1), (2, 0), sharex=ax)

    ax.errorbar(x, y, y_unc, fmt='o')
    ax.plot([0,100], p_eval([0,100]))
    ax.set_ylabel('y', fontsize=14)

    ax_res.errorbar(x, y - p_eval(x), y_unc, fmt='o')
    ax_res.axhline(color='C1')
    ax_res.set_ylabel('residuals', fontsize=14)
    ax_res.set_xlabel('x', fontsize=14)
    plt.setp(ax.get_xticklabels(), visible=False)

    fig.tight_layout()

def huber_loss(val, c=3):
    loss = np.empty_like(val)
    quad_loss = np.abs(val) < c
    loss[quad_loss] = 0.5*val[quad_loss]**2
    loss[~quad_loss] = c*(np.abs(val[~quad_loss]) - 0.5*c)

    return loss

def huber_plot():
    
    x_grid = np.linspace(-15,15,1000)
 
    fig, ax = plt.subplots()
    ax.plot(x_grid, 0.5 * x_grid ** 2, label="squared loss", lw=2)
    for c in (10, 5, 3):
        ax.plot(x_grid, huber_loss(x_grid, c), label="Huber loss, c={0}".format(c), lw=2)
    ax.set_ylabel('loss', fontsize=14)
    ax.set_xlabel('$\Delta \sigma$',  fontsize=14)
    ax.legend(loc='best', fancybox=True, frameon=False)
    fig.tight_layout()

def total_huber_loss(theta, x, y, y_unc, c=3):
    m, b = theta
    
    distance = (y - m*x - b)/y_unc
    
    return np.sum(huber_loss(distance, c=c))

def minimize_huber():
    
    x, y, y_unc = gen_mix_data()

    res = minimize(total_huber_loss, [.6,20], method='Powell', # Powell method does not need derivatives
                      args=(x, y, y_unc, 1))
    
    p = np.polyfit(x, y, 1, w=1/y_unc)
    p_eval = np.poly1d(p)

    fig = plt.figure(figsize=(6,5))
    ax = plt.subplot2grid((3,1), (0, 0), rowspan=2)
    ax_res = plt.subplot2grid((3,1), (2, 0), sharex=ax)

    ax.errorbar(x, y, y_unc, fmt='o')
    ax.plot([0,100], p_eval([0,100]), label='least-squares')
    ax.plot([0,100], res.x[1] + res.x[0]*np.array([0,100]), label='Huber loss')
    ax.set_ylabel('y', fontsize=14)
    ax.legend(loc=9,fancybox=True)
    
    ax_res.errorbar(x, y - res.x[1] - res.x[0]*x, y_unc, fmt='o')
    ax_res.axhline(color='C2')
    ax_res.set_ylabel('residuals', fontsize=14)
    ax_res.set_xlabel('x', fontsize=14)
    plt.setp(ax.get_xticklabels(), visible=False)

    fig.tight_layout()
    
    return