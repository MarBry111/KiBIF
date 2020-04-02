#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
from subprocess import getoutput
import requests
import sys
import ssl
import pandas as pd
from OpenSSL import crypto
from multiprocessing.dummy import Pool as ThreadPool
import time
from tqdm import tqdm

hostname = 'www.facebook.com'
port = 443

#https://www.domcop.com/top-10-million-domains

j = 0
nrows = 1000

n_list = [i for i in range(28000, 10000000, nrows)]
#n_list_10000 = [i for i in range(0, 10000, nrows)]

#n_input = int(sys.argv[1])

def process_keys(n = 0):

    if n == 0: 
        n = 1
    pd_pages = pd.read_csv('top10milliondomains.csv', skiprows=n, nrows=nrows, names= ['Rank', 'Domain', 'OpenRank'], header=None)
    pd_pages['Key'] = np.nan

    for i, p in tqdm(pd_pages.iterrows(), total=pd_pages.shape[0]):
        
        #if (p['Rank']) % 10 == 0:
        #    print(n, i, j, end = '\r')
        
        hostname = p['Domain'] 

        try:
            cert = ssl.get_server_certificate((hostname, port))

            x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
            key = crypto.dump_publickey(crypto.FILETYPE_PEM,x509.get_pubkey())
            #print(key)

            #key_decode = key.decode()

            #print(key_decode)

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

pool = ThreadPool(32)

with pool as p:
    r = list(tqdm(p.imap(process_keys, n_list), total=nrows))
