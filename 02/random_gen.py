import os
import random
from subprocess import getoutput
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

N = 4096

def random_gen_u():
    for i in range(4):
        rand_bytes = os.urandom(N//8)
        with open('rand'+str(i), 'wb+') as f:
            f.write(rand_bytes)

def random_gen():
    for i in range(4):
        rand_bytes = random.getrandbits(N)
        string = "" 
        with open('rand_notu'+str(i), 'wb+') as f:
            for ii in rand_bytes:
                string = string + str(bin(ii)[2:].zfill(8))
            f.write(string.encode())

def not_random_gen():
    not_rnd = '100'*1000
    not_rnd_b = not_rnd.encode()   
    with open('not_rand', 'wb+') as f:
        f.write(not_rnd_b)

def LCG(n, x, a = 22695477, m = 2**32, c = 1):
    output = str(x)
    xs = [x]
    for i in range(n-1):
        x = (a*x + c)%m
        output = output + str(x)
        xs.append(x)
    with open('lcg_randomness', 'wb+') as f:
        f.write(output.encode())
    return xs

def test_file(fn):
    print(getoutput('rngtest <'+fn))

xs = LCG(N, 5)
test_file('lcg_randomness')

labels, values = zip(*Counter(xs).items())

indexes = np.arange(len(labels))
width = 0.1

plt.figure(figsize=(10,8))
#plt.bar(indexes, values, width)
#plt.xticks(indexes + width * 0.5, labels)
plt.plot(values, 'o')
plt.savefig('p_o.png')