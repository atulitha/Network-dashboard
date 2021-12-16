#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import xlwt
import requests
import xlrd
import json


# In[2]:


df=pd.read_csv('Device_fact1.csv',low_memory=False)
df=df.replace(np.nan, 'nullvalue')
df.drop_duplicates(subset ="DeviceName",
                     keep = False, inplace = True)


# In[3]:





# In[4]:


dict={}
listofState=[]
for i in df.index:
    listofState.append(df['State'][i])
    
listofState=set(listofState)


# In[5]:


listofState=list(listofState)


# In[6]:


listofState


# In[7]:

xf=pd.ExcelFile('network_id_name.xls')
dfw=xf.parse()
merakilist=[]
for j in dfw.index:
    p=dfw['networkname'][j]
    #print(p)
    #print(l)
        
    p=p[0:7]
    merakilist.append(p)

for i in listofState:
    dp=[]
    for j in df.index:
        if(i==df['State'][j]):
            #print(df['New Site Code'][j])
            if(df['Site_Code'][j] not in  merakilist):
                y=df['Site_Name'][j].strip()
                li=df['Site_Code'][j]+" - "+y
                dp.append(li)
    dp=list(set(dp))
    dp.sort()
    if(len(dp)>0 and i!="nullvalue"):
        dict[i]=dp
dict


# In[8]:


out_file = open("listofsitename.json", "w") 
json.dump(dict, out_file, indent = 4) 
out_file.close() 


# In[ ]:




