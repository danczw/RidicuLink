import datetime
import logging

import azure.functions as func

from linfluenc_time_trigger.blob import blob
from linfluenc_time_trigger.bot_nlp import nlp_bot
import os
import requests

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)
    
    # load env variables
    LINKEDIN_ORG_ID = os.environ['LINKEDIN_ORG_ID']
    LINKEDIN_ACCESS_TOKEN = os.environ['LINKEDIN_ACCESS_TOKEN']
    OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
    BLOB_CON_STRING = os.environ['BLOB_CON_STRING']

    # Azure Blob Storage container name
    container_name = 'linfluenc-parsed-texts'
    # blob name
    file_name = 'parsed_text.json'

    # init azure connections
    azure_blob = blob(BLOB_CON_STRING, container_name, file_name)

    # load data
    azure_blob.load_rand_texts(0.5)
    selected_run = azure_blob.selected_run
    selected_run_texts = azure_blob.selected_run_texts

    # create new post
    openai_bot = nlp_bot(OPENAI_API_KEY, selected_run_texts, selected_run)
    openai_bot.create_text(250, 1, 0.9)

    # post to linkedin
    url = 'https://api.linkedin.com/v2/ugcPosts'
    comment = f'''{openai_bot.new_text}\n
                =========================\n
                This text was created using GPT-3. Key word: #{openai_bot.search_word.split("_")[0]}'''

    headers = {'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0',
            'Authorization': 'Bearer ' + LINKEDIN_ACCESS_TOKEN}

    post_data = {
        'author': 'urn:li:organization:' + LINKEDIN_ORG_ID,
        'lifecycleState': 'PUBLISHED',
        'specificContent': {
            'com.linkedin.ugc.ShareContent': {
                'shareCommentary': {
                    'text': comment  
                },
                'shareMediaCategory': 'NONE'
            }
        },
        'visibility': {
            'com.linkedin.ugc.MemberNetworkVisibility': 'PUBLIC'
        }
    }

    response = requests.post(url, headers=headers, json=post_data)
    print(response)