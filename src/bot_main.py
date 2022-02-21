from blob import blob
from dotenv import load_dotenv
import os
from bot_nlp import nlp_bot

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

print(openai_bot.new_text)