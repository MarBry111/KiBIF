import struct
import time 
import os 


t = 0.5
T = 100


for ii in range(int(T*60/t)):
	time.sleep(t)
	#os.system('cat /proc/sys/kernel/random/entropy_avail')
	os.system('cat /proc/sys/kernel/random/entropy_avail >> ~/Desktop/entropy.txt')

