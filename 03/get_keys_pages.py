#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from subprocess import getoutput
import requests
import sys
import ssl
import pandas as pd
from OpenSSL import crypto
import concurrent.futures

hostname = 'www.facebook.com'
port = 443

#https://www.domcop.com/top-10-million-domains

key_page = {}

j = 0
nrows = 1000

n_list = [i for i in range(9000, 10000000, nrows)]

print(n_list)

def process_keys(n = 0):
    global j 

    if n == 0: 
        n = 1
    pd_pages = pd.read_csv('top10milliondomains.csv', skiprows=n, nrows=nrows, names= ['Rank', 'Domain', 'OpenRank'], header=None)
    pd_pages['Key'] = np.nan

    for i, p in pd_pages.iterrows():
        
        if (p['Rank']) % 10 == 0:
            print(n, i, j, end = '\r')
        
        hostname = 'www.' + p['Domain'] 

        try:
            cert = ssl.get_server_certificate((hostname, port))

            x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
            key = crypto.dump_publickey(crypto.FILETYPE_PEM,x509.get_pubkey())
            #print(key)

            #key_decode = key.decode()

            #print(key_decode)

            j += 1

            pd_pages.loc[i, 'Key'] =  key

        except:
            pass
            #key_decode = np.nan
        
        '''
        if key_decode in key_page:
            key_page[key_decode] = key_page[key_decode] + [hostname]
        else:
            key_page[key_decode] = [hostname]
        '''
    pd_pages.to_csv('keys/pages_with_keys'+str(n)+'.csv')

for n in n_list:
    process_keys(n)