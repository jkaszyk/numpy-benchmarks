def data(np):
    np.random.seed(0)
    s=np.random.randn(2**16)+np.random.randn(2**16)*1.j 
    sc=np.random.choice(s, 32)
    return (s, sc)
#run: make_decision(s, sc)
#from: https://github.com/serge-sans-paille/pythran/issues/801

np = None
#pythran export make_decision(complex128[], complex128[])
def make_decision(E, symbols):
    L = E.shape[0]
    syms_out = np.zeros(L, dtype=E.dtype)
    for i in range(L):
        im = np.argmin(abs(E[i]-symbols)**2)
        syms_out[i] = symbols[im]
    return syms_out

def func(inp, data):
    np=inp
    return make_decision(*data)
