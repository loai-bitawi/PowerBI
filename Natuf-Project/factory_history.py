
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 11 15:46:10 2025

@author: LENOVO
"""

import pandas as pd
import os
import io

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json


def run_factory_hist ():
    
    key= json.loads(os.environ['GOOGLE_SERVICE_KEY_JSON'])
    
    
    
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
    MAIN_FOLDER_ID = '1Pa9IdGXHnt0VSm97TZpbgDSmH33HjtZH'
    
    
    # Get all files in the folder
    query = f"'{MAIN_FOLDER_ID}' in parents"
    files = drive_service.files().list(q=query).execute().get('files', [])
    for file in files:
        if file['name'] == 'FACTORY SALES.xlsx': 
            # Read Excel file into a DataFrame
            request = drive_service.files().get_media(fileId=file['id'])
            file_data = io.BytesIO(request.execute())  
            df = pd.read_excel(file_data)  
    return df

