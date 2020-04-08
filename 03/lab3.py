#!/usr/bin/env python
# coding: utf-8

import numpy as np
import requests
import sys
import ssl
import pandas as pd
from OpenSSL import crypto
import matplotlib.pyplot as plt
import pandas as pd
import os
from Crypto.PublicKey import RSA
from tqdm import tqdm
import whois
from multiprocessing.dummy import Pool as ThreadPool



# In[2]:


# # Scrapping data from webistes

# ## pobranie kluczy + czyszczenie dataframea

# In[5]:


if(False):
    keys_paths = os.listdir('keys')
    keys_paths = ['keys/'+p for p in keys_paths]
    
    pd_keys = [pd.read_csv(p, index_col = 0) for p in keys_paths]
    pd_key = pd_keys[0]
    for p in pd_keys[1:]:
        pd_key = pd_key.append(p)
    
    del pd_key['Rank']
    
    pd_key = pd_key.reset_index()
    
    del pd_key['index']
    
    pd_key.loc[pd_key['Key'].notnull()]
    
    pd_key.to_csv('domeny_klucze.csv')
else:
    pd_key = pd.read_csv('domeny_klucze.csv', index_col = 0, usecols = [0, 1,3])
    
    domains_exclude = pd.read_csv('doms.csv', header = None)
    domains_exclude = domains_exclude[0].values.tolist()


# ## Dict = klucz : lista domen

# In[6]:


if(False):
    key_page = {}
    
    for i, p in pd_key.iterrows():
        key_decode = p['Key']
        hostname = p['Domain']
        if key_decode in key_page:
            key_page[key_decode] = key_page[key_decode] + [hostname]
        else:
            key_page[key_decode] = [hostname,]
            
    del key_page[np.nan]


# ## Lista - klucz, liczba domen

# In[7]:


if(False):
    list_keys = []
    
    for i, k in key_page.items():
        list_keys.append([i, len(k)])
        
    pd_no_keys = pd.DataFrame.from_records(list_keys)
    
    pd_no_keys.to_csv('key_count.csv')
else:
    pd_no_keys = pd.read_csv('key_count.csv', index_col = 0)


# In[8]:


print('1key 1domain:', pd_no_keys.loc[ pd_no_keys.iloc[:,1] == 1, '1'].sum())
print('Alldomain:', pd_no_keys['1'].sum())


# #### plotting histograms ( before cleaning data)



if False:
    keys_list = pd_no_keys.loc[:,1].values.tolist()
    
    keys_list.sort()
    keys_list = np.array(keys_list)
    
    plt.figure(figsize=(10,5))
    plt.plot(keys_list[keys_list>1], 'o')


# ### Ratio

# In[14]:


print('domens:', np.sum(pd_no_keys['1'].values))
print('share key:', np.sum(pd_no_keys['1'].values[pd_no_keys['1'].values > 1]))
print('ratio:', np.sum(pd_no_keys['1'].values[pd_no_keys['1'].values > 1])/np.sum(pd_no_keys['1'].values))


# In[15]:


pd_no_keys.loc[pd_no_keys.loc[:,'1'] > 2,:].sort_values(by=['1'],ascending=False)


# ## Duplikaty

# In[16]:


# unique keys 
keys_gr1 = pd_no_keys.loc[pd_no_keys.loc[:,'1'] > 1, '0']
keys_gr1 = set(keys_gr1.values.tolist())


# In[17]:


# function to get the last which is not co com eu etc
def domain_name(list_i):
    list_split = list_i.split('.')
    if len(list_split) > 2:
        list_tmp = list_split[:-1]
    else:
        list_tmp = list_split
        
    if type(list_tmp) == list:
        list_tmp.reverse()
        not_find = True
        j = 0
        xi = 'com'
        while (xi in domains_exclude):
            try: 
                xi = list_tmp[j]
            except:
                xi = list_i
                break
            j += 1
    else: 
        xi = list_tmp
    
    return xi


# In[18]:


if False:
    pd_key_celan = pd_key.copy()
    
    for k in tqdm(keys_gr1):
        list_t = pd_key.loc[pd_key.loc[:,'Key'] == k, 'Domain'].values.tolist()
        # split on dot - and get rid of last part com/uk/pl etc
        # and make dictionary : domain - pages 
        domains_pages = {}
        for p in list_t:
            d = domain_name(p)
            if d in domains_pages:
                domains_pages[d] = domains_pages[d] + [p]
            else:
                domains_pages[d] = [p,]
        # change pages for the first from list 
        for d, p in domains_pages.items():
            #pd_key_celan.loc[p, 'Domain'] =  d
            pd_key_celan.loc[(pd_key_celan['Key'] == k) & (pd_key_celan['Domain'].isin(p)), 'Domain'] = d
        
    pd_key_celan.drop_duplicates(inplace=True)
    pd_key_celan = pd_key_celan.loc[ pd_key_celan['Key'].notnull(), :]
    
    pd_key_celan.to_csv('domeny_klucze_clean_I.csv')
else:
    pd_key_celan = pd.read_csv('domeny_klucze_clean_I.csv', index_col = 0)


# In[19]:


k = "b'-----BEGIN PUBLIC KEY-----\\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAzWJP5cMThJgMBeTvRKKl\\n7N6ZcZAbKDVAtNBNnRhIgSitXxCzKtt9rp2RHkLn76oZjdNO25EPp+QgMiWU/rkk\\nB00Y18Oahw5fi8s+K9dRv6i+gSOiv2jlIeW/S0hOswUUDH0JXFkEPKILzpl5ML7w\\ndp5kt93vHxa7HswOtAxEz2WtxMdezm/3CgO3sls20wl3W03iI+kCt7HyvhGy2aRP\\nLhJfeABpQr0Uku3q6mtomy2cgFawekN/X/aH8KknX799MPcuWutM2q88mtUEBsuZ\\nmy2nsjK9J7/yhhCRDzOV/yY8c5+l/u/rWuwwkZ2lgzGp4xBBfhXdr6+m9kmwWCUm\\n9QIDAQAB\\n-----END PUBLIC KEY-----\\n'"
pd_key.loc[pd_key['Key'] == k, : ]


# In[20]:


print('clean:', pd_key_celan.shape)
print('regular:', pd_key.shape)


# ## Dataframe = klucz : lista domen

# In[21]:


if False:
    key_page = {}
    
    for i, p in pd_key_celan.iterrows():
        key_decode = p['Key']
        hostname = p['Domain']
        if key_decode in key_page:
            key_page[key_decode] = key_page[key_decode] + [hostname]
        else:
            key_page[key_decode] = [hostname,]
                
    list_keys = []
    
    for i, k in key_page.items():
        list_keys.append([i, len(k)])
        
    pd_no_keys_clean = pd.DataFrame.from_records(list_keys)
    
    pd_no_keys_clean.to_csv('key_count_clean.csv')
else:
    pd_no_keys_clean = pd.read_csv('key_count_clean.csv', index_col = 0)


# ### New Ratio

# In[22]:


print('domens:', np.sum(pd_no_keys_clean['1'].values))
print('share key:', np.sum(pd_no_keys_clean['1'].values[pd_no_keys_clean['1'].values > 1]))
print('ratio:', np.sum(pd_no_keys_clean['1'].values[pd_no_keys_clean['1'].values > 1])/np.sum(pd_no_keys_clean['1'].values))


# #### plotting histograms ( stage I cleaning data)


# ## Cleaning data by hand

# ### 2-10 domains same key - common prefix

# In[27]:


print('2:', pd_no_keys_clean.loc[pd_no_keys_clean['1'] == 2, '0'].shape[0])
print('3:', pd_no_keys_clean.loc[pd_no_keys_clean['1'] == 3, '0'].shape[0])
print('4:', pd_no_keys_clean.loc[pd_no_keys_clean['1'] == 4, '0'].shape[0])


# In[28]:


if False:
    for k in tqdm(pd_no_keys_clean.loc[(pd_no_keys_clean['1'] > 1) & (pd_no_keys_clean['1'] <11), '0'].values.tolist()):
        p = pd_key_celan.loc[pd_key_celan['Key'] == k, 'Domain'].values.tolist()
        common = os.path.commonprefix(p)
        if len(common) > 1:
            print
            pd_key_celan.loc[(pd_key_celan['Key'] == k) & (pd_key_celan['Domain'].isin(p)), 'Domain'] = common
    pd_key_celan.drop_duplicates(inplace=True)


# In[29]:


print('2:', pd_no_keys_clean.loc[pd_no_keys_clean['1'] == 2, '0'].shape[0])
print('3:', pd_no_keys_clean.loc[pd_no_keys_clean['1'] == 3, '0'].shape[0])
print('4:', pd_no_keys_clean.loc[pd_no_keys_clean['1'] == 4, '0'].shape[0])


# ### get the owners of domains and compare

# In[30]:


domain = whois.query('google.com')
domain.name_servers.pop().split('.')[1]


# In[31]:


# unique keys 
keys_gr11 = pd_no_keys_clean.loc[pd_no_keys_clean.loc[:,'1'] > 1, '0']
keys_gr11 = keys_gr11.values.tolist()


# In[54]:

pd_key_celaner = pd_key_celan.copy()
pd_key_celaner['Server'] = np.nan

#for k in tqdm(keys_gr11, desc = "outer_loop", position=0):
def get_owner(j):
    k = keys_gr11[j]

    domains_c = pd_key_celan.loc[pd_key_celan.loc[:,'Key'] == k, 'Domain'].values.tolist()

    for d in tqdm(domains_c, desc = str(j)):
        
        domain = pd_key.loc[(pd_key.loc[:,'Key'] == k) & (pd_key['Domain'].str.contains(d)), 'Domain'].values.tolist()[0]
        try:
            serv = whois.query(domain).name_servers.pop()
            serv = domain_name(serv)
        except:
            serv = d

        pd_key_celaner.loc[(pd_key_celaner.loc[:,'Key'] == k) & (pd_key_celaner['Domain'] == d), 'Server'] = serv


pool = ThreadPool(64)

results = pool.map(get_owner, range(len(keys_gr11)))
pool.close()
pool.join()

pd_key_celaner = pd_key_celaner.loc[pd_key_celaner['Server'].notnull(), :]
pd_key_celaner.drop_duplicates(subset=['Key', 'Server'], keep = 'last')

pd_key_celaner.to_csv('domeny_klucze_clean_II.csv')
