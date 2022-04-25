from azure.storage.blob import BlobServiceClient
import datetime
import json
import math
import random

class blob:
    def __init__(self, azure_key: str, container_name: str, file_name: str):
        self.connection_string = azure_key
        self.container_name = container_name
        self.file_name = file_name
        self.selected_run = ''
        self.selected_run_texts = []

    def _select_rand_items(self, text_dict: dict, perc: float):
        '''
        Selects a random key from a dict and random items from its values
        amount of items selected depends on parameter

        Parameter
        ---------
        text_dict : dict[str => list]
            dictionary of scrape runs and corresponding list of texts
        perc : float 
            select % of items from a list => 0.7: 70% of items are selected

        Return
        ---------
        rand_run_key : str
            random scrape run key
        rand_run_texts : list
            random texts from random scrape run
        '''
        # get random run
        all_run_keys = text_dict.keys()
        rand_run_key = random.sample(all_run_keys, 1)[0]

        # get random text items from run
        all_run_texts = text_dict[rand_run_key]
        number_of_texts = math.floor(perc * len(all_run_texts))

        if number_of_texts == 0:
            number_of_texts = 1
        
        number_of_texts = min(10, number_of_texts)

        rand_run_texts = random.sample(all_run_texts, number_of_texts)

        return rand_run_key, rand_run_texts

    def load_rand_texts(self, perc: float):
        '''
        Loads existing text data from Azure Blob Storage

        Parameter
        ---------
        perc : float
            select % of texts from scrape run to be used for gpt3
            => i.e. 0.7 means 70% of texts found for the random selected
                scrape run will be used to create a new text
        '''
        try:
            # Create the BlobServiceClient object which will be used to create a container client
            blob_service_client = BlobServiceClient.from_connection_string(
                                                        self.connection_string)

            # get blob client
            blob_client = blob_service_client.get_blob_client(
                                                container = self.container_name,
                                                blob = self.file_name)

            # get existing scraped data from Azure blob storage
            all_texts_byte = blob_client.download_blob().readall()
            all_texts_json = json.loads(all_texts_byte)

            run_key, run_texts = self._select_rand_items(all_texts_json, perc)

            self.selected_run = run_key
            self.selected_run_texts = run_texts
    
        except Exception as ex:
            print('Exception:')
            print(ex)
            
    def upload_texts(self, text_data: list, search_word: str):
        '''
        Appends and upload latest data to existing texts on Azure Blob Storage

        Parameter
        ---------
        text_data : list
            list of new scraped texts
        search_word : word for which scraping was done for
        '''
        try:
            # Create the BlobServiceClient object which will be used to create a container client
            blob_service_client = BlobServiceClient.from_connection_string(
                                                        self.connection_string)

            # get blob client
            blob_client = blob_service_client.get_blob_client(
                                                container = self.container_name,
                                                blob = self.file_name)

            # setup new scraped data key
            new_data_key = search_word + \
                       '_' + \
                       datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

            # get existing scraped data from Azure blob storage
            existing_texts_byte = blob_client.download_blob().readall()
            existing_texts_json = json.loads(existing_texts_byte)

            # combine new and existing data
            all_texts_json = existing_texts_json.copy()
            all_texts_json[new_data_key] = text_data

            # upload combined data
            blob_client.upload_blob(json.dumps(all_texts_json), overwrite=True)

            print('upload complete')

        except Exception as ex:
            print('Exception:')
            print(ex)