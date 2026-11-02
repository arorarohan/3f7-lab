from vl_codes import huffman, vl_encode, vl_decode, bits2bytes, bytes2bits
from itertools import groupby
from trees import xtree2newick, code2xtree, xtree2code
import camzip
import camunzip
from math import log2
from json import load
from shannon_fano_investigation import H


#load hamlet
f = open('hamlet.txt', 'r')
hamlet = f.read()
f.close()

frequencies = dict([(key, len(list(group))) for key, group in groupby(sorted(hamlet))])
Nin = sum([frequencies[a] for a in frequencies]) #normalization term, total number of characters
p = dict([(a, frequencies[a]/Nin) for a in frequencies]) #probability table

print(f"Length of initial hamlet = {Nin}")

camzip.camzip('huffman', 'hamlet.txt')

xt = huffman(p)
c = xtree2code(xt)
print(f"Number of leaves = {len(c)}") # n = 67, smae as before.
print(c)
print(f"length of longest codeword (|) = {len(c['|'])}") #12.

hamlet_huf = vl_encode(hamlet, c)
hamlet_zipped = bits2bytes(hamlet_huf)
print(f"Length of compressed hamlet = {len(hamlet_zipped)}") #115752
print(f"Compression rate = {len(hamlet_zipped)/Nin * 8} bpb") # 4.47. really close to entropy!
print(f"Entropy: {H(p)}") # 4.45

#try decoding
xt = code2xtree(c)
hamlet_unzipped = vl_decode(hamlet_huf, xt)
print(f'Length of the unzipped file: {len(hamlet_unzipped)}') # 
#print("".join(hamlet_unzipped[:294])) # we recover the initial hamlet file!

#try corruption
hamlet_corrupted = hamlet_huf.copy()
hamlet_corrupted[400] ^= 1 #flip 1 singular bit
chamlet_decoded = vl_decode(hamlet_corrupted, xt)
print(''.join(chamlet_decoded[:297]))
