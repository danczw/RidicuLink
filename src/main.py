from dotenv import load_dotenv
import json
import math
import openai
import os
import random

# load env variables and set api key
load_dotenv()
OPEN_AI_KEY = os.getenv('OPENAI_API_KEY')
openai.api_key = OPEN_AI_KEY

# load data
file_path = './data/'
file_name = 'parsed_text.json'
with open(file_path + file_name, 'r') as file:
    text_data = json.load(file)

keys = list(text_data.keys())

# select random scrape run (scrape run = search word and scrape datetime)
if len(keys) == 1:
    key_index = 0
else:
    key_index = random.randint(0, len(keys) - 1)

random_key = keys[key_index]
random_key_texts = text_data[random_key]

# select % random text from scrape run to be used for gpt3
percentage = 0.7
n_texts = math.floor(len(random_key_texts) * percentage)
random_texts = random.sample(random_key_texts, n_texts)

print('Number of posts used for GPT3:', len(random_texts), f'(key word: {random_key})')

# call openai api
response = openai.Completion.create(engine = "text-davinci-001",
                                prompt = random_texts,
                                max_tokens = 200,
                                n = 2,
                                temperature = 0.9)

# filter for longeste reponse text and clean text
all_resp = [i.text for i in response.choices]
long_resp = max(all_resp, key=len)
long_resp = long_resp.replace('  ', ' ')

print(long_resp)