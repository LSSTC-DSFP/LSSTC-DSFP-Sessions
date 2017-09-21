#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
    This hacked version of triangle, called triangle_linear, is an adaption of the following authors open source code, their credentials below.  triangle_linear is an adaption by Megan Shabram and Dan Gettings, made in 2013. Some of the original functionality may still be there but are not being used in this version. This code takes longer to run. It is calculating a 2d Gaussian kernel density estimate of 2d marginal posteriors in order to report posterior summarys.  It also reports 95 % equal tailed credible intervals by importing python code written by Megan Shabram and Dan Gettings called credible_interval.py
'''


from __future__ import print_function, absolute_import, unicode_literals

__all__ = ["corner", "hist2d", "error_ellipse"]
__version__ = "0.0.5"
__author__ = "Dan Foreman-Mackey (danfm@nyu.edu)"
__copyright__ = "Copyright 2013 Daniel Foreman-Mackey"
__contributors__ = [    # Alphabetical by first name.
                        "Ekta Patel @ekta1224",
                        "Geoff Ryan @geoffryan",
                        "Phil Marshall @drphilmarshall",
                        "Pierre Gratier @pirg",
                   ]

import numpy as np
import matplotlib.pyplot as pl
from matplotlib.ticker import MaxNLocator
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import Ellipse
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
import scipy.ndimage as ndimage
import scipy.stats as stats
import kdestats
import credible_interval

def corner(xs, labels=None,labelsy=None, extents=None, truths=None, truth_color='black',
           scale_hist=False, quantiles=[], **kwargs):
    """
    Make a *sick* corner plot showing the projections of a set of samples
    drawn in a multi-dimensional space.

    :param xs: ``(nsamples, ndim)``
        The samples. This should be a 1- or 2-dimensional array. For a 1-D
        array this results in a simple histogram. For a 2-D array, the zeroth
        axis is the list of samples and the next axis are the dimensions of
        the space.

    :param labels: ``ndim`` (optional)
        A list of names for the dimensions.

    :param truths: ``ndim`` (optional)
        A list of reference values to indicate on the plots.

    :param truth_color: (optional)
        A ``matplotlib`` style color for the ``truths`` makers.

    :param quantiles: (optional)
        A list of fractional quantiles to show on the 1-D histograms as
        vertical dashed lines.

    :param scale_hist: (optional)
        Should the 1-D histograms be scaled in such a way that the zero line
        is visible?

    """

    # Deal with 1D sample lists.
    xs = np.atleast_1d(xs)
    if len(xs.shape) == 1:
        xs = np.atleast_2d(xs)
    else:
        assert len(xs.shape) == 2, "The input sample array must be 1- or 2-D."
        xs = xs.T
    assert xs.shape[0] <= xs.shape[1], "I don't believe that you want more " \
                                       "dimensions than samples!"

    K = len(xs)
    factor = 2.0           # size of one side of one panel
    lbdim = 0.5 * factor   # size of left/bottom margin
    trdim = 0.05 * factor  # size of top/right margin
    whspace = 0.05         # w/hspace size
    plotdim = factor * K + factor * (K - 1.) * whspace
    dim = lbdim + plotdim + trdim
    fig = pl.figure(figsize=(dim, dim))
    lb = lbdim / dim
    tr = (lbdim + plotdim) / dim
    fig.subplots_adjust(left=lb, bottom=lb, right=tr, top=tr,
                        wspace=whspace, hspace=whspace)

    if extents is None:
        # LINEAR-SCALE
        extents = [[x.min(), x.max()] for x in xs]
        ##log##
        #extents = [[np.log10(x.min()), np.log10(x.max())] for x in xs]

    for i, x in enumerate(xs):
        # Plot the histograms.
        ax = fig.add_subplot(K, K, i * (K + 1) + 1)
        n, b, p = ax.hist(x, bins=kwargs.get("bins", 50), range=extents[i],
                histtype="step", color=kwargs.get("color", "red"), linewidth=2.0)
        #### log10###
        # n, b, p = ax.hist(np.log10(x), bins=kwargs.get("bins", 50), range=extents[i],
        #         histtype="step", color=kwargs.get("color", "black"), linewidth=2.0)
        ####============================================================================
        values = credible_interval.from_histogram(n, b,[0.6827, 0.9545])
        #values = credible_interval.from_histogram(n, b,[0.3173, 0.0455])
        peak_location = b[np.argmax(n)]
        nearest_index1 = np.argmin(np.abs(b-values[0][0])) #from left
        nearest_index2 = np.argmin(np.abs(b-values[0][1]))  #from right
        nearest_index3 = np.argmin(np.abs(b-peak_location))
        ax.plot([(values[0][0]+((b[1]-b[0])/2.)),(values[0][0]+((b[1]-b[0])/2.))],[0,n[nearest_index1]],color='r',linestyle='--')
        ax.plot([(values[0][1]+((b[1]-b[0])/2.)),(values[0][1]+((b[1]-b[0])/2.))],[0,n[nearest_index2]],color='r',linestyle='--')
        ax.plot([(peak_location+((b[1]-b[0])/2.)),(peak_location+((b[1]-b[0])/2.))],[0,n[nearest_index3]],color='r',linestyle='-')
        ####============================================================================
        #ax.plot([np.log10(0.9),np.log10(0.9)],[0,n[nearest_index3]],color='red',linestyle='--')
        #ax.plot([np.log10(1.0),np.log10(1.0)],[0,n[nearest_index3]],color='green',linestyle='-')
        
        if truths is not None:
            ax.axvline(truths[i], color='black',zorder=102)
            #ax.axvline(truths[i], color=truth_color)

        # Plot quantiles if wanted.
        if len(quantiles) > 0:
            xsorted = sorted(x)
            for q in quantiles:
                ax.axvline(xsorted[int(q * len(xsorted))], ls="dashed",
                           color=kwargs.get("color", "k"))

        # Set up the axes.
        ax.set_xlim(extents[i])
        if scale_hist:
            maxn = np.max(n)
            ax.set_ylim(-0.1 * maxn, 1.1 * maxn)
        else:
            ax.set_ylim(0, 1.1 * np.max(n))
        ax.set_yticklabels([])
        ax.xaxis.set_major_locator(MaxNLocator(5))

        # Not so DRY.
        if i < K - 1:
            ax.set_xticklabels([])
        else:
            [l.set_rotation(45) for l in ax.get_xticklabels()]
            if labels is not None:
                #print("\n=====================\n xlabel: ",labels[i],"\n===================\n")
                ax.set_xlabel(labels[i], fontsize=24)
                ax.xaxis.set_label_coords(0.5, -0.3)

        for j, y in enumerate(xs[:i]):
            # ````````````````````````````````````````````````````````````````````````````````````````````````````````````
            # if labels is not None: print("--------------------------\n xlabel: ",labels[j],"\n---------------------------")
            # if labelsy is not None: print("--------------------------\n ylabel: ",labelsy[i],"\n---------------------------")
            # ````````````````````````````````````````````````````````````````````````````````````````````````````````````
            ax = fig.add_subplot(K, K, (i * K + j) + 1)
            #hist2d(y, x, ax=ax, extent=[extents[j], extents[i]], **kwargs)
            # ```````````````````````````````````````````````````````````````
            try: 
                hist2d(y, x, ax=ax, extent=[extents[j], extents[i]], **kwargs)
            except:
                # Attempting to catch the following error:
                # "RuntimeError: Failed to converge after 100 iterations."
                # If so, leaving this subplot blank
                print("This one failed!")
            # ```````````````````````````````````````````````````````````````

            if truths is not None:
                ax.plot(truths[j], truths[i], "o", color='black', zorder=102)
                ax.axvline(truths[j], color='black', zorder=102)
                ax.axhline(truths[i], color='black',zorder=102)

            ax.xaxis.set_major_locator(MaxNLocator(5))
            ax.yaxis.set_major_locator(MaxNLocator(5))

            if i < K - 1:
                ax.set_xticklabels([])
            else:
                [l.set_rotation(45) for l in ax.get_xticklabels()]
                if labels is not None:
                    ax.set_xlabel(labels[j], fontsize=24)
                    ax.xaxis.set_label_coords(0.5, -0.3)


            if j > 0:
                ax.set_yticklabels([])
            else:
                [l.set_rotation(45) for l in ax.get_yticklabels()]
                if labelsy is not None:
                    ax.set_ylabel(labelsy[i], fontsize=24)
                    ax.yaxis.set_label_coords(-0.3, 0.5)

    return fig


def error_ellipse(mu, cov, ax=None, factor=1.0, **kwargs):
    """
    Plot the error ellipse at a point given it's covariance matrix.

    """
    # some sane defaults
    facecolor = kwargs.pop('facecolor', 'none')
    edgecolor = kwargs.pop('edgecolor', 'k')

    x, y = mu
    U, S, V = np.linalg.svd(cov)
    theta = np.degrees(np.arctan2(U[1, 0], U[0, 0]))
    ellipsePlot = Ellipse(xy=[x, y],
            width=2 * np.sqrt(S[0]) * factor,
            height=2 * np.sqrt(S[1]) * factor,
            angle=theta,
            facecolor=facecolor, edgecolor=edgecolor, **kwargs)

    if ax is None:
        ax = pl.gca()
    ax.add_patch(ellipsePlot)


def hist2d(x, y, *args, **kwargs):
    """
    Plot a 2-D histogram of samples.

    """
    ax = kwargs.pop("ax", pl.gca())

    extent = kwargs.pop("extent", [[x.min(), x.max()], [y.min(), y.max()]])
    bins = kwargs.pop("bins", 50)
    color = kwargs.pop("color", "k")
    plot_datapoints = kwargs.get("plot_datapoints", True)

    cmap = cm.get_cmap("gray")
    cmap._init()
    cmap._lut[:-3, :-1] = 0.
    cmap._lut[:-3, -1] = np.linspace(1, 0, cmap.N)

    #-------------------------------------------------------------------------------------
    N_levels = 2

    # -------------------------------
    # Creating the interpolation grid
    # -------------------------------
    # Number of grid points
    Npts = 100j
    
    # X Grid
    # ----------------------
    # Find grid limits
    xminx2 = x.min()
    xmaxx2 = x.max()
    yminx2 = y.min()
    ymaxx2 = y.max()
    # Create the Grid
    #Xx, Yx = np.mgrid[xminx:xmaxx:0.001, yminx:ymaxx:0.001] # 2D Version
    Xx2, Yx2 = np.mgrid[xminx2:xmaxx2:Npts, yminx2:ymaxx2:Npts] # 2D Version
    positionsx2 = np.vstack([Xx2.ravel(), Yx2.ravel()]) # 2xN Version
    
    # Make Log-Space KDE
    # ------------------
    # Data Point Values
    # LINEAR-SCALE DATA
    valuesx2_lin = np.vstack( [x,y] )
    #### log 10 ###
    #valuesx2_log = np.vstack( [np.log10(x),y] )
    # Make the X kernel from the X values array
    #kernelx2_lin = stats.gaussian_kde(valuesx2_lin)  # this is the Gaussian KDE
    try:
        kernelx2_lin = stats.gaussian_kde(valuesx2_lin)  # this is the Gaussian KDE
    except:
        pass
    
    # Sample KDE For Contours
    # -----------------------
    # LINEAR-SPACED X,Y VALUES
    Xx2_lin_vals = np.linspace(xminx2, xmaxx2, num=np.real(Npts*(-1j)), endpoint=True)
    # Log-spaced x,y values
    ###log10###
    #Xx2_log_vals = np.linspace(np.log10(xminx2), np.log10(xmaxx2), num=np.real(Npts*(-1j)), endpoint=True)
    # LINEAR-SPACED X,Y VALUES
    Yx2_lin_vals = np.linspace(yminx2, ymaxx2, num=np.real(Npts*(-1j)), endpoint=True)
    # Make into meshgrid arrays
    Xx2_lin, Yx2_lin = np.meshgrid(Xx2_lin_vals, Yx2_lin_vals)
    # print('\n````````````````````````````````')
    # print('Xx2_lin.min(), Xx2_lin.max()')
    # print(Xx2_lin.min(), Xx2_lin.max())
    # print('log10(Xx2_lin.min()), log10(Xx2_lin.max())')
    # print(np.log10(Xx2_lin.min()), np.log10(Xx2_lin.max()))

    # print('\nYx2_lin.min(), Yx2_lin.max()')
    # print(Yx2_lin.min(), Yx2_lin.max())
    # print('````````````````````````````````\n')

    # Format that Gaussian KDE can understand
    positionsx2_lin = np.vstack([Xx2_lin.ravel(), Yx2_lin.ravel()]) # 2xN Version

    # Get Samples of KDE for Contours
    try:
        Zkernelx2_lin = np.reshape( kernelx2_lin(positionsx2_lin).T, Xx2_lin.shape)
    except:
        pass

    #sigma_levels_X2_lin = ( kdestats.confmap(Zkernelx2_lin, 0.68), )
    try:
        #sigma_levels_X2_lin = ( kdestats.confmap(Zkernelx2_lin, 0.68), )
        sigma_levels_X2_lin = ( kdestats.confmap(Zkernelx2_lin, 0.95), )
    except:
        pass

    # Plot Contours, Points
    # ---------------------
    # Extent Array
    # LINEAR-SCALED EXTENTS
    extentx2_lin = [xminx2, xmaxx2, yminx2, ymaxx2]
    ###log10###
    #extentx2_log = [np.log10(xminx2), np.log10(xmaxx2), yminx2, ymaxx2]
    # Contours, Points
    
    ax.locator_params(axis='x', nbins=4)
    
    # ------------------
    # Plotting
    # ------------------
    
    # X Plot
    # --------------
    #x_points_color = '#444444'
    #x_points_color = 'red'
    x_points_color = '#1E90FF'
    x_contours_color = 'red'
    #x_contours_color = 'black'
    #x_points_color = 'blue'
    #x_contours_color = 'navy'
    
    
    #-------------------------------------------------------------------------------------
#    X = np.linspace(extent[0][0], extent[0][1], bins + 1)
#    Y = np.linspace(extent[1][0], extent[1][1], bins + 1)
#    H, X, Y = np.histogram2d(x.flatten(), y.flatten(), bins=(X, Y))
#
#    V = 1.0 - np.exp(-0.5 * np.arange(0.5, 2.1, 0.5) ** 2)
#    Hflat = H.flatten()
#    inds = np.argsort(Hflat)[::-1]
#    Hflat = Hflat[inds]
#    sm = np.cumsum(Hflat)
#    sm /= sm[-1]
#
#    for i, v0 in enumerate(V):
#        try:
#            V[i] = Hflat[sm <= v0][-1]
#        except:
#            V[i] = Hflat[0]
#
#    X1, Y1 = 0.5 * (X[1:] + X[:-1]), 0.5 * (Y[1:] + Y[:-1])
#    X, Y = X[:-1], Y[:-1]

    if plot_datapoints:
        # Kernel Density Estimate IMAGE
        # Kernel Density Estimate CONTOURS
        try:
            ax.contour(Xx2_lin, Yx2_lin, Zkernelx2_lin, levels=sigma_levels_X2_lin, linewidths=2, alpha=1, colors=x_contours_color, zorder=101, extent=extentx2_lin )
        except:
            pass
#n_skip=int(len(x)/5000)
        # LINEAR-SCALE DATA
### plot points, or not, using this line below #######
        ax.plot(x, y, lw=0, marker='s',markersize=2,mew=0.2,mec=x_points_color, mfc='none',zorder=99,alpha=1)
    ## Thin out the points plotted:
#ax.plot(x[::n_skip], y[::n_skip], lw=0, marker='s',markersize=2,mew=0.2,mec=x_points_color, mfc='none',zorder=100,alpha=1)


        ### use log10 scaleing below ###
        #ax.plot(np.log10(x), y, lw=0, marker='s',markersize=2,mew=0.2,mec=x_points_color, mfc='none',zorder=100,alpha=1)
        #ax.plot(esigma_lowx,esigma_hix, lw=0, marker='+',markersize=3,mew=0.5,mec=x_points_color, mfc='none',zorder=1,alpha=1)  ## NEW
        # CENTER
        #ax1.plot(max_coords_X[0],max_coords_X[1], marker='.', markersize=5, mew=2, mec='navy', mfc='none', zorder=200)
    

#    ax.pcolor(X, Y, H.max() - H.T, cmap=cmap)
#    ax.contour(X1, Y1, H.T, V, colors=color)

    data = np.vstack([x, y])
    mu = np.mean(data, axis=1)
    cov = np.cov(data)
    if kwargs.pop("plot_ellipse", False):
        error_ellipse(mu, cov, ax=ax, edgecolor="r", ls="dashed")
        
    # Scaling
    ax.set_xscale('linear')
    ax.set_yscale('linear')
#    ax.set_xlim(extent[0])
#    ax.set_ylim(extent[1])
