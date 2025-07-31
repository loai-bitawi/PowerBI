import requests
import pandas as pd
import os
import json


def run_factory():
    
    url = 'https://api.bizeebuy.com/oauth2/token'
    
    params= {
        "client_id":os.environ['BIZEEBUY_CLIENT_ID'],
        "client_secret":os.environ['BIZEEBUY_CLIENT_SECRET'],
        "grant_type":"refresh_token",
        "refresh_token": os.environ['BIZEEBUY_REFRESH_TOKEN']
    }
    
    response = requests.post(url, data=params)
    print("Status Code:", response.status_code)
    key= response.json()
    
    # Replace with the actual API URL
    url = "https://api.bizeebuy.com/v1/sales/gross-margin"
    
    # Replace with your actual API key or token
    headers = {
        "Authorization": f"Bearer {key['access_token']}"
    }
    
    from datetime import date, timedelta
    
    start_date = date(2025, 7, 1)
    end_date = date.today()
    
    delta = (end_date - start_date).days
    dates = [start_date + timedelta(days=i) for i in range(delta + 1)]
    
    df=pd.DataFrame(data=None, columns=['company_name',
     'product_name',
     'product_sku',
     'Prod_type',
     'MRP',
     'per_unit_cogs',
     'Total_sale_qty',
     'total_sale',
     'return_qty',
     'return_amt',
     'Total_cost_cogs',
     'profit',
     'profit_per',
     'date'])
    for d in dates:    
        # Replace with the actual data you want to send
        payload ={
            "type":"CUSTOMER",
            "tax":"1",
            "from_date":str(d),
            "to_date":str(d),
            "source" : "INV"
        }
        
        response = requests.post(url, data=payload, headers=headers)
        
        # Check the response
        print("Status Code:", response.status_code)
        data= response.json()
        temp=pd.DataFrame(data['data'])
        temp['date']=d
        
        df=pd.concat([df,temp],ignore_index=True)
        
        
    import pandas as pd
    import io
    
    import gspread
    from oauth2client.service_account import ServiceAccountCredentials
    
    
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
    MAIN_FOLDER_ID = '1Pa9IdGXHnt0VSm97TZpbgDSmH33HjtZH'
    
    
    # Dictionary to store CSV and Excel files as DataFrames, grouped by subfolder names
    data_files_dict = pd.DataFrame()
    
    # Function to recursively fetch all subfolders and their data files
    # Initialize list for this folder
    # Get all files in the folder
    query = f"'{MAIN_FOLDER_ID}' in parents"
    files = drive_service.files().list(q=query).execute().get('files', [])
    
    for file in files:
        if file['name'] == 'SALES CHANNELBU CUSTOMER .xlsx': 
            # Read Excel file into a DataFrame
            request = drive_service.files().get_media(fileId=file['id'])
            file_data = io.BytesIO(request.execute())  
            data_files_dict = pd.read_excel(file_data)  
    
    df=pd.merge(df, data_files_dict,how='left',left_on='company_name',right_on='Customer Name')   
    df.drop('Customer Name',inplace=True,axis=1)
    return df



