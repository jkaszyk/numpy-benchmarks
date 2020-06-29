#from: https://stackoverflow.com/questions/55854611/efficient-way-of-vectorizing-distance-calculation/55877642#55877642
def data(np):
    N = 800
    x = np.random.rand(N,N)
    y = np.random.rand(N,N)
    return (x,y)
#run: l1norm(x, y)

#pythran export l1norm(float64[][], float64[:,:])
np = None
def l1norm(x, y):
    return np.sum(np.abs(x[:, None, :] - y), axis=-1)

def func(imp, data):
    np = imp
    return l1norm(*data)
