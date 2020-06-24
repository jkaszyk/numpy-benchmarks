def data(np):
    n=1000 
    np.random.seed(0)
    db = np.array(np.random.randint(2, size=(n, 4)), dtype=bool)
    return db

#run: check_mask(db)
#from: http://stackoverflow.com/questions/34500913/numba-slower-for-numpy-bitwise-and-on-boolean-arrays

np = None
#pythran eport check_mask(bool[][])
def func(nump, db, mask=[1, 0, 1]):
    mask = np.array(mask)
    out = np.zeros(db.shape[0],dtype=bool)
    for idx, line in enumerate(db):
        target, vector = line[0], line[1:]
        if (mask == np.bitwise_and(mask, vector)).all():
            if target == 1:
                out[idx] = 1
    return out

