"""Utilities used in Robert Lupton's Practical Sessions

These replace LSST stack code, although with different APIs
"""

import numpy as np
import matplotlib.pyplot as plt

class CCD:
    """Describe a CCD's properties"""
    rawWidth = 552                      # number of pixels digitised per parallel transfer
    tau_s = 13.92e-6                    # Time for one serial transfer (s)
    tau_p = 222.72e-6                   # Time for one parallel transfer (s)

    def __init__(self):
        pass

class BBox:
    """Simple Bounding Box class for DSFP"""

    def __init__(self, bbox):
        self.x0 = bbox[0][0]
        self.y0 = bbox[0][1]
        self.x1 = self.x0 + bbox[1][0]
        self.y1 = self.y0 + bbox[1][1]

        self.size = bbox[1]
        
class Image:
    """Simple Image class for DSFP"""
    def __init__(self, fileName):
        biasData = np.load(fileName)
        self.image = biasData["image"]
        self.amps = []
        for bbox in biasData['bboxes']:
            self.amps.append(BBox(bbox))
            
    def getAmpImage(self, amp):
        """Return the image of a single amplifier, passed either then index or a BBox"""
        try:
            amp.x0
        except AttributeError:
            amp = self.amps[amp]

        return self.image[amp.y0:amp.y1, amp.x0:amp.x1]

def imshow(image, nsigma=2, *args, **kwargs):
    """Like pyplot.imshow but with sane defaults for image display
    
    If vmin or vmax is omitted, use a linear stretch from nsigma[0]..nsigma[1]  (or +- nsigma if a scalar)
    """
    if 'aspect' not in kwargs:
        kwargs['aspect'] = 'equal'
    if 'cmap' not in kwargs:
        kwargs['cmap'] = 'gray'
    if 'interpolation' not in kwargs:
        kwargs['interpolation'] = 'none'
    if 'origin' not in kwargs:
        kwargs['origin'] = 'lowerleft'
        
    if not ('vmin' in kwargs and'vmax' in kwargs):
        q1, med, q3 = np.percentile(image, [25, 50, 75])
        stdev = 0.741*(q3 - q1)
        try:
            vmin, vmax = nsigma
        except TypeError:
            vmin, vmax = -nsigma, nsigma
            
        kwargs['vmin'] = med + vmin*stdev
        kwargs['vmax'] = med + vmax*stdev

    plt.imshow(image, *args, **kwargs)
