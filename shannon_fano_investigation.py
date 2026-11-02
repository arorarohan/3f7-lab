from itertools import groupby
from vl_codes import shannon_fano, vl_encode, bytes2bits, bits2bytes, vl_decode
import trees
from math import log2

def H(pr):
    """calculate entropy in bits"""
    return sum([pr[a] * log2(1/pr[a]) for a in pr])


if __name__ == '__main__':
    #load hamlet
    f = open('hamlet.txt', 'r')
    hamlet = f.read()
    f.close()

    frequencies = dict([(key, len(list(group))) for key, group in groupby(sorted(hamlet))])
    Nin = sum([frequencies[a] for a in frequencies]) #normalization term, total number of characters
    p = dict([(a, frequencies[a]/Nin) for a in frequencies]) #probability table
    print(f"Length of initial hamlet = {Nin}")

    c = shannon_fano(p)
    print(f"Number of leaves = {len(c)}")
    print(c)
    print(f"length of longest codeword (&) = {len(c['&'])}")

    hamlet_sf = vl_encode(hamlet, c)
    hamlet_zipped = bits2bytes(hamlet_sf)
    print(f"Length of compressed hamlet = {len(hamlet_zipped)}") #so a 60% compression rate, not too bad. or 4.82 bits per byte.
    print(f"Entropy: {H(p)}") #the lower bound is entropy so we are about 0.4 bits per byte away from it.

    #try decoding
    xt = trees.code2xtree(c)
    hamlet_unzipped = vl_decode(hamlet_sf, xt)
    print(f'Length of the unzipped file: {len(hamlet_unzipped)}')
    # print("".join(hamlet_unzipped[:294])) # we recover the initial hamlet file!