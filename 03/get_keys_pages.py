import numpy as np
from subprocess import getoutput
import requests
import sys
import ssl
import pandas as pd
from OpenSSL import crypto

hostname = 'www.facebook.com'
port = 443

#key = getoutput('openssl s_client -connect '+hostname+':'+str(port)+' | openssl x509 -pubkey -noout')
#print(key)

#https://www.domcop.com/top-10-million-domains

pd_pages = pd.read_csv('top10milliondomains.csv', index_col= 0)
list_pages = pd_pages.Domain.values.tolist()

key_page = {}

for i, p in eumerate(list_pages):
    if i % 100 == 0:
        print(i)
    
    cert = ssl.get_server_certificate((p, port))

    x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
    key = crypto.dump_publickey(crypto.FILETYPE_PEM,x509.get_pubkey())
    key_decode = key.decode()

    if key_decode in wordFreqDic:
        key_page[key_decode] = key_page[key_decode] + [p]
    else:
        key_page[key_decode] = [p]

print(len(key_page))