#from: http://stackoverflow.com/questions/13815719/creating-grid-with-numpy-performance
#pythran export create_grid(float [])
def data(np):
    import numpy as np 
    N = 800 
    x = np.arange(0,1,1./N)
    return x
#run: create_grid(x)
def func(np, x):
    N = x.shape[0]
    z = np.zeros((N, N, 3))
    z[:,:,0] = x.reshape(-1,1)
    z[:,:,1] = x
    fast_grid = z.reshape(N*N, 3)
    return fast_grid
