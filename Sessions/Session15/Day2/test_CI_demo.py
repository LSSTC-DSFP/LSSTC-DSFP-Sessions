from CI_demo import distance, average
import numpy as np

def test_distance():
    dis = distance(np.array([0,0]), np.array([2,2]))
    print(dis)
    assert dis == 2
    
def test_average():
    avg = average([1,1])
    assert avg == 1