# -*- coding: utf-8 -*-
"""
Created on Thu Jul 31 10:42:58 2025

@author: LENOVO
"""

import pandas as pd
import os
import io

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json

def run_cafe():
    
    key={
      "type": "service_account",
      "project_id": "natuf-project",
      "private_key_id": "3def1829792c55d191003af546368a1d68cead57",
      "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCsw1BNFOv/EY0n\nWr+CAm1aLf2JQGxElhFGK1tzYmLxaJkUjDEYsXKsxjUwia58YHQuXwO+MtVLniVq\nHYpKTOPQ4AYfkbx2DltYTiFXpLxQTLQ2LU2noZgyza2eizoOrpbvYAXcPeH0doj7\nhGKyz9ar8EQIAUTEnd3CpZaEaczWWrd0yUCpC6FdrdncGt58aVqP5UhbKj78M0rl\ncaglN9dBFJsFdwzZiMZusKF2kbMozs1Z6XJmX43Rtb0os42prkj2BTuxjUu4KlrI\npzreaDGGyZ78RHI1+6YJqQWLh8MQNYCGWanr5JxFFJ3fscJMIIf2Z0JpBDAIavvK\nBImtvittAgMBAAECggEAGulSyysQ5vr0LrbxYX5gy90hox1ssBNjTfenh3YCPSIi\nxGNhK3xKxXSbqPuteTTqLCYDVn+jH6QbJmhDGDdZfnpDIexI++fZHUyQX49rASQt\np0nP0Ka4p2NIIgwEh3B1VQTzbL8cAUFsradN25ZKFZ737fpKnMkNmApEw8waSyJ1\nG6FBYQvQeAQ3ntuUJIbiSd2Bi38VFlZiYsf/jZCJTvzftINWfJEQLvrtrSAUsIo6\nQZ+8VoiLAXDy2HFeALGqNbPOoXmTXSMYnS71yZWlW244urJpH9muPiOCQgWq7gXg\nXjOGYNkD8lWy6OfxxQFvl0ZRo2PPj+ZQI/J4IlcGGQKBgQDoe1WQ150U2L4Ts0HN\n0gArS6esout+5gLzQx+l25MZbY1whJy3M6bM7Hc34MX47jSeW45itiw6EyfCy6gh\nu1C8YIc8bzOfEhT/A8d5078tVCe+xPv8e/20joYRsHoah0DNLFrBUzgTkJ1+SadT\ndUvIr1qp2T1j89tZmZTeeDXixQKBgQC+PWtCxx1AG+yKwfXPHobuFh+xuWunbqQG\n+9pMOWd7lGsYIzqD/eZrYU77CK8JzMtTfWsuH9tR8HIMTvV0uAoIwPMKKqqmiyb5\nhlTRfAU0l/O6VwON1lvAkuJLmpvJexMYmJiAFKLcECXRs7j0dfFWmLgtkUBGfgxx\n12Y05YWQiQKBgCIdXxwHF8zkVVgsuN5MD6xKyMsjiS0w8YPi+LTs+LQFiHjXbOvR\nT4vIs2HmwQZbZitKwiUoGGtZPj9uhTiV9S3/eDjdFJUmISCe3Fm7QdWUANUUsOmH\nBF7Hf1L/M5vK9y5kcNjnrlXopcPPaRdtIfbMDKDZ+RE+ypRmXhsbRsUFAoGAUPA6\nsWebt0nqIsMQ/PUE/UjmZSv5dHvrR5lhsCqAL6Dey585ZyzgGvGEs+Nm7Wl3XGcw\n8afWHQ+KxlfVsLoYcs782Gd8wWzUwTb44UO9xzmbFb2tomwAD3eu1fHKtDcr0bwi\nreOZwr0QCh9H4qJHcst5GNICobtBOjIlpv28DNkCgYEAmC+aELk9Bm4HY+FGoyNQ\nAV+CeOINQOrZvS/WwSSJAdEas2lOtGc6B/6jamfdN/4XUmsNmjrDNhvMhmktdO8X\nFt0T3NlX5J+UBj71ZnsLX6HQmCHMSDGFp4mNSvZz98wialHKmddy8a+TspU4WOU1\nt5QUXkKaT239nOR+JSFq7t4=\n-----END PRIVATE KEY-----\n",
      "client_email": "natuf-573@natuf-project.iam.gserviceaccount.com",
      "client_id": "110952632135315212789",
      "auth_uri": "https://accounts.google.com/o/oauth2/auth",
      "token_uri": "https://oauth2.googleapis.com/token",
      "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
      "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/natuf-573%40natuf-project.iam.gserviceaccount.com",
      "universe_domain": "googleapis.com"
    }
    
    
    
    # Define scope for Google Drive API access
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    
    
    # Load service account credentials from JSON file
    creds = ServiceAccountCredentials.from_json_keyfile_dict(key, scope)
    
    # Authenticate client
    client = gspread.authorize(creds)
    
    # List all files in the shared folder
    from googleapiclient.discovery import build
    drive_service = build('drive', 'v3', credentials=creds)
    
    # Set the main folder ID
    MAIN_FOLDER_ID = '1KVgxD6yp9OHj8Uvyg1zpgfncxYHvX331'
    
    
    # Dictionary to store CSV and Excel files as DataFrames, grouped by subfolder names
    data_files_dict = {}
    
    # Function to recursively fetch all subfolders and their data files
    def fetch_data_files(folder_id, folder_name):
        # Initialize list for this folder
        data_files_dict[folder_name] = []
    
        # Get all files in the folder
        query = f"'{folder_id}' in parents"
        files = drive_service.files().list(q=query).execute().get('files', [])
    
        for file in files:
            if file['name'] =='FACTORY':           
                continue
            if file['name'] in ['EVENT SKU CORRECTION.xlsx','SKU Correction.xlsx']: 
                # Read Excel file into a DataFrame
                request = drive_service.files().get_media(fileId=file['id'])
                file_data = io.BytesIO(request.execute())  
                df = pd.read_excel(file_data)  
                data_files_dict[file['name']]=df
            if file['mimeType'] == 'application/vnd.google-apps.folder':  # If it's a subfolder
                fetch_data_files(file['id'], file['name'])  # Recursive call
            elif file['name'] in ['SKU Correction','NOTES','EVENT SKU CORRECTION.xlsx']:
                continue
            elif file['mimeType'] in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:  # If it's an Excel file
                # Read Excel file into a DataFrame
                request = drive_service.files().get_media(fileId=file['id'])
                file_data = io.BytesIO(request.execute())  
                df = pd.read_excel(file_data)  
    
                data_files_dict[folder_name].append(df)  # Store DataFrame in dictionary
            
            elif file['mimeType'] == 'text/csv':  # If it's a CSV file
                # Read CSV file into a DataFrame
                request = drive_service.files().get_media(fileId=file['id'])
                file_data = io.BytesIO(request.execute())  
                df = pd.read_csv(file_data)  
    
                data_files_dict[folder_name].append(df)  # Store DataFrame in dictionary
    
    # Start recursion from the main folder
    fetch_data_files(MAIN_FOLDER_ID, 'Main Folder')
    
    # Print summary
    for subfolder, dfs in data_files_dict.items():
        print(f"\nSubfolder: {subfolder} - {len(dfs)} files loaded.")
    
    
    del data_files_dict['CAFE']
    del data_files_dict['Main Folder']
    clmns=list(data_files_dict['EVENTS'][0].iloc[4])
    master_order_report=pd.DataFrame(data=None, columns=data_files_dict['Master Order Report'][0].columns)
    others=pd.DataFrame(data=None, columns=clmns)
    others['place']=None
    for key in data_files_dict.keys():
        if key == 'Master Order Report':
            for df in data_files_dict[key]:
                master_order_report=pd.concat([master_order_report,df],ignore_index=True)
                
        elif key in ['FACTORY','EVENT SKU CORRECTION.xlsx','SKU Correction.xlsx']:
            continue
                
        else:
            temp=pd.DataFrame(data=None, columns=clmns)
            for df in data_files_dict[key]:
                idx=df.iloc[4]
                temp_df=df[5:]
                temp_df.columns=idx
                temp=pd.concat([temp,temp_df],ignore_index=True)
            temp['place']=key
            if key =='EVENTS':
                corr= data_files_dict['EVENT SKU CORRECTION.xlsx']
                corr['Item Name']=corr['Item Name'].str.upper()
                corr['Item Name']=corr['Item Name'].str.strip()
                temp['Item Name']=temp['Item Name'].str.upper()
                temp['Item Name']=temp['Item Name'].str.strip()
                temp=pd.merge(temp,corr,how='left',left_on='Item Name', right_on='Item Name',suffixes=('','_y'))
                temp['Correct Name']=temp['Correct Name'].fillna(temp['Item Name'])
                temp.drop(['SL NO','Item Name','CAT'],axis=1,inplace=True)
                temp=pd.merge(temp,corr,how='left',left_on='Correct Name', right_on='Correct Name',suffixes=('','_y'))
                temp.drop(['SL NO','Item Name'],axis=1,inplace=True)
                temp.drop_duplicates(inplace=True)
    
                temp.columns=['Date', 'Timestamp', 'Invoice No.',  'Price', 'Qty.',
                       'Sub Total', 'Discount', 'Tax', 'Final Total', 'Table No.',
                       'Server Name', 'Covers', 'Variation', 'Category', 'HSN', 'place',
                       'Item Name', 'CAT']
            else:
                corr= data_files_dict['SKU Correction.xlsx']
                corr['Item Name']=corr['Item Name'].str.upper()
                corr['Item Name']=corr['Item Name'].str.strip()
                temp['Item Name']=temp['Item Name'].str.upper()
                temp['Item Name']=temp['Item Name'].str.strip()
                temp=pd.merge(temp,corr,how='left',left_on='Item Name', right_on='Item Name',suffixes=('','_y'))
                temp['Corrected Name']=temp['Corrected Name'].fillna(temp['Item Name'])
                temp.drop(['Sl','Item Name','Category_y'],axis=1,inplace=True)
    
                temp=pd.merge(temp,corr,how='left',left_on='Corrected Name', right_on='Corrected Name',suffixes=('','_y'))
                temp.drop(['Sl','Item Name'],axis=1,inplace=True)
                temp.drop_duplicates(inplace=True)
                temp.columns=['Date', 'Timestamp', 'Invoice No.',  'Price', 'Qty.',
                       'Sub Total', 'Discount', 'Tax', 'Final Total', 'Table No.',
                       'Server Name', 'Covers', 'Variation', 'Category', 'HSN', 'place',
                       'Item Name', 'CAT']
            others=pd.concat([others,temp],ignore_index=True)
    
    others=others[others['Date']!='Total']
    
    cols=list(master_order_report.columns)
    cols.remove('container_charge')
    cols.remove('order_type')
    
    others['Invoice No.']=others['Invoice No.'].astype(str)
    others['Invoice No.']=others['Invoice No.'].str.strip()
    others['Invoice No.']=others['Invoice No.'].replace("O","O1")
    master_order_report=master_order_report[master_order_report['status']=='Success']
    master_order_report.drop_duplicates(inplace=True)
    master_order_report['invoice_no']=master_order_report['invoice_no'].astype(str)
    master_order_report['invoice_no']=master_order_report['invoice_no'].str.strip()
    others=pd.merge(others, master_order_report,left_on=['Invoice No.','Timestamp'],right_on=['invoice_no','date'],how='left',)
    others.drop(cols,axis=1,inplace=True)
    return others





