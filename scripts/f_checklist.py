import pandas as pd
import numpy as np
import socket
import xlsxwriter

def hname_without_ext(i):
    ty=str(i).find('.')
    devn=""
    if(ty!=-1):
        devn=i[0:ty]
    else:
        devn=i
    return devn

def neighbor(h,hostname,aphostname):
    df = pd.DataFrame(columns= ['deviceName', 'ipAddress', 'duplexMode', 'farEndInterface', 'interfaceIndex', 'nearEndInterface', 'neighborCapabilities', 'neighborDeviceName', 'neighborDevicePlatformType', 'action_cd', 'create_ts', 'change_ts', 'create_sk', 'change_sk'])
    hname=h
    for j in range(0,len(nei_df)):
        devn=hname_without_ext(nei_df['deviceName'][j])
        if devn==hname:   
            df.loc[len(df.index)]=nei_df.iloc[j].tolist()
            n=hname_without_ext(nei_df['neighborDeviceName'][j])
            if n not in hostname and n not in aphostname and n!="nullvalue": 
                print(n)
                if 'AIR' in nei_df['neighborDevicePlatformType'][j]:
                    aphostname.append(n)
                else:
                    hostname.append(n)
    return df

def pulling(i):
    global row
    flag=False
    for j in range(0,len(df)):
        devn=hname_without_ext(df['deviceName'][j])
        if devn==i:
            flag=True
            sheet.write(row,0,df['deviceName'][j])
            sheet.write(row,1,df['ipAddress'][j])
            sheet.write(row,2,df['deviceType'][j])
            sheet.write(row,3,df['productFamily'][j])
            sheet.write(row,4,df['modelNr'][j])
            sheet.write(row,5,df['serialNr'][j])
            sheet.write(row,6,df['softwareVersion'][j])
            try:
                days = (int) (int(df['upTime'][j] )/ (1000*60*60*24))
                sheet.write(row,7,days)#uptime in days %365=years
            except Exception as e:
                print(str(e))
            row=row+1
            break
    if flag==False:
        sheet.write(row,0,i)
        row=row+1
def ap_pulling(i):
        global row
        flag=False
        for j in range(0,len(ap)):
            devn=hname_without_ext(ap['name'][j])
            if i== devn:
                flag=True
                sheet.write(row,0,ap['name'][j])
                sheet.write(row,1,ap['ipAddress'][j])
                sheet.write(row,2,ap['type'][j])
                sheet.write(row,3,'Access Point')
                sheet.write(row,4,ap['model'][j])
                sheet.write(row,5,ap['serialNumber'][j])
                sheet.write(row,6,ap['softwareVersion'][j])
                try:
                    days = (int) (int(ap['upTime'][j]) / (1000*60*60*24))
                    sheet.write(row,7,days)#uptime in days %365=years
                except Exception as e:
                    print(str(e))
                row=row+1
                break  
        if flag==False:
            sheet.write(row,0,i)
            row=row+1

def interfaces(i):
    global row2
    for j in df2.index:
        devn=hname_without_ext(df2["deviceName"][j])
        if devn==i:
            worksheet2.write(row2,0,df2["deviceName"][j])
            worksheet2.write(row2,1,df2["ipAddress"][j])
            worksheet2.write(row2,2,df2["name"][j])
            worksheet2.write(row2,3,df2["adminStatus"][j])
            worksheet2.write(row2,4,df2["duplexMode"][j])
            worksheet2.write(row2,5,df2["speed"][j])
            row2=row2+1

def etherChannels(i):
    global row3
    for j in df3.index:
        devn=hname_without_ext(df3["deviceName"][j])
        if devn==i:
            print("hi")
            worksheet3.write(row3,0,df3["deviceName"][j])
            worksheet3.write(row3,1,df3["ipAddress"][j])
            worksheet3.write(row3,2,df3["channelGroupId"][j])
            worksheet3.write(row3,3,df3["name"][j])
            worksheet3.write(row3,4,df3["numberOfMembers"][j])
            row3=row3+1 


def check(sitecode):
    print(sitecode)
    global row
    global row2
    global row3
    global fact_df
    global nei_df
    global df, ap,df2,df3
    row=1
    row2=1
    row3=1
    fact_table_df = pd.read_csv('static/excels/fact.csv')
    fact_df=fact_table_df.replace(np.nan, 'nullvalue')
    nei_table_df=pd.read_csv('static/excels/neighbor_table.csv')
    nei_df=nei_table_df.replace(np.nan, 'nullvalue')
    print(nei_df)
    df = pd.read_csv('static/excels/devices.csv')
    df=df.replace(np.nan, 'nullvalue')
    ap=pd.read_csv('static/excels/net_prime_aps.csv')
    ap=ap.replace(np.nan, 'nullvalue')
    df2=pd.read_csv('static/excels/ethetnetInterfaces.csv')
    df2=df2.replace(np.nan, 'nullvalue')
    print(df2)
    df3=pd.read_csv('static/excels/etherChannels.csv')
    df3=df3.replace(np.nan, 'nullvalue')
    print(df3)
    devicedata=fact_df.loc[fact_df['Site_Code'] == sitecode]
    print(devicedata)

    Devicelist=[]
    hostname=[]
    aplist=[]
    aphostname=[]

    for i in devicedata.index:
        ip=devicedata['IpAddress'][i]
        if 'Router' in devicedata['DeviceType'][i] or 'Router' in devicedata['ProductType'][i] or 'Router' in devicedata['ProductFamily'][i]:
            if ip not in Devicelist:
                Devicelist.append(devicedata['IpAddress'][i])
                hostname.append(devicedata['DeviceName'][i])
        elif 'Switch' in devicedata['DeviceType'][i] or 'Switch' in devicedata['ProductType'][i] or 'Switch' in devicedata['ProductFamily'][i]:
            if ip not in Devicelist:
                Devicelist.append(devicedata['IpAddress'][i])
                hostname.append(devicedata['DeviceName'][i])
        
        elif 'Controller' in devicedata['DeviceType'][i] or 'Controller' in devicedata['ProductType'][i] or 'Controller' in devicedata['ProductFamily'][i]:
            if ip not in Devicelist:
                Devicelist.append(devicedata['IpAddress'][i])
                hostname.append(devicedata['DeviceName'][i])
        elif 'AIR' in  devicedata['ModelNr'][i] or 'AP' in devicedata['DeviceType'][i] or 'AP' in devicedata['ProductType'][i] or 'AP' in devicedata['ProductFamily'][i]:
            if ip not in aplist:
                aplist.append(devicedata['IpAddress'][i])
                aphostname.append(devicedata['DeviceName'][i])
        
    for i in range(0,len(hostname)):
        hostname[i]=hname_without_ext(hostname[i])
    print(len(hostname),hostname)
    frames=[]
    for h in hostname:
        ip_df=neighbor(h,hostname,aphostname)
        frames.append(ip_df)
    print(pd.concat(frames))
    print(hostname)
    print(aphostname) 

    data=pd.concat(frames,ignore_index=True)
    data.drop(data.columns[[2, 4, 8,9,10,11,12,13]], axis = 1, inplace = True)

    writer_object = pd.ExcelWriter("checklist.xlsx",engine ='xlsxwriter')
    workbook_object = writer_object.book
    global sheet
    global worksheet2
    global worksheet3
    sheet = workbook_object.add_worksheet('sheet1')
    sheet.write(0,0,"DeviceName")
    sheet.write(0,1,"ipAddress")
    sheet.write(0,2,"deviceType")
    sheet.write(0,3,"productFamily")
    sheet.write(0,4,"Model")
    sheet.write(0,5,"Serial Number")
    sheet.write(0,6,"Software Version")
    sheet.write(0,7,"Uptime(Days)")
    data.to_excel(writer_object, sheet_name ='neighbor',index=False)

    worksheet2=workbook_object.add_worksheet("ethernetInterfaces")
    worksheet2.write(0,0,"deviceName")
    worksheet2.write(0,1,"ipAddress")
    worksheet2.write(0,2,"name")
    worksheet2.write(0,3,"adminStatus")
    worksheet2.write(0,4,"duplexMode")
    worksheet2.write(0,5,"speed")

    worksheet3=workbook_object.add_worksheet("etherChannels")
    worksheet3.write(0,0,"deviceName")
    worksheet3.write(0,1,"ipAddress")
    worksheet3.write(0,2,"channelGroupId")
    worksheet3.write(0,3,"name")
    worksheet3.write(0,4,"numberOfMembers")
    print("workbook created")
    
        #def etherChannels():
    for i in hostname:
        pulling(i)
        interfaces(i)
        etherChannels(i)
    for i in aphostname:
        ap_pulling(i)

    writer_object.save()