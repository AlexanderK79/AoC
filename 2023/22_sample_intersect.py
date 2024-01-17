import numpy as np
a = np.array([[ 1, 2, 3],
              [ 4, 5, 6],
              [ 7, 8, 9],
              [10, 11, 12]])    

def shift_array(array, place):
    new_arr = np.roll(array, place, axis=0)
    new_arr[:place] = np.zeros((new_arr[:place].shape))
    return new_arr

def shift(xs, n):
    e = np.empty_like(xs)
    if n >= 0:
        e[:n] = np.nan
        e[n:] = xs[:-n]
    else:
        e[n:] = np.nan
        e[:n] = xs[-n:]
    return e


print(a)
print(shift(a,2))
print(shift(a,-1))
# array([[ 0,  0,  0],
#        [ 0,  0,  0],
#        [ 1,  2,  3],
#        [ 4,  5, 6]])

