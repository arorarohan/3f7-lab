from itertools import groupby
import arithmetic as arith

#load p from hamlet as always
f = open('hamlet.txt', 'r')
hamlet = f.read()
f.close()

frequencies = dict([(key, len(list(group))) for key, group in groupby(sorted(hamlet))])
Nin = sum([frequencies[a] for a in frequencies]) #normalization term, total number of characters
p = dict([(a, frequencies[a]/Nin) for a in frequencies]) #probability table
print(f"Length of initial hamlet = {Nin}")

#compute the cumulative
cum = [0.0]
for a in p:
    cum.append(cum[-1]+p[a])
cum.pop()
cum = dict([(a,cum[k]) for a,k in zip(p,range(len(p)))])

lo, hi = 0.0, 1.0
n = 4 #the number of symbols per codeword
for k in range(n):
    a = hamlet[k]
    lohi_range = hi - lo
    hi = lo + lohi_range * (cum[a] + p[a])
    lo = lo + lohi_range * cum[a]
#print(f'lo = {lo}, hi = {hi}, hi-lo = {hi-lo}')


arith_encoded = arith.encode(hamlet, p)
#arith_decoded = arith.decode(arith_encoded, p, Nin)
#print('\n'+''.join(arith_decoded[:294]))

arith_corrupted = arith_encoded.copy()
arith_corrupted[1000] ^= 1
arith_decoded = arith.decode(arith_corrupted, p, Nin)
print('\n'+''.join(arith_decoded[:294]))