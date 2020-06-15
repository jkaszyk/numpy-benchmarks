#from: http://stackoverflow.com/questions/4651683/numpy-grouping-using-itertools-groupby-performance
def data(np):
    N = 500000 
    np.random.seed(0)
    values = np.array(np.random.randint(0,3298,size=N),dtype='u4') 
    values.sort()
    return values
#run: grouping(values)

np = None

#pythran export grouping(uint32 [])

def grouping(values):
    diff = np.concatenate(([1], np.diff(values)))
    idx = np.concatenate((np.where(diff)[0], [len(values)]))
    return values[idx[:-1]], np.diff(idx)

def func(imp, data):
    np = imp
    return grouping(data)
