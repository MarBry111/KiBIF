import numpy as np
from subprocess import getoutput
import sys
from time import gmtime, strftime, sleep

path_u_rand = '/dev/urandom'
path_rand = '/dev/random'

#reading entropy from given source + writing to file
def get_rand_entr(path, file):
    data = None 
    dt = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    #with open(path, "rb") as f: 
    #    data = f.read(1)
    entropy = getoutput("cat /proc/sys/kernel/random/entropy_avail")
    with open(file, "a") as file_object:
        file_object.write(dt+','+entropy+'\n')

    return entropy

#pobieranie 1 bajtu z danego źródła - path, zapisywanie do pliku -file, size - ilosc bajtów
def get_one_byte(path, file, size = 1):
    data = None 
    dt = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    with open(path, "rb") as f: 
        data = f.read(size)
    entropy = getoutput("cat /proc/sys/kernel/random/entropy_avail")
    with open(file, "a") as file_object:
        file_object.write(dt+','+entropy+'\n')

    return entropy


def main():
    e = getoutput("cat /proc/sys/kernel/random/entropy_avail")
    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), e)
    for i in range(100):
        sleep(1)
        with open(path_rand, "rb") as f: 
            data = f.read(1)
        e = getoutput("cat /proc/sys/kernel/random/entropy_avail")
        print(strftime("%Y-%m-%d %H:%M:%S", gmtime()), e , data)

main()