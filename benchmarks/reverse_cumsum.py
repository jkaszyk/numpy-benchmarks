#from: http://stackoverflow.com/questions/16541618/perform-a-reverse-cumulative-sum-on-a-numpy-array
#pythran export reverse_cumsum(float[])
def data(np):
    r = np.random.rand(1000000)
    return r
#run: reverse_cumsum(r)
np = None
def reverse_cumsum(x):
    return np.cumsum(x[::-1])[::-1]

def func(inp, data):
    np=inp
    return reverse_cumsum(data)
