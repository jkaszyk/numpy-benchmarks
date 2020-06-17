#from: http://wiki.scipy.org/Cookbook/Theoretical_Ecology/Hastings_and_Powell
def data(np):
    y = np.random.rand(3) 
    args = np.random.rand(7)
    return (y, args)
#run: hasting(y, *args)

# NOPE
np = None
#pythran export hasting(float [], float, float, float, float, float, float, float)
def hasting(y, t, a1, a2, b1, b2, d1, d2):
    yprime = np.empty((3,))
    yprime[0] = y[0] * (1. - y[0]) - a1*y[0]*y[1]/(1. + b1 * y[0])
    yprime[1] = a1*y[0]*y[1] / (1. + b1 * y[0]) - a2 * y[1]*y[2] / (1. + b2 * y[1]) - d1 * y[1]
    yprime[2] = a2*y[1]*y[2]/(1. + b2*y[1]) - d2*y[2]
    return yprime

def func(np, data):
    return hasting(data[0], *data[1])
