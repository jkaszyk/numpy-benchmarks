#from: https://groups.google.com/forum/#!topic/parakeet-python/p-flp2kdE4U
def data(np):
   d = 10 
   re = 5 
   params = (d, re, np.ones((2*d, d+1, re)), np.ones((d, d+1, re)),  np.ones((d, 2*d)), np.ones((d, 2*d)), np.ones((d+1, re, d)), np.ones((d+1, re, d)), 1)
   return params
#run: slowparts(*params)

#pythran export slowparts(int, int, float [][][], float [][][], float [][], float [][], float [][][], float [][][], int)
np = None
def slowparts(d, re, preDz, preWz, SRW, RSW, yxV, xyU, resid):
    """ computes the linear algebra intensive part of the gradients of the grae
    """
    fprime = lambda x: 1 - np.power(np.tanh(x), 2)

    partialDU = np.zeros((d+1, re, 2*d, d))
    for k in range(2*d):
        for i in range(d):
            partialDU[:,:,k,i] = fprime(preDz[k]) * fprime(preWz[i]) * (SRW[i,k] + RSW[i,k]) * yxV[:,:,i]
    
    return partialDU

def func(inp, data):
    np = inp
    return slowparts(*data)
