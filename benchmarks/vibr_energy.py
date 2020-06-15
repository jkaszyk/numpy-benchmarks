#from: http://stackoverflow.com/questions/17112550/python-and-numba-for-vectorized-functions
def data(np):
    N = 100000 
    a, b, c = np.random.rand(N), np.random.rand(N), np.random.rand(N)
    return (a,b,c)
#run: vibr_energy(a, b, c)

#pythran export vibr_energy(float64[], float64[], float64[])
numpy = None
def vibr_energy(harmonic, anharmonic, i):
    return numpy.exp(-harmonic * i - anharmonic * (i ** 2))

def func(np, data):
    numpy = np
    return vibr_energy(*data)
