from multiprocessing import Pool
import numpy as np
import time

def divide_by_gain(number, gain=8):
    return number/gain
    
if __name__ == '__main__':
    pixel_data = np.random.rand(4000000)
    tstart = time.time()
    with Pool() as p:
        res = p.map(divide_by_gain,pixel_data)
    trun = time.time() - tstart
    print('It takes {:.6f} s to correct for the gain'.format(trun))