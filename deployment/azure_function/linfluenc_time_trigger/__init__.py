import datetime
import logging

import azure.functions as func

from linfluenc_time_trigger.blob import blob
from linfluenc_time_trigger.bot_nlp import nlp_bot
from dotenv import load_dotenv
import os
import requests

def main(mytimer: func.TimerRequest) -> None:
    utc_timestamp = datetime.datetime.utcnow().replace(
        tzinfo=datetime.timezone.utc).isoformat()

    if mytimer.past_due:
        logging.info('The timer is past due!')

    logging.info('Python timer trigger function ran at %s', utc_timestamp)

    # load env variables and set api key
    load_dotenv()
    OPEN_AI_KEY = os.getenv('OPENAI_API_KEY')
    AZURE_CON_STRING = os.getenv('AZURE_CON_STRING')

    # Azure Blob Storage container name
    container_name = 'linfluenc-parsed-texts'
    # blob name
    file_name = 'parsed_text.json'

    # init azure connections
    azure_blob = blob(AZURE_CON_STRING, container_name, file_name)

    # load data
    azure_blob.load_rand_texts(0.7)
    selected_run = azure_blob.selected_run
    selected_run_texts = azure_blob.selected_run_texts

    # create new post
    openai_bot = nlp_bot(OPEN_AI_KEY, selected_run_texts, selected_run)
    openai_bot.create_text(250, 1, 0.9)

    # post to linkedin
    ORGANIZATION_ID = os.getenv('ORGANIZATION_ID')
    ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

    url = 'https://api.linkedin.com/v2/ugcPosts'
    comment = f'''{openai_bot.new_text}\n
                =========================\n
                This text was created using GPT-3. Key word: #{openai_bot.search_word.split("_")[0]}'''

    headers = {'Content-Type': 'application/json',
            'X-Restli-Protocol-Version': '2.0.0',
            'Authorization': 'Bearer ' + ACCESS_TOKEN}

    post_data = {
        'author': 'urn:li:organization:' + ORGANIZATION_ID,
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