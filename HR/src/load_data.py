import requests 

import json 

from azure.storage.filedatalake import DataLakeServiceClient 

from azure.core._match_conditions import MatchConditions 

from azure.storage.filedatalake._models import ContentSettings 

 

# Workday API credentials and endpoint 

workday_api_url = "https://accentureworkday_url/api_endpoint" 

workday_username = "martin.nikolaev" 

workday_password = "d3migold" 

 

# Azure Data Lake Storage credentials 

storage_account_name = "accenture" 

storage_account_key = "accentureWKDkey" 

datalake_container_name = "HR_Datalake" 

datalake_directory_name = "filestore" 

datalake_file_name = "HRDataset_v14.csv" 

 

# Function to get data from Workday API 

def get_data_from_workday(): 

    headers = { 

        'Content-Type': 'application/json', 

        'Accept': 'application/json' 

    } 

    response = requests.get(workday_api_url, auth=(workday_username, workday_password), headers=headers) 

    if response.status_code == 200: 

        return response.text 

    else: 

        raise Exception(f"Error fetching data from Workday API: {response.status_code}") 

 

# Function to upload data to Azure Data Lake 

def upload_data_to_azure_datalake(data): 

    try: 

        service_client = DataLakeServiceClient(account_url=f"https://filestore@accentureazure.dfs.core.windows.net", credential=storage_account_key) 

        file_system_client = service_client.get_file_system_client(file_system=datalake_container_name) 

        directory_client = file_system_client.get_directory_client(datalake_directory_name) 

        file_client = directory_client.get_file_client(datalake_file_name) 

 

        # Upload data to Azure Data Lake 

        file_client.upload_data(data, overwrite=True, content_settings=ContentSettings(content_type='text/csv')) 

        print(f"Data uploaded to Azure Data Lake: HR_Datalake /filestore/ HRDataset_v14.csv")


    except Exception as e: 

        print(f"Error uploading data to Azure Data Lake: {str(e)}") 

 

# Main function 

def main(): 

    raw_data = get_data_from_workday() 

    upload_data_to_azure_datalake(raw_data) 

 

if __name__ == "__main__": 

    main() 