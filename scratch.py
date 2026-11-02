from vl_codes import shannon_fano
import random
import trees

p = [random.random() for _ in range(10)] #random distribution
p = dict([(chr(k+ord('a')), p[k]/sum(p)) for k in range(len(p))]) #10 symbols in alpha order, with its probability.
#print(f'Probability distribution: {p}')
#print(sum(p.values())) #check validity of dists

c = shannon_fano(p)
print(f'Codebook: {c}')
t = trees.code2xtree(c)
n = trees.xtree2newick(t)
print(n)