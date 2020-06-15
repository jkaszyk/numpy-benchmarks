def data(np):
    r = np.arange(1000000, dtype=float)
    return r
#run: rosen(r)
np = None
#pythran export rosen(float[])

def rosen(x):
    t0 = 100 * (x[1:] - x[:-1] ** 2) ** 2
    t1 = (1 - x[:-1]) ** 2
    return np.sum(t0 + t1)

def func(inp, data):
    np = inp
    return rosen(data)
