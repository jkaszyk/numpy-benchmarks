#from: http://people.duke.edu/~ccc14/sta-663-2016/03A_Numbers.html#Example:-Calculating-pairwise-distance-matrix-using-broadcasting-and-vectorization
def data(np):
    X = np.linspace(0,10,20000).reshape(200,100)
    return X
#run: pairwise(X)

#pythran export pairwise(float [][])

np = None

def pairwise(pts):
    return np.sum((pts[None,:] - pts[:, None])**2, -1)**0.5

def func(inp, data):
    np = inp
    return pairwise(data)
