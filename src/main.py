from dotenv import load_dotenv
import json
import nlp_bot
import os
from nlp_bot import nlp_bot

# load env variables and set api key
load_dotenv()
OPEN_AI_KEY = os.getenv('OPENAI_API_KEY')

# load data
file_path = './data/'
file_name = 'parsed_text.json'
with open(file_path + file_name, 'r') as file:
    text_data = json.load(file)

openai_bot = nlp_bot(OPEN_AI_KEY, text_data)
openai_bot.create_post(0.7, 200, 1, 0.8)

print(openai_bot.new_post)