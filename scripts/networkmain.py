import pandas as pd
import numpy as np
import json
from flask import Flask, render_template, redirect, url_for, request
from pprint import pprint  # just for nice printing
from anytree import Node
from anytree.exporter import DictExporter
from anytree import Node, RenderTree, AsciiStyle,PreOrderIter


def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


'''def table(name):
      x=name
      df=pd.read_csv('cdpneighbors1.csv')
      df=df.replace(np.nan, 'nullvalue')
      hr=pd.read_csv('Device_fact1.csv',low_memory=False)
      hr=hr.replace(np.nan, 'nullvalue')
      hr.columns = hr.columns.str.strip()
      dr=hr[hr['DeviceName'].str.contains(x)]
      dy=df[df['deviceName'].str.contains(x)]
      
      #dr.set_index("DeviceName", inplace = True)
      #dy.set_index("deviceName", inplace = True)
      dr.drop_duplicates(keep='first',inplace=True)
      
      dy.drop(dy.filter(regex="Unname"),axis=1, inplace=True)
      return render_template('table.html', name1=x,tables=[dr.to_html(classes='data', header="true",index=False)],tables1=[dy.to_html(classes='data', header="true",index=False)])
'''
def treestart(devicedatafort,trp):
      print("started tree")
      root = Node(name="Cloud",group='cloud.png',updated="cloud")
      added=[]
      
      for p in devicedatafort.index:
            #print(p)
            if(devicedatafort['group_d1'][p]==1 and (devicedatafort['updateddeviceName'][p] not in added)):
                  #print(devicedatafort['updateddeviceName'][p] not in added)
                  t=devicedatafort['deviceName'][p]
                  ip=devicedatafort['deviceIpAddress'][p]
                  group_id=str(("group")+str(int(devicedatafort['group_d1'][p]))+str(".png"))
                  t=Node(name=devicedatafort['deviceName'][p],group=group_id,parent=root,updated=devicedatafort['updateddeviceName'][p],ip=ip)
                  added.append(devicedatafort['updateddeviceName'][p])
     
      for p in devicedatafort.index:
            if(devicedatafort['group_d2'][p]==1 and devicedatafort['updatedneighbordeviceName'][p] not in added):
                  t=devicedatafort['neighborDeviceName'][p]
                  ip=devicedatafort['neighborIpAddress'][p]
                  group_id=str(("group")+str(int(devicedatafort['group_d2'][p]))+str(".png"))
                  t=Node(name=devicedatafort['neighborDeviceName'][p],group=group_id,parent=root,updated=devicedatafort['updatedneighbordeviceName'][p],ip=ip)
                  added.append(devicedatafort['updatedneighbordeviceName'][p])
      no=[]
      lopi=0
     
      for i in devicedatafort.index:
            
            d1=devicedatafort['updateddeviceName'][i]
            d2=devicedatafort['updatedneighbordeviceName'][i]
            group_d1=int(devicedatafort['group_d1'][i])
            ip1=devicedatafort['deviceIpAddress'][i]
            group_d2=int(devicedatafort['group_d2'][i])
            d1_name=devicedatafort['deviceName'][i]
            d2_name=devicedatafort['neighborDeviceName'][i]
            ip2=devicedatafort['neighborIpAddress'][i]
            
                      
        
            if((d1 not in added) and (d2 not in added)):
                  
                  added.append(d1)
                  added.append(d2)
                  if(group_d2>group_d1):
                        group_d1="group"+str(group_d1)+".png"
                        group_d2="group"+str(group_d2)+".png"   
                        d1=Node(name=d1_name,group=group_d1,updated=d1,parent=root,ip=ip1)
                        d2=Node(name=d2_name,group=group_d2,updated=d2,parent=d1,ip=ip2)
            
                  if(group_d2<=group_d1):
                        group_d1="group"+str(group_d1)+".png"
                        group_d2="group"+str(group_d2)+".png"
                        d2=Node(name=d2_name,group=group_d2,updated=d2,parent=root,ip=ip2)
                        d1=Node(name=d1_name,group=group_d1,updated=d1,parent=d2,ip=ip1)
        
            elif(d1 not in added and d2 in added ):
                 
                  added.append(d1)
                  for node in PreOrderIter(root):
                        if(node.updated==d2):
                              d2=node
                              break
                  group_d1="group"+str(group_d1)+".png"
                  group_d2="group"+str(group_d2)+".png"
                  d1=Node(name=d1_name,group=group_d1,updated=d1,parent=d2,ip=ip1)
        
        
            elif(d2 not in added and d1 in added ):
                  
                  group_d1="group"+str(group_d1)+".png"
                  group_d2="group"+str(group_d2)+".png"
                  added.append(d2)
                  for node in PreOrderIter(root):
                        if(node.updated==d1):
                              d1=node
                  d2=Node(name=d2_name,group=group_d2,updated=d2,parent=d1,ip=ip2)
        
            elif(d1 in added and d2 in added):
                  
                  dic={}
                  dic['parent']=d1_name
                  dic['child']=d2_name
                  no.append(dic)
            lopi=lopi+1
            
      
      
      exporter = DictExporter()
      hi=exporter.export(root)
      
      out_file = open("static/flare.json", "w") 
      json.dump(hi, out_file, indent = 4) 
      out_file.close() 
      tr={}
      added1=list(set(list(trp['deviceName'])))
      
      #print(added1)
      for j in added1:
            dp=[]
            l={}
            for i in trp.index:
                  if(j==trp['deviceName'][i]):
                        dt={}
                        dt['farEndInterface']=trp['farEndInterface'][i]
                        dt['neighborDeviceName']=trp['neighborDeviceName'][i]
                        dt['nearEndInterface']=trp['nearEndInterface'][i]
                        dp.append(dt)
            l[j]=dp
            tr[j]=dp
     


      
      
      return no,hi,tr
def delete():  
      return "DataUnavailable"
         
        
 
def networkdiagram1(sitename): 
      print(sitename) 
      
      df=pd.read_csv('scripts/cdpneighbors1.csv')
      df=df.replace(np.nan, 'nullvalue')
      hr=pd.read_csv('scripts/Device_fact1.csv',low_memory=False)
      hr=hr.replace(np.nan, 'nullvalue')
      hr.columns = hr.columns.str.strip()
      devicedata=hr.loc[hr['Site_Code'] == sitename]
      devicedataforui=pd.DataFrame(columns = ['name', 'group','id'])
      deviced=[]
      devicelist=[]
      t=0
      routerlist=[]
      for i in devicedata.index:
            ty=devicedata['DeviceName'][i].find('.')
            devn=""
            if(ty!=-1):
                  devn=devicedata['DeviceName'][i][0:ty]
            else:
                  devn=devicedata['DeviceName'][i]
            devn1=devicedata['IpAddress'][i]
            grp=-9
            img=""
            if( 'Router' in devicedata['DeviceType'][i] or 'Router' in devicedata['ProductType'][i] or 'Router' in devicedata['ProductFamily'][i]):
        
                  grp=1
                  deviced.append(devn)
                  routerlist.append(devn)
                  img=str(grp)+".png"
            elif('Switch' in devicedata['DeviceType'][i] or 'Switch' in devicedata['ProductType'][i] or 'Switch' in devicedata['ProductFamily'][i]):
                  grp=2
                  img=str(grp)+".png"
            elif('Controller' in devicedata['DeviceType'][i] or 'Controller' in devicedata['ProductType'][i] or 'Controller' in devicedata['ProductFamily'][i]):
                  grp=3
                  img=str(grp)+".png"
            elif('AIR' in  devicedata['ModelNr'][i] or 'AP' in devicedata['DeviceType'][i] or 'AP' in devicedata['ProductType'][i] or 'AP' in devicedata['ProductFamily'][i]):
                  grp=4
                  img=str(grp)+".png"
            else:
                  grp=5
                  img=str(grp)+".png"
            devicelist.append(devn)
            devicedataforui=devicedataforui.append({'name':devn,'group':grp,'id':t,'IpAddress':devn1},ignore_index = True)
            t=t+1
      devicedatafort=df.loc[df['deviceName'].isin(devicelist)]
      t='Data Unavailable'
      l=pd.DataFrame()
      for i in devicedatafort.index:
                        #print(devicedatafort['neighborCapabilities'][i])
            devn=devicedatafort['neighborDeviceName'][i]

            if(devn in devicelist):
                              #print("found")
                  l=l.append(devicedatafort.loc[i],ignore_index=True)
                        
      devicedatafort=l
      trp=l
      y=[]
      devicedatafory=pd.DataFrame()
      o=0
      print("routerlist")
      print(routerlist)
      routerconnected=[]
      for i in devicedatafort.index:
            deviceName=devicedatafort['deviceName'][i]
            if(deviceName in routerlist):
                  if((devicedatafort['neighborDeviceName'][i] not in routerlist)):
                        routerconnected.append(devicedatafort['neighborDeviceName'][i])
      print("routerconnected")
      routerconnected=list(set(routerconnected))
      temp=[]
      for i in routerconnected:
                        #print(i.find("AS"))
            if(i.find("AS")!=-1):
                  temp.append(i)
                              #routerconnected.remove(i)
      for i in temp:
            routerconnected.remove(i)           
      print(routerconnected)
      lio=pd.DataFrame()
      dic={}
      hi={}
      tr={}

      if(len(routerconnected)<=0):
            print("Going here")
            msg=t         
            return dic,hi,tr,msg
      print("in step1")
                  #trp=devicedatafort
                  #have to write remove duplicate algorithm
      changedindexes=[]
      for i in devicedatafort.index:
                        
            d1=devicedatafort["deviceName"][i]
            d2=devicedatafort["neighborDeviceName"][i]
            d3=devicedatafort["farEndInterface"][i]
            d4=devicedatafort["nearEndInterface"][i]
            if(d3!="nullvalue" and d4!="nullvalue"):
                  lo={}
                  lo['deviceName']=d1
                  lo['neighborDeviceName']=d2
                  lo['nearEndInterface']=d4
                  lo['farEndInterface']=d3
                  lio=lio.append(lo,ignore_index = True) 
            elif(d3=="nullvalue"):
                        flag=0
                              
                        for j in devicedatafort.index:
                              d11=devicedatafort["deviceName"][j]
                              d21=devicedatafort["neighborDeviceName"][j]
                              d31=devicedatafort["farEndInterface"][j]
                              d41=devicedatafort["nearEndInterface"][j]
                              flag=0
                              if(d1==d21 and d2==d11 and d4==d31):
                                    lo={}
                                    lo['deviceName']=d1
                                    lo['neighborDeviceName']=d2
                                    lo['nearEndInterface']=d4
                                    lo['farEndInterface']=d41
                                    lio=lio.append(lo,ignore_index = True)
                                    flag=1
                                    changedindexes.append(j)
                        if(flag==0):
                                    lo={}
                                    lo['deviceName']=d1
                                    lo['neighborDeviceName']=d2
                                    lo['nearEndInterface']=d4
                                    lo['farEndInterface']=d3
                                    lio=lio.append(lo,ignore_index = True)
            elif(d4=="nullvalue"):
                  flag=0
                  for j in devicedatafort.index:
                                    
                        d11=devicedatafort["deviceName"][j]
                        d21=devicedatafort["neighborDeviceName"][j]
                        d31=devicedatafort["farEndInterface"][j]
                        d41=devicedatafort["nearEndInterface"][j]
                        flag=0
                        if(d1==d21 and d2==d11 and d3==d41):
                              lo={}
                              lo['deviceName']=d1
                              lo['neighborDeviceName']=d2
                              lo['nearEndInterface']=d31
                              lo['farEndInterface']=d3
                              lio=lio.append(lo,ignore_index = True)
                              flag=1
                              changedindexes.append(j)
                                          
                  if(flag==0):
                        lo={}
                        lo['deviceName']=d1
                        lo['neighborDeviceName']=d2
                        lo['nearEndInterface']=d4
                        lo['farEndInterface']=d3
                        lio=lio.append(lo,ignore_index = True)
                                    
            else:
                  print("4th if")
                  print("hello")
                  o=o+1

      msg="tree"           
      devicedatafort=lio        
      lp=pd.DataFrame()
      devicedatafort.sort_values(by = ['deviceName','neighborDeviceName'],inplace = True)
      for i in range(0,len(devicedatafort)):
            deviceName=devicedatafort.iloc[i,0]
            o=0
            farEndInterface=devicedatafort.iloc[i,1]
            nearEndInterface=devicedatafort.iloc[i,2]
            neighborDeviceName=devicedatafort.iloc[i,3]
            for j in range(i+1,len(devicedatafort)):
                  deviceName1=devicedatafort.iloc[j,0]
                  farEndInterface1=devicedatafort.iloc[j,1]
                  nearEndInterface1=devicedatafort.iloc[j,2]
                  neighborDeviceName1=devicedatafort.iloc[j,3]
                  if(deviceName==neighborDeviceName1 and neighborDeviceName==deviceName1):
                        if(farEndInterface==nearEndInterface1 and  nearEndInterface==farEndInterface1):
                              lp=lp.append(devicedatafort.iloc[[j]],ignore_index=True)
                              o=o+1
                        
      lp.drop_duplicates(keep='first',inplace=True)
      devicedatafort=devicedatafort.append(lp,ignore_index=True)
      devicedatafort.drop_duplicates(keep=False,inplace=True)
      print("in step 3")
      ty=pd.DataFrame()
      tuo=0
      for i in devicedatafort.index:
                        
            deviceName=devicedatafort['deviceName'][i]
            updateddeviceName=""
            upadatedneighborDeviceName=""
            farEndInterface=devicedatafort['farEndInterface'][i]
            nearEndInterface=devicedatafort['nearEndInterface'][i]
            neighborDeviceName=devicedatafort['neighborDeviceName'][i]
            group_d1=0
            group_d2=0
            updateddeviceName=deviceName
            updatedneighborDeviceName=neighborDeviceName
            deviceIpAddress=""
            neighborIpAddress=""
            for j in devicedataforui.index:
                  if(deviceName==devicedataforui['name'][j]):
                        group_d1=devicedataforui['group'][j]
                        deviceIpAddress=devicedataforui['IpAddress'][j]
                        break
            for j in devicedataforui.index:
                  if(neighborDeviceName==devicedataforui['name'][j]):
                        group_d2=devicedataforui['group'][j]
                        neighborIpAddress=devicedataforui['IpAddress'][j]
                        break
                        
            if((group_d1==1 and group_d2==2) and (neighborDeviceName in routerconnected)):

                  t=farEndInterface.find("/")
                  if(t!=-1):
                        far=farEndInterface[t-1]
                        updatedneighborDeviceName=neighborDeviceName+far
                              
            elif((group_d1==2 and group_d2==1 and nearEndInterface!="nullvalue" and deviceName in routerconnected)):
                  t=nearEndInterface.find("/")
                  if(t!=-1):
                        far=nearEndInterface[t-1]
                        updateddeviceName=deviceName+far
            elif((deviceName in routerconnected) and (neighborDeviceName in routerconnected)):
                  t=nearEndInterface.find("/")
                  if(t!=-1):
                        far=nearEndInterface[t-1]
                        updateddeviceName=deviceName+far
                        t=farEndInterface.find("/")
                        if(t!=-1):
                              far=farEndInterface[t-1]
                              updatedneighborDeviceName=neighborDeviceName+far
                              
            elif((deviceName in routerconnected)):
                  t=nearEndInterface.find("/")
                  if(t!=-1):
                        far=nearEndInterface[t-1]
                        updateddeviceName=deviceName+far
            elif((neighborDeviceName in routerconnected)):
                  t=farEndInterface.find("/")
                  if(t!=-1):
                        far=farEndInterface[t-1]
                        updatedneighborDeviceName=neighborDeviceName+far
                        
            lo={}
            lo['deviceName']=deviceName
            lo['farEndInterface']=farEndInterface
            lo['nearEndInterface']=nearEndInterface
            lo['neighborDeviceName']=neighborDeviceName
            lo['group_d1']=group_d1
            lo['group_d2']=group_d2
            lo['updateddeviceName']=updateddeviceName
            lo['updatedneighbordeviceName']=updatedneighborDeviceName
            lo['deviceIpAddress']=deviceIpAddress
            lo['neighborIpAddress']=neighborIpAddress
            ty=ty.append(lo,ignore_index = True)
            tuo=tuo+1
                 
                  
      ty.sort_values(by = ['group_d1', 'group_d2','deviceName','updateddeviceName','neighborDeviceName','updatedneighbordeviceName'],inplace=True)
                  
      you=[]
      tui=pd.DataFrame()
      you.append(ty.iloc[0,1])
      tu=[]
      for i in you:
            for j in ty.index:
                  if(i==ty['updateddeviceName'][j]):
                        if(j not in tu):
                              tui=tui.append(ty.iloc[[j]],ignore_index = True)
                              tu.append(j)
                              if(ty['updatedneighbordeviceName'][j] not in you):
                                    you.append(ty['updatedneighbordeviceName'][j])
            for j in ty.index:
                  if(i==ty['updatedneighbordeviceName'][j]):
                        if(j not in tu):
                              tui=tui.append(ty.iloc[[j]],ignore_index = True)
                              tu.append(j)
                              if(ty['updateddeviceName'][j] not in you):
                                    you.append(ty['updateddeviceName'][j])
                        
      for i in ty.index:
            if(i not in tu):
                  tui=tui.append(ty.loc[[j]],ignore_index = True)
                  tu.append(i)
                             
      tui.drop_duplicates(keep='first',inplace=True) 
      tui.sort_values(by = ['group_d1', 'group_d2','deviceName','updateddeviceName','neighborDeviceName','updatedneighbordeviceName'],inplace=True) 
      
      dic,hi,tr=treestart(tui,trp)
      #print(dic)
      return dic,hi,tr
                  
                  