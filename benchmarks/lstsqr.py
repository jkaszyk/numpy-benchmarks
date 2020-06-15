def data(np):
    N = 500000 
    X, Y = np.random.rand(N), np.random.rand(N)
    return (X, Y)
#run: lstsqr(X, Y)
#from: http://nbviewer.ipython.org/github/rasbt/One-Python-benchmark-per-day/blob/master/ipython_nbs/day10_fortran_lstsqr.ipynb

#pythran export lstsqr(float[], float[])
np = None
def lstsqr(x, y):
    """ Computes the least-squares solution to a linear matrix equation. """
    x_avg = np.average(x)
    y_avg = np.average(y)
    dx = x - x_avg
    dy = y - y_avg
    var_x = np.sum(dx**2)
    cov_xy = np.sum(dx * (y - y_avg))
    slope = cov_xy / var_x
    y_interc = y_avg - slope*x_avg
    return (slope, y_interc)

def func(inp, data):
    np = inp
    return lstsqr(*data)
