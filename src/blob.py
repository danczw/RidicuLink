from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import json
import os

# load env variables and set api key
load_dotenv()
AZURE_CON_STRING = os.getenv('AZURE_CON_STRING')

try:
    # Create the BlobServiceClient object which will be used to create a container client
    blob_service_client = BlobServiceClient.from_connection_string(
                                                            AZURE_CON_STRING)

    # Create a unique name for the container
    container_name = 'linfluenc-parsed-texts'

    # List container in storage account
    container_list = blob_service_client.list_containers()
    container_list = [container.name for container in container_list]
    print(container_list)

    if container_name in container_list:
        # Load container if exists
        container_client =  blob_service_client.get_container_client(
                                                            container_name)
    else:
        # Create the container if not exists
        container_client = blob_service_client.create_container(
                                                            container_name)
    
    # Create a blob client using the local file name as the name for the blob
    local_path = './data/'
    local_file_name = 'parsed_text.json'
    upload_file_path = os.path.join(local_path, local_file_name)
    blob_client = blob_service_client.get_blob_client(container=container_name,
                                                      blob=local_file_name)

    # get new scraped data
    with open(upload_file_path, 'r+') as local_file:
        new_data = json.load(local_file)
        local_file.close()

    # get existing scraped data from Azure blob storage
    with open(local_path + 'temp.json', 'wb') as temp_file:
        old_data = blob_client.download_blob()
        old_data.readinto(temp_file)
        temp_file.close()

    # append data 
    with open(local_path + 'temp.json', 'r+') as temp_file:
        blob_data_json = json.load(temp_file)
        blob_data_json.update(new_data)
        temp_file.close()

    # open appended data as byte and save to blob
    with open(upload_file_path, 'rb') as upload_file:
        blob_client.upload_blob(upload_file, overwrite=True)
        upload_file.close()

except Exception as ex:
    print('Exception:')
    print(ex)
