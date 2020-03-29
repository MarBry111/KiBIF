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
        #tried to write as bytes
        with open('lcg_randomness_ints', 'ab+') as f:
           f.write(int(x).to_bytes(4, byteorder='little'))
    #with open('lcg_randomness', 'wb+') as f:
    #    f.write(output.encode())
    return xs

def test_file(fn):
    print(getoutput('rngtest <'+fn))

def main():
    xs = LCG(N, 5)
    test_file('lcg_randomness_ints')
    '''
    labels, values = zip(*Counter(xs).items())

    indexes = np.arange(len(labels))
    width = 0.5

    #plot histogram
    plt.figure(figsize=(15,5))
    plt.bar(indexes, values, width)
    plt.xticks(indexes + width * 0.5, labels)
    plt.xlabel('liczby', fontsize=15)
    plt.ylabel('liczba wystąpień danej liczby', fontsize=15)
    plt.xticks(rotation=90,fontsize=1)
    #plt.plot(values, 'o', linewidth = 0.5)
    plt.savefig('p_o_factorial.png')

    #checcking for some dependences between xi and xi+1
    xs_2 = np.array([xs[:-1],xs[1:]])
    plt.scatter(xs_2[0,:], xs_2[1,:])
    plt.savefig('p_scatter.png')
    '''

if __name__ == "__main__":
    main()