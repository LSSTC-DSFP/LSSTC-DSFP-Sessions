"""
Utilities for RHL's workshop at the DSFP, Chicago, July 2016
"""
import math, os, sys
import matplotlib.pyplot as pyplot
import numpy as np
import imageProc

try:
    _mpFigures
except NameError:
    _mpFigures = {0 : None}              # matplotlib (actually pyplot) figures
    eventHandlers = {}                  # event handlers for matplotlib figures

def getMpFigure(fig=None, clear=True):
    """Return a pyplot figure(); if fig is supplied save it and make it the default
    fig may also be a bool (make a new figure) or an int (return or make a figure (1-indexed;
    python-list style -n supported)
    """

    if not pyplot:
        raise RuntimeError("I am unable to plot as I failed to import matplotlib")

    if isinstance(fig, bool):       # we want a new one
        fig = len(_mpFigures) + 1    # matplotlib is 1-indexed

    if isinstance(fig, int):
        i = fig
        if i == 0:
            raise RuntimeError("I'm sorry, but matplotlib uses 1-indexed figures")
        if i < 0:
            try:
                i = sorted(_mpFigures.keys())[i] # simulate list's [-n] syntax
            except IndexError:
                if _mpFigures:
                    print >> sys.stderr, "Illegal index: %d" % i
                i = 1

        def lift(fig):
            fig.canvas._tkcanvas._root().lift() # == Tk's raise, but raise is a python reserved word

        if _mpFigures.has_key(i):
            try:
                lift(_mpFigures[i])
            except Exception, e:
                del _mpFigures[i]
                
        if not _mpFigures.has_key(i):
            for j in range(1, i):
                getMpFigure(j, clear=False)
                
            _mpFigures[i] = pyplot.figure()
            #
            # Modify pyplot.figure().show() to make it raise the plot too
            #
            def show(self, _show=_mpFigures[i].show):
                _show(self)
                try:
                    lift(self)
                except Exception, e:
                    pass
            # create a bound method
            import types
            _mpFigures[i].show = types.MethodType(show, _mpFigures[i], _mpFigures[i].__class__)

        fig = _mpFigures[i]

    if not fig:
        i = sorted(_mpFigures.keys())[0]
        if i > 0:
            fig = _mpFigures[i[-1]]
        else:
            fig = getMpFigure(1)

    if clear:
        fig.clf()

    pyplot.figure(fig.number)           # make it active

    return fig

class Data(object):
    def __init__(self, image=None, mask=None, variance=None, shape=None):
        if image is not None:
            if shape:
                assert image.shape == shape
            else:
                shape = image.shape
        if mask is not None:
            assert mask.shape == shape
        if variance is not None:
            assert variance.shape == shape
                
        if shape:
            self.image = image if image is not None else np.zeros(shape)
            self.mask = mask if mask is not None  else np.zeros(shape, dtype="uint16")
            self.variance = variance if variance is not None else np.zeros_like(self.image)
        else:
            self.image, self.mask, self.variance = None, None, None
            
        self.truth = None

    def read(self, dirName="./Data", readImage=True, readEimage=True, readRaw=False):
        self.image, self.mask, self.truth = readData(dirName, readImage, readEimage, readRaw)
        q25, q75 = np.percentile(self.image.flat, [25, 75])
        self.variance = self.image + (0.741*(q75 - q25))**2        

    def copy(self, image=None, mask=None):
        cp = Data(None)

        cp.image = image if image is not None else None if self.image is    None else self.image.copy()
        cp.mask =  mask  if mask  is not None else None if self.mask  is    None else self.mask.copy()
        cp.variance =                              None if self.variance is None else self.variance.copy()
        cp.truth =                                 None if self.truth is    None else self.truth.copy()

        if cp.mask is None:
            cp.mask = np.zeros_like(cp.image, dtype="uint16")

        return cp

    def clearMaskPlane(self, bitName=None):
        """Clear the bitName (e.g. INTRP) bit in the mask"""
        if bitName:
            self.mask &= ~imageProc.maskPlanes[bitName]
        else:
            self.mask = 0x0

    def setMaskPlane(self, threshold, bitName, clear=False):
        """Set the bitName (e.g. INTRP) bit in the mask when the image is above threshold;
        if clear is True, unset the bitplane first (see also clearMaskPlane)"""
        if clear:
            self.clearMaskPlane(bitName)

        self.mask[self.image > threshold] |= imageProc.maskPlanes[bitName]

def readData(dirName="./Data", image=True, eimage=True, readRaw=False):
    ims = []
    if image:
        for f in ("raw" if readRaw else "image", "mask",):
            ims.append(np.load(os.path.join(dirName, "%s.npy" % f)))
    else:
        ims += [None, None]
        
    if eimage:
        ims.append(np.load(os.path.join(dirName, "eimage.npy")))
    else:
        ims.append(None)

    return ims

def mtv(im, I0=0, b=1, mask=None, isMask=False, alpha=None, clear=True, fig=None, evData=None):
    """Display an image, using an asinh stretch (softened by b)"""
    fig = pyplot.figure(fig)

    try:
        mtv(im.image, I0=I0, b=b, fig=fig.number, evData=im)
        mtv(im.mask, isMask=True, alpha=alpha, fig=fig.number, clear=False)

        return
    except AttributeError:
        if not isMask:
            evData = im
    
    if isMask:
        if alpha is None:
            alpha = 0.7

        maskPlanes = imageProc.maskPlanes
        
        r = (im & (maskPlanes["BAD"] | maskPlanes["CR"])) != 0
        g = (im & (maskPlanes["INTRP"] | maskPlanes["SATUR"] | maskPlanes["EDGE"])) != 0
        b = (im & (maskPlanes["DETECTED"] | maskPlanes["EDGE"])) != 0

        alpha = alpha*np.ones_like(im)
        alpha[im == 0] = 0

        lim4 = np.dstack([r, g, b, alpha]).reshape([im.shape[0], im.shape[1], 4])
        pyplot.imshow(lim4, origin="lower", interpolation="nearest")
    else:
        if b == 0:
            b = 1e-10
        ax = pyplot.imshow(np.arcsinh((im - I0)/b), origin='lower', interpolation='nearest',
                           cmap=pyplot.cm.gray)

        if mask is not None:
            mtv(mask, isMask=True, alpha=alpha, fig=fig.number)

    if evData is not None:
        axes = pyplot.axes()
        myText = axes.text(0.05, 1.05, 'Press "return" to show intensity here',
                           transform=axes.transAxes, va='top')

        global eventHandlers
        eventHandlers[fig] = EventHandler((evData, myText), fig)

class EventHandler(object):
    """A class to handle key strokes with matplotlib displays"""
    def __init__(self, data, fig):
        self.fig = fig

        im, text = data
        try:
            self.image = im.image
            self.mask = im.mask
        except AttributeError:
            self.image = im
            self.mask = None

        self.text = text

        self.cid = self.fig.canvas.mpl_connect('key_press_event', self)

    def __call__(self, ev):
        if ev.key != "\n" and ev.key != "enter":
            return

        if not (ev.xdata and ev.ydata):
            return
        x = np.clip(int(ev.xdata + 0.5), 0, self.image.shape[0])
        y = np.clip(int(ev.ydata + 0.5), 0, self.image.shape[1])
        str = "(%4d, %4d) %9.2f" % (x, y, self.image[y, x])
        if hasattr(self, "mask") and self.mask is not None:
            str += " 0x%02x" % (self.mask[y, x])

            mval = self.mask[y, x]
            for k, v in imageProc.maskPlanes.items():
                if mval & v:
                    str += " %s" % k

        self.text.set_text(str)
        self.fig.canvas.draw()
        
