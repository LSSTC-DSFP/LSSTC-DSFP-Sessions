import numpy as np
import scipy.signal
import imageProc

class IdArray(object):
    def __init__(self, n):
        self._data = np.zeros(n + 2, dtype=int)
        
    def __getitem__(self, i):
        return self._data[i + 1]

    def __setitem__(self, i, val):
        self._data[i + 1] = val
        
    def clear(self):
        self._data[:] = 0
        
class Span(object):
    def __init__(self, y, x0, x1=None):
        self.y = y
        self.x0 = x0
        self.x1 = x1
        
class Footprint(object):
    def __init__(self, fId):
        self.id = fId
        self.spans = []
        self.centroid = None
        self.npix = None

def findPeakInFootprint(image, foot):
    s = foot.spans[0]
    ypeak = s.y
    xpeak = s.x0

    max = image[s.y, s.x0]
    npix = 0

    for s in foot.spans:
        for x in range(s.x0, s.x1):
            npix += 1
            val = image[s.y, x]
            if val > max:
                xpeak = x
                ypeak = s.y

    return xpeak, ypeak, npix

def findObjects(data, threshold, grow=0):
    h, w = data.shape
    
    nextId = 1
    aliases = {}
    spans = {}

    idc, idp = [IdArray(w), IdArray(w)]
    for y in range(h):
        idc, idp = idp, idc
        idc.clear()

        drow = data[y]    
        for x in range(w):
            if drow[x] > threshold:
                if x == 0 or x > 0 and drow[x - 1] < threshold:
                    span = Span(y, x, w)

                if idc[x - 1] > 0:
                    idc[x] = idc[x - 1]
                elif idp[x - 1] > 0:
                    idc[x] = idp[x - 1]
                elif idp[x] > 0:
                    idc[x] = idp[x]
                elif idp[x + 1] > 0:
                    idc[x] = idp[x + 1]
                else:
                    spans[nextId] = []
                    span = Span(y, x, w)
                    idc[x] = nextId
                    nextId += 1

                if idp[x + 1] and idc[x] != idp[x + 1]:
                    aliases[idc[x]] = idp[x + 1]
            else:
                if idc[x - 1] > 0:
                    span.x1 = x
                    spans[idc[x - 1]].append(span)
    #
    # Remove cycles in the aliases -- you get this if you have objects with holes in the middle
    #
    for objId in spans:
        resolved = set()
        while objId in aliases:
            nobjId = aliases[objId]
            if nobjId in resolved:
                del aliases[objId]
                break
            resolved.add(nobjId)
                
            objId = nobjId

    nextId = 1
    footprints = {}
    footObjIds = {}    # mapping from IDs used for spans to footprint Ids

    for objId, spans in spans.items():
        while objId in aliases:
            objId = aliases[objId]

        if objId in footObjIds:
            foot = footprints[footObjIds[objId]]
        else:
            fId = nextId; nextId += 1
            footObjIds[objId] = fId

            foot = Footprint(fId)
            footprints[fId] = foot

        foot.spans += spans
    del spans
    #
    # Grow footprints by given number of pixels
    if grow:
        footprints = growFootprints(data.shape, footprints, grow)

    if not grow:
        for i, foot in footprints.items():
            xc, yc, npix = findPeakInFootprint(data, foot)
            foot.centroid = (xc, yc)
            foot.npix = npix

    return footprints

def growFootprints(shape, footprints, radius):
    size = int(radius + 1)
    x, y = np.mgrid[-size:size+1, -size:size+1]
    disk = np.zeros([2*size + 1, 2*size + 1])
    disk[np.hypot(x, y) <= radius] = 1

    tmp = footprintToIdImage(shape, footprints)
    tmp = scipy.signal.convolve(tmp, disk, mode='same')

    return findObjects(tmp, 1, grow=0)

def setMaskFromFootprints(da, footprints, bitName):
    bitMask = imageProc.maskPlanes[bitName]
    
    for i, foot in footprints.items():
        for span in foot.spans:
            da.mask[span.y, span.x0:span.x1] |= bitMask

def footprintToIdImage(shape, footprints):
    """Return an image with the given shape, with pixels set to the Footprint IDs"""
    data = np.zeros(shape)
    for foot in footprints.values():
        for span in foot.spans:
            data[span.y, span.x0:span.x1] = foot.id
            
    return data
