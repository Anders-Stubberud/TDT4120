import numpy as np
from scipy.spatial import Delaunay
from collections import defaultdict

coords = [(0, 1), (0, 2), (1, 2), (2, 1)]
delauney = Delaunay(coords)
print(delauney.simplices)
