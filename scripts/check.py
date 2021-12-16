import sys
import pandas as pd
import numpy as np
import os
import socket
import xlrd
import openpyxl 
import json
from flask import Flask, render_template, redirect, url_for, request
from multiprocessing import Lock
import multiprocessing as mp
import threading 
import time
import networkx as nx
from pprint import pprint  # just for nice printing
from anytree import Node
from anytree.exporter import DictExporter
from anytree import Node, RenderTree, AsciiStyle,PreOrderIter

df=pd.read_csv('cdpneighbors.csv')

df=df.replace(np.nan, 'nullvalue')
hr=pd.read_csv('Device_fact1.csv',low_memory=False)
hr=hr.replace(np.nan, 'nullvalue')
print(len(df))
t='Host'
l=pd.DataFrame()
dhr=pd.DataFrame()
for i in df.index:
    t1=df['deviceName'][i].find('.')
    if(t1!=-1):
        t1=df['deviceName'][i][0:t1]
    else:
        t1=df['deviceName'][i]

    t2=df['neighborDeviceName'][i].find('.')
    if(t2!=-1):
        t2=df['neighborDeviceName'][i][0:t2]
    else:
        t2=df['neighborDeviceName'][i]
    dhr=dhr.append({'deviceName':t1,'neighborDeviceName':t2,'farEndInterface':df['farEndInterface'][i],'nearEndInterface':df['nearEndInterface'][i]},ignore_index = True)
        
dhr.to_csv('cdpneighbors1.csv')

