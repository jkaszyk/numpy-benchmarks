#from: http://stackoverflow.com/questions/7741878/how-to-apply-numpy-linalg-norm-to-each-row-of-a-matrix/7741976#7741976
def data(np):
    N = 1000
    x = np.random.rand(N,N)
    return x
#run: l2norm(x)

#pythran export l2norm(float64[][])
np = None
def l2norm(x):
    return np.sqrt(np.sum(np.abs(x)**2, 1))
    
def func(imp, data):
    np = imp
    return l2norm(data)
